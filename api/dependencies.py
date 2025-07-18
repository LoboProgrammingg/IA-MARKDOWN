from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from functools import lru_cache

from pipeline.handler import create_pipeline_with_separated_vectorstores
from langchain_core.language_models.llms import BaseLLM

from .schemas.user import User
from . import security
from .crud import user_crud, token_crud

http_bearer_scheme = HTTPBearer(
    description="Insira o seu Access Token JWT aqui, prefixado com 'Bearer '."
)

@lru_cache(maxsize=1)
def get_pipeline_multi_vs():
    try:
        print("🔧 Carregando o pipeline...")
        pipeline = create_pipeline_with_separated_vectorstores()
        print("✅ Pipeline carregado com sucesso.")
        return pipeline
    except Exception as e:
        print(f"❌ Erro crítico ao carregar o pipeline: {e}")
        raise RuntimeError(f"Não foi possível inicializar o pipeline: {e}") from e

def get_active_pipeline():
    try:
        return get_pipeline_multi_vs()
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"O pipeline de IA não está disponível: {e}",
        )


class MockLLM(BaseLLM):
    def _call(self, prompt: str, stop: list[str] | None = None, **kwargs) -> str:
        return f"Resposta mock para a pergunta: {prompt[:100]}..."
    
    @property
    def _llm_type(self) -> str:
        return "mock"

@lru_cache(maxsize=1)
def get_llm_model() -> MockLLM:
    print("🔧 Inicializando o Mock LLM...")
    return MockLLM()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer_scheme)) -> User:
    token = credentials.credentials
    payload = security.decode_access_token(token)
    
    jti = payload.get("jti")
    if not jti or token_crud.is_token_denied(jti):
        raise HTTPException(status_code=401, detail="Token inválido ou revogado")
        
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Conteúdo do token inválido")
    
    user = user_crud.get_user_by_email(email=email)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuário do token não encontrado")
    
    return User.model_validate(user)

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user

def get_current_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="O usuário não tem privilégios de administrador",
        )
    return current_user