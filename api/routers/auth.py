from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from .. import security
from ..crud import user_crud, token_crud
from ..schemas.user import Token, TokenRefreshRequest

from ..dependencies import http_bearer_scheme

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token, summary="Realizar login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_crud.get_user_by_email(form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
        )
    
    user_data = {"sub": user.email}
    access_token = security.create_access_token(data=user_data)
    refresh_token = security.create_refresh_token(data=user_data)
    
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/refresh", response_model=Token, summary="Atualizar Access Token")
def refresh_access_token(request: TokenRefreshRequest):
    payload = security.decode_refresh_token(request.refresh_token)
    email: str = payload.get("sub")
    
    user = user_crud.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário do token não encontrado")
        
    user_data = {"sub": user.email}
    new_access_token = security.create_access_token(data=user_data)
    new_refresh_token = security.create_refresh_token(data=user_data)
    
    return {"access_token": new_access_token, "refresh_token": new_refresh_token}

@router.post("/logout", summary="Realizar logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(http_bearer_scheme)):
    token = credentials.credentials
    payload = security.decode_access_token(token)
    jti = payload.get("jti")
    if jti:
        token_crud.add_token_to_denylist(jti)
    
    return {"message": "Logout bem-sucedido"}
