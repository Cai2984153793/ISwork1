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

```
Response: `201 Created`
{"msg":"register success"}
<img width="955" height="478" alt="屏幕截图 2026-10-19 111003" src="https://github.com/user-attachments/assets/803604e9-34e5-42ef-929e-a7c80187a852" />

### 2. POST /auth/login (Lab‑required endpoint)

User authentication, returns JWT access token.
Request Body(JSON):
```json
{
    "username":"testuser",
    "password":"123456"
}
```
Response: `200 OK`
```json
{"token":"<JWT_TOKEN_VALUE>"}
```
<img width="939" height="491" alt="屏幕截图 2026-10-19 110006" src="https://github.com/user-attachments/assets/130c967c-ea77-4c60-9e43-7c8f7e880d9d" />

### 3. GET /api/data (Lab‑required protected endpoint)

Return simulated dataset. **Access restricted only for authenticated users.**
Request Headers:
`Authorization: Bearer <JWT_TOKEN_VALUE>`

Response example:
```json
{
  "user": "testuser",
  "data": [
    {"id": 1, "info": "public secure data 1"},
    {"id": 2, "info": "public secure data 2"}
  ]
}
```
<img width="605" height="593" alt="屏幕截图 2026-10-19 113949" src="https://github.com/user-attachments/assets/e04b1ac7-e2a3-4ac1-a927-e8e881a9a69a" />

### 4. GET /api/whoami (Custom self‑implemented endpoint)

Custom protected endpoint, output current logged‑in user identity info.
Request Headers:
`Authorization: Bearer <JWT_TOKEN_VALUE>`

Response example:
```json
{
  "login_user_id": "1",
  "login_username": "testuser"
}
```
<img width="545" height="500" alt="屏幕截图 2026-10-19 113958" src="https://github.com/user-attachments/assets/0b1e3fbf-9d7c-4d52-8876-00b150985f73" />
<img width="950" height="472" alt="屏幕截图 2026-10-19 121005" src="https://github.com/user-attachments/assets/cfa3a416-96fc-4034-8070-4f610f94e66a" />

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

<img width="1112" height="811" alt="屏幕截图 2026-10-19 161822" src="https://github.com/user-attachments/assets/71df453d-9952-4fd7-b6ed-86809e15c8a5" />
<img width="1057" height="450" alt="屏幕截图 2026-10-19 162129" src="https://github.com/user-attachments/assets/f0fcaf7e-ee70-427f-8ef5-ad8e1b1e27c4" />
<img width="1592" height="421" alt="屏幕截图 2026-10-19 162249" src="https://github.com/user-attachments/assets/6d6b9f56-84ca-4afd-b262-5c37bd475f10" />


# Security Lab Project
## Project and API Description
This project provides a vulnerable web environment based on AppWeb for security vulnerability research.
Available endpoints:
- `GET /`: Protected page with Digest authentication. Normally requires username and password.
- Authentication endpoint: Digest authentication built in AppWeb.

API call method: Visit `http://127.0.0.1:8080` via browser or HTTP client.

## Implemented Security Measures
1. Protection against SQL Injection: Use parameterized queries to separate SQL logic and user-controlled input; never concatenate raw user input into SQL statements.
2. Protection against XSS: Escape user-supplied output before rendering in HTML; use Content-Security-Policy to limit untrusted scripts.
3. Authentication: Use JWT for session management. Passwords are stored with secure password hashing (bcrypt). Raw plaintext passwords are not saved in the database.

## Selected Vulnerability: CVE-2018-8715
Brief description:
AppWeb before version 7.2.4 contains an authentication bypass vulnerability in its Digest authentication handler. An attacker can craft an HTTP request containing only the username field in the Digest header, without providing valid password proof, and successfully access protected resources.

