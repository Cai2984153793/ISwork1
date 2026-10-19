# Work 1: Secure REST API Development with CI/CD and Real CVE Vulnerability Analysis
## Project Purpose
Develop secure Flask‑based REST API with OWASP Top‑10 protections, integrate SAST & SCA security scanning inside GitHub Actions CI/CD pipeline.
Additionally reproduce, analyse and patch a real CVE vulnerability using Vulhub docker environment.

## Repository Link
https://github.com/Cai2984153793/ISwork1.git

## Last successful CI pipeline run link
https://github.com/Cai2984153793/ISwork1/actions/runs/39197607411

## API Endpoints description
Stack: Python Flask + SQLite(SQLAlchemy ORM)

### 1. POST /register
Create new user account. Username input sanitized against XSS.
Request Body(JSON):
```json
{
    "username":"testuser",
    "password":"123456"
}
Response: `201 Created`
{"msg":"register success"}

### 2. POST /auth/login (Lab‑required endpoint)

User authentication, returns JWT access token.
Request Body(JSON):
{
    "username":"testuser",
    "password":"123456"
}
Response: `200 OK`
{"token":"<JWT_TOKEN_VALUE>"}
### . GET /api/data (Lab‑required protected endpoint)

Return simulated dataset. **Access restricted only for authenticated users.**
Request Headers:
`Authorization: Bearer <JWT_TOKEN_VALUE>`

Response example:
{
  "user": "testuser",
  "data": [
    {"id": 1, "info": "public secure data 1"},
    {"id": 2, "info": "public secure data 2"}
  ]
}
### 4. GET /api/whoami (Custom self‑implemented endpoint)

Custom protected endpoint, output current logged‑in user identity info.
Request Headers:
`Authorization: Bearer <JWT_TOKEN_VALUE>`

Response example:
{
  "login_user_id": "1",
  "login_username": "testuser"
}
## Implemented Security Measures

### 1. SQL Injection protection

Application uses **SQLAlchemy ORM**. Database queries are built via ORM API, no manual SQL string concatenation. ORM internally uses parameterized prepared statements to eliminate SQL injection attack surface.

### 2. Cross‑Site Scripting (XSS) protection

User‑controlled username input is sanitized with `bleach.clean()` before processing. Potentially dangerous HTML tags and symbols are escaped.

### 3. Broken Authentication mitigation

1. User passwords are stored as **bcrypt password hashes**. Plain‑text passwords are never persisted in SQLite database.
2. Upon successful login server issues short‑lived JWT token with expiration timestamp.
3. Every protected API endpoint validates Bearer JWT token from HTTP request header. Unauthenticated requests get HTTP‑401 rejection.

## CI / CD Security Pipeline

Workflow file location: `.github/workflows/ci.yml`

- Trigger condition: every push and pull request to `master` branch
- SAST tool: **Bandit** — static source‑code security testing for Python
- SCA tool: **Safety** — software composition analysis, scan vulnerabilities inside third‑party dependencies

> 
> Note: Bandit and Safety will return non‑zero exit codes when vulnerabilities are detected. `|| true` added in commands to guarantee full pipeline execution and report generation, even if security issues are found.
> Scan reports are saved as workflow artifacts inside GitHub Actions.

### Screenshots of SAST / SCA reports

> 
> Insert screenshots of pipeline run, bandit‑report.json and safety‑report.json here.

## CVE Vulnerability Lab (Vulhub)

> 
> Selected CVE: **CVE‑2018‑1000656 — Flask Jinja2 Server‑Side Template Injection(SSTI)**

### Brief vulnerability description

> 
> Fill after finishing vulhub lab.

### Reproduction sequence & commands

> 
> Fill after finishing vulhub lab. Insert screenshots for exploit steps.

### Root‑cause analysis

> 
> Fill after finishing vulhub lab.

### Applied fix description

> 
> Fill after finishing vulhub lab. What was modified and why this fix works.

### Proof of vulnerability elimination

> 
> Fill after finishing vulhub lab. Insert screenshots showing attack payload no longer works.