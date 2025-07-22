from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import HTTPAuthorizationCredentials
from .. import security
from ..crud import token_crud
from fastapi_limiter.depends import RateLimiter
import httpx
from api.settings import get_settings

from ..dependencies import http_bearer_scheme

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
    "/refresh",
    summary="Atualizar Access Token via Keycloak",
    description="Recebe um refresh_token e retorna novo access_token/refresh_token do Keycloak. Use este endpoint para renovar o token sem precisar relogar. Respostas de erro: 400 (payload inválido), 401 (refresh token inválido ou expirado)."
)
def refresh_token_proxy(payload: dict = Body(...)):
    refresh_token = payload.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="refresh_token é obrigatório.")
    settings = get_settings()
    token_url = f"{settings.keycloak_url}/realms/{settings.keycloak_realm}/protocol/openid-connect/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": settings.keycloak_client_id,
        "client_secret": settings.keycloak_client_secret,
    }
    response = httpx.post(token_url, data=data)
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Refresh token inválido ou expirado.")
    return response.json()