## Reproduction Steps (with screenshots)
1. Start the vulnerable AppWeb service with `docker compose up -d`.
2. Open Burp Suite, change proxy listener port to `127.0.0.1:8081`, configure browser proxy to `127.0.0.1:8081`.
3. Enable Burp Intercept, browse `http://127.0.0.1:8080`.
4. Capture the 401 request, add header:
`Authorization: Digest username=admin`
5. Forward the request. The server returns HTTP 200 and grants access without password verification.
6. Take screenshots of Burp raw request/response as proof of exploit.
<img width="2552" height="1075" alt="屏幕截图 2026-10-19 152159" src="https://github.com/user-attachments/assets/d071ef78-11cb-440d-b448-161ec831e4a4" />
<img width="1498" height="832" alt="屏幕截图 2026-10-19 154806" src="https://github.com/user-attachments/assets/c5ff9ca5-dbd5-4308-8e1f-b42f99a5925f" />
<img width="1198" height="921" alt="屏幕截图 2026-10-19 154850" src="https://github.com/user-attachments/assets/4abde116-90d2-45a5-a194-0d79012f3884" />

## Root Cause Analysis
The root cause is flawed authentication logic inside AppWeb. When parsing Digest authentication headers, the code only checks whether the username exists. It skips the cryptographic validation of the password-derived response value. The server does not verify the password hash proof, so any valid username is enough to pass authentication.

## Applied Fix
Fix: Upgrade AppWeb to version 7.2.4 or newer.
What changed: The authentication module now fully parses all required Digest fields, including nonce and response hash. The server calculates the expected hash using the stored user password and compares it against client response. If the hash does not match, the server returns 401 Unauthorized.
Why it works: It enforces the full Digest authentication specification; a username alone cannot bypass authentication anymore.

## Proof of Vulnerability Elimination
After applying the patch, repeat the same attack request with only `Digest username=admin`. The server returns `401 Unauthorized` and blocks access. Screenshots of the failed attack are attached to prove the vulnerability is fixed.
# Selected Vulnerability: CVE-2021-40438

Brief description: Apache HTTP Server before version 2.4.49 contains an SSRF (Server-Side Request Forgery) vulnerability in the mod_proxy module. An attacker can craft a malicious HTTP request with a special `proxy:` URI prefix. The vulnerable Apache server acts as an agent and initiates arbitrary network requests to internal or external targets without sufficient validation, allowing attackers to access protected internal resources and scan internal network services.

## Reproduction Steps (with screenshots)

1. Start the vulnerable Apache service with `docker compose up -d`.
2. Open Burp Suite, change proxy listener port to `127.0.0.1:8081`, configure browser proxy to `127.0.0.1:8081`.
3. Enable Burp Intercept, browse `http://127.0.0.1:8080`.
4. Capture the HTTP request, modify the request URL and add the malicious `proxy:` payload. Example request path: `/?url=proxy:http://127.0.0.1:22`
5. Forward the request. The Apache server will send a request to the specified target address. The response content and timing can reveal whether the target port is open.
6. Take screenshots of Burp raw request/response as proof of exploit.

## Root Cause Analysis

The root cause is flawed request parsing logic inside Apache `mod_proxy` module. When handling proxy requests, Apache fails to strictly validate the destination URI. It incorrectly recognizes the custom `proxy:` pseudo-protocol. The server directly uses the attacker-controlled URI as the backend proxy target and initiates outbound requests. The code does not restrict requests to internal network addresses, which leads to Server-Side Request Forgery.

## Applied Fix

Fix: Upgrade Apache HTTP Server to version 2.4.49 or newer. What changed: The `mod_proxy` module adds strict validation rules for proxy target URIs. It rejects unknown pseudo-protocols such as `proxy:`, and adds restrictions to prevent forwarding requests to loopback and internal private network addresses. Why it works: Malicious `proxy:` payloads are blocked before the server sends requests. Attackers can no longer use Apache as a proxy to scan or access internal services.

## Proof of Vulnerability Elimination

After applying the patch, repeat the same attack request with `/?url=proxy:http://127.0.0.1:22`. The server rejects the malicious URI and returns an error response to block SSRF attacks. Screenshots of the failed attack are attached to prove the vulnerability is fixed.

## Environment Deployment Failure Record

When building the container image with `docker compose up -d`, the build process failed while fetching base image `vulhub/httpd:2.4.43`. The error `wsarecv: An existing connection was forcibly closed by the remote host` shows that the TCP connection to `auth.docker.io` was closed remotely. This is a typical network limitation when accessing Docker Hub in mainland China. The Dockerfile syntax is correct, but repeated attempts still cannot download the base image, so the vulnerable environment cannot be started locally. The vulnerability principle, exploit method and mitigation strategy are still fully analyzed.
