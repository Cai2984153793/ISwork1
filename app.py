from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import jwt
import bcrypt
from datetime import datetime, timedelta
from datetime import timezone
import bleach

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "my_secure_secret_key_2026_longkey123456"
db = SQLAlchemy(app)

# 用户模型：password_hash存bcrypt字节哈希，不再存明文密码
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.LargeBinary, nullable=False)

with app.app_context():
    db.create_all()

# 注册接口
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = bleach.clean(data.get('username', ''))
    password = data.get('password', '')
    if not username or not password:
        return jsonify({"msg": "username and password required"}),400
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "user already exists"}), 409
    # bcrypt哈希密码
    hash_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    new_user = User(username=username, password_hash=hash_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "register success"}), 201

# 任务要求：POST /auth/login
@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = bleach.clean(data.get('username', ''))
    password = data.get('password', '')
    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.checkpw(password.encode("utf-8"), user.password_hash):
        return jsonify({"msg": "invalid username or password"}), 401
    payload = {
        "sub": str(user.id),
        "username": user.username,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({"token": token})

# 任务要求：受保护接口 GET /api/data
@app.route('/api/data', methods=['GET'])
def api_data():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"msg": "missing token"}), 401
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    except Exception as e:
        print("JWT ERROR:", str(e))
        return jsonify({"msg": "invalid token"}), 401
    # 返回模拟业务数据
    mock_data = [
        {"id":1,"info":"public secure data 1"},
        {"id":2,"info":"public secure data 2"}
    ]
    return jsonify({"user":payload["username"], "data":mock_data})

# 自定义第三个接口（自己设计，例：GET /api/whoami 返回当前登录用户信息）
@app.route('/api/whoami', methods=['GET'])
def whoami():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"msg": "missing token"}), 401
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    except Exception as e:
        print("JWT ERROR:", str(e))
        return jsonify({"msg": "invalid token"}), 401
    return jsonify({"login_user_id": payload["sub"], "login_username": payload["username"]})

if __name__ == '__main__':
    app.run(debug=True)
