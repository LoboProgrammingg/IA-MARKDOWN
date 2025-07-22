"""
Configurações centralizadas da aplicação.
Compatível com Pydantic V2.
Utiliza Pydantic BaseSettings para garantir boas práticas, segurança e facilidade de deploy em cloud (GCP, Docker, etc).
Todas as variáveis sensíveis devem ser passadas via ambiente ou arquivo .env (NUNCA hardcode).
"""
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import Optional
from functools import lru_cache
from dotenv import load_dotenv, find_dotenv
import sys

_ = load_dotenv(find_dotenv())

class Settings(BaseSettings):
    # --- JWT/Segurança ---
    access_token_secret_key: str = Field(..., env="ACCESS_TOKEN_SECRET_KEY")
    refresh_token_secret_key: str = Field(..., env="REFRESH_TOKEN_SECRET_KEY")
    access_token_expire_minutes: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_minutes: int = Field(10080, env="REFRESH_TOKEN_EXPIRE_MINUTES")
    secret_key: str = Field(..., env="SECRET_KEY")

    # --- Banco de Dados ---
    database_url: str = Field(..., env="DATABASE_URL")  # Ex: postgresql+asyncpg://user:pass@host/db

    # --- Provedores de IA ---
    gemini_api_key: Optional[str] = Field(None, env="GEMINI_API_KEY")
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    vertexai_project: Optional[str] = Field(None, env="VERTEXAI_PROJECT")
    vertexai_location: Optional[str] = Field(None, env="VERTEXAI_LOCATION")
    vertexai_credentials: Optional[str] = Field(None, env="VERTEXAI_CREDENTIALS")

    # --- Keycloak/Auth ---
    keycloak_url: str = Field(..., env="KEYCLOAK_URL")
    keycloak_realm: str = Field(..., env="KEYCLOAK_REALM")
    keycloak_client_id: str = Field(..., env="KEYCLOAK_CLIENT_ID")
    keycloak_client_secret: str = Field(..., env="KEYCLOAK_CLIENT_SECRET")
    keycloak_audience: str = Field(..., env="KEYCLOAK_AUDIENCE")

    # --- Infra/DevOps ---
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")
    cors_allowed_origins: str = Field("*", env="CORS_ALLOWED_ORIGINS")
    environment: str = Field("development", env="ENVIRONMENT")
    debug: bool = Field(False, env="DEBUG")
    log_level: str = Field("INFO", env="LOG_LEVEL")

    # --- Validação extra ---
    @field_validator(
        "access_token_secret_key", "refresh_token_secret_key", "secret_key", "database_url",
        "keycloak_url", "keycloak_realm", "keycloak_client_id", "keycloak_client_secret", "keycloak_audience",
        mode="before"
    )
    @classmethod
    def check_required(cls, v, info):
        if v is None or v == "":
            raise ValueError(f"A variável obrigatória {info.field_name.upper()} não está definida!")
        return v

    model_config = {
        "extra": "allow",
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Singleton para acessar configurações em toda a aplicação."""
    try:
        return Settings()
    except Exception as e:
        print(f"[ERRO] Falha ao carregar configurações: {e}", file=sys.stderr)
        raise 