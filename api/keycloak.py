import httpx
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status, Request
from functools import lru_cache
from typing import Dict, Any
from .settings import get_settings
import logging
import json

# Configuração básica de logging estruturado
logger = logging.getLogger("auth")
handler = logging.StreamHandler()
formatter = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", "msg": %(message)s}')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

@lru_cache(maxsize=1)
def get_jwks():
    settings = get_settings()
    url = f"{settings.keycloak_url}/realms/{settings.keycloak_realm}/protocol/openid-connect/certs"
    resp = httpx.get(url)
    resp.raise_for_status()
    return resp.json()

def get_public_key(token: str) -> str:
    jwks = get_jwks()
    unverified_header = jwt.get_unverified_header(token)
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            return jwt.algorithms.RSAAlgorithm.from_jwk(key)
    logger.warning(json.dumps({"event": "public_key_not_found", "kid": unverified_header.get("kid"), "msg": "Chave pública não encontrada para o token JWT."}))
    raise HTTPException(status_code=401, detail="Chave pública não encontrada para o token JWT.")

def verify_jwt_token(token: str) -> Dict[str, Any]:
    settings = get_settings()
    try:
        public_key = get_public_key(token)
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=settings.keycloak_client_id,
            options={"verify_exp": True}
        )
        return payload
    except JWTError as e:
        logger.warning(json.dumps({"event": "jwt_invalid", "error": str(e)}))
        raise HTTPException(status_code=401, detail=f"Token JWT inválido: {e}")

def get_current_user(request: Request) -> Dict[str, Any]:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        logger.info(json.dumps({"event": "jwt_missing", "msg": "Token JWT não fornecido.", "headers": dict(request.headers)}))
        raise HTTPException(status_code=401, detail="Token JWT não fornecido.")
    token = auth_header.split()[1]
    return verify_jwt_token(token)

def require_roles(*roles):
    def dependency(user=Depends(get_current_user)):
        user_roles = user.get("realm_access", {}).get("roles", [])
        if not any(role in user_roles for role in roles):
            logger.info(json.dumps({"event": "role_denied", "required_roles": roles, "user_roles": user_roles, "msg": "Permissão negada."}))
            raise HTTPException(status_code=403, detail=f"Permissão negada. Requer um dos roles: {roles}")
        return user
    return dependency