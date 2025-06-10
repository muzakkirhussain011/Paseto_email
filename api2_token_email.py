# Token-and-Mail micro-service (FastAPI · PASETO v4.local · AWS SES)
#
# Endpoints
#   • POST /internal/register   → token + 6-digit OTP e-mail
#   • POST /internal/login      → token only
#   • POST /internal/token      → generic token factory
#   • POST /internal/send_email → plain-text SES mailer
#   • GET  /protected/ping      → demo protected resource
#
# All routes except /protected/ping require X-API-Key.

import os, random, json, logging
from datetime import datetime, timedelta
from typing import Optional

import boto3, pyseto
from botocore.exceptions import ClientError
from dotenv import load_dotenv, find_dotenv
from fastapi import (
    FastAPI, Header, HTTPException, status,
    Depends, Security
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr

# ───────────────────  0. ENV & LOGS  ───────────────────────────
load_dotenv(find_dotenv(usecwd=True))

def log_json(level, msg, **kw):
    logging.log(level, json.dumps({"msg": msg, **kw}))

SERVICE_API_KEY = os.getenv("SERVICE_API_KEY")
PASETO_KEY      = os.getenv("PASETO_SYMMETRIC_KEY")    # 32-byte
SENDER_EMAIL    = os.getenv("SENDER_EMAIL")
AWS_REGION      = os.getenv("AWS_REGION", "us-east-1")

for k, v in {"SERVICE_API_KEY": SERVICE_API_KEY,
             "PASETO_SYMMETRIC_KEY": PASETO_KEY,
             "SENDER_EMAIL": SENDER_EMAIL}.items():
    if not v:
        raise RuntimeError(f"Missing env var {k}")
if len(PASETO_KEY.encode()) != 32:
    raise RuntimeError("PASETO_SYMMETRIC_KEY must be exactly 32 bytes")

ses = boto3.client("ses", region_name=AWS_REGION)

app = FastAPI(title="API-2 · Token & Mail (v4.local)")

# ───────────────────  1. HELPERS  ──────────────────────────────
def _auth_key(x_api_key: str | None):
    if x_api_key != SERVICE_API_KEY:
        raise HTTPException(401, "Bad X-API-Key")

def _issue_token(uid: str, email: str, mins=60) -> str:
    now  = datetime.utcnow()
    data = {
        "sub"  : uid,
        "email": email,
        "iat"  : int(now.timestamp()),
        "exp"  : int((now + timedelta(minutes=mins)).timestamp()),
    }
    key = pyseto.Key.new(version=4, purpose="local",
                         key=PASETO_KEY.encode())
    return pyseto.encode(key, data)

def _send_plain(to_addr: str, subject: str, body: str,
                bcc: list[str] | None = None):
    dest = {"ToAddresses": [to_addr]}
    if bcc: dest["BccAddresses"] = bcc
    ses.send_email(
        Source=SENDER_EMAIL,
        Destination=dest,
        Message={
            "Subject": {"Data": subject, "Charset": "UTF-8"},
            "Body":    {"Text": {"Data": body, "Charset": "UTF-8"}},
        },
    )

# ───────────────────  2. MODELS  ───────────────────────────────
class BaseUser(BaseModel):
    user_id: str
    email_address: EmailStr

class RegisterRequest(BaseUser):
    name: Optional[str] = None

class LoginRequest(BaseUser):
    pass

class TokenRequest(BaseUser):
    pass

class EmailRequest(BaseModel):
    email_address: EmailStr
    subject: str
    body: str
    bcc: Optional[list[EmailStr]] = None

# ───────────────────  3. TOKEN VERIFIER  ───────────────────────
bearer = HTTPBearer(auto_error=False)
key_v4_local = pyseto.Key.new(
    version=4, purpose="local", key=PASETO_KEY.encode())

async def verify_bearer(
    cred: HTTPAuthorizationCredentials = Security(bearer)):
    if not cred:
        raise HTTPException(401, "Missing Bearer token")
    try:
        payload = pyseto.decode(key_v4_local, cred.credentials, verify=True)
    except pyseto.PasetoError:
        raise HTTPException(401, "Invalid PASETO")
    if payload["exp"] < int(datetime.utcnow().timestamp()):
        raise HTTPException(401, "Token expired")
    return payload

# ───────────────────  4. ENDPOINTS  ────────────────────────────
@app.post("/internal/register", status_code=201)
async def register(data: RegisterRequest,
                   x_api_key: str = Header(None, alias="X-API-Key")):
    _auth_key(x_api_key)
    token = _issue_token(data.user_id, data.email_address)
    otp   = f"{random.randint(0, 999999):06d}"

    body = f"""Hi {data.name or ''},

Your one-time verification code:

    {otp}

It expires in 10 minutes.

– ViCertify
"""
    try:
        _send_plain(data.email_address,
                    "Your ViCertify verification code", body)
        log_json(logging.INFO, "OTP mail sent",
                 email=data.email_address, otp=otp)
    except ClientError as e:
        log_json(logging.ERROR, "SES error", err=e.response["Error"])
        raise HTTPException(502, "SES failed")
    return {"access_token": token, "token_type": "bearer", "expires_in": 3600}


@app.post("/internal/login", status_code=200)        # ← fixed
async def login(data: LoginRequest,
                x_api_key: str = Header(None, alias="X-API-Key")):
    _auth_key(x_api_key)
    token = _issue_token(data.user_id, data.email_address)
    return {"access_token": token, "token_type": "bearer", "expires_in": 3600}


@app.post("/internal/token", status_code=200)        # ← fixed
async def generic_token(data: TokenRequest,
                        x_api_key: str = Header(None, alias="X-API-Key")):
    _auth_key(x_api_key)
    token = _issue_token(data.user_id, data.email_address)
    return {"access_token": token, "token_type": "bearer", "expires_in": 3600}


@app.post("/internal/send_email", status_code=202)   # ← fixed
async def send_email(data: EmailRequest,
                     x_api_key: str = Header(None, alias="X-API-Key")):
    _auth_key(x_api_key)
    try:
        _send_plain(data.email_address, data.subject,
                    data.body, data.bcc)
        return {"status": "queued"}
    except ClientError as e:
        raise HTTPException(502, e.response["Error"]["Message"])


# ——— protected resource to demo token validation ——————————
@app.get("/protected/ping")
async def ping(payload: dict = Depends(verify_bearer)):
    return {"ok": True, "token": payload}

# start → uvicorn api2_token_email:app --host 0.0.0.0 --port 8000
