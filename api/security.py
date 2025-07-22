import os
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status
from .settings import get_settings
import logging
import json

settings = get_settings()

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuração básica de logging estruturado
logger = logging.getLogger("security")
handler = logging.StreamHandler()
formatter = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", "msg": %(message)s}')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    result = pwd_context.verify(plain_password, hashed_password)
    if not result:
        logger.info(json.dumps({"event": "password_verification_failed", "msg": "Senha incorreta."}))
    return result

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    to_encode.update({"jti": os.urandom(16).hex()})
    return jwt.encode(to_encode, settings.access_token_secret_key, algorithm=ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.refresh_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.refresh_token_secret_key, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.access_token_secret_key, algorithms=[ALGORITHM])
    except JWTError as e:
        logger.warning(json.dumps({"event": "access_token_invalid", "error": str(e)}))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

def decode_refresh_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.refresh_token_secret_key, algorithms=[ALGORITHM])
    except JWTError as e:
        logger.warning(json.dumps({"event": "refresh_token_invalid", "error": str(e)}))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
