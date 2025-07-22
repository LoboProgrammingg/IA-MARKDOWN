# api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from .responses import error_response
from fastapi.responses import JSONResponse
import logging
import os
import json
from redis.asyncio import from_url
from redis.exceptions import ConnectionError as RedisConnectionError

# ATUALIZAÇÃO: A importação de 'templates' foi substituída por 'prompts' e 'contexts'
from .routers import (
    auth,
    users,
    chat,
    documents,
    retrievers,
    pipelines,
    system,
    contexts,
    prompts,
)
from .crud import user_crud
from retriever import config_manager as retriever_config_manager
from pipeline import config_manager as pipeline_config_manager
from .responses import success_response
from .settings import get_settings
settings = get_settings()
from fastapi_limiter import FastAPILimiter

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# Instanciação da aplicação FastAPI com metadados para documentação
app = FastAPI(
    title="IA-MARKDOWN API",
    description="""
API para gerenciamento de recursos de IA (documentos, prompts, templates, contextos, pipelines, retrievers, etc).

**Autenticação:**
- Todos os endpoints protegidos exigem JWT emitido pelo Keycloak.
- Para obter um token, faça uma requisição POST para:
  `http://<KEYCLOAK_HOST>/realms/<REALM>/protocol/openid-connect/token`
  com os campos:
    - `grant_type=password`
    - `client_id=<CLIENT_ID>`
    - `client_secret=<CLIENT_SECRET>` (se necessário)
    - `username=<USUÁRIO>`
    - `password=<SENHA>`
- Envie o token no header: `Authorization: Bearer <token>`

**RBAC:**
- Endpoints sensíveis exigem roles específicos do Keycloak (ex: `admin`).

**Não existe mais login/logout local.**
""",
    version="1.0.0",
    contact={
        "name": "Matheus Lobo Camara",
        "url": "http://example.com", # Adicione um link se desejar
        "email": "matheuscamara@mti.mt.gov.br",
    },
    license_info={
        "name": "MTI - GOV",
        "url": "https://www.mti.mt.gov.br/",
    },
)

# Configuração de logging estruturado para produção (GCP)
if settings.environment == "production":
    class JsonFormatter(logging.Formatter):
        def format(self, record):
            log_record = {
                "level": record.levelname,
                "time": self.formatTime(record, self.datefmt),
                "message": record.getMessage(),
                "name": record.name,
            }
            if record.exc_info:
                log_record["exception"] = self.formatException(record.exc_info)
            return json.dumps(log_record)
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logging.basicConfig(level=logging.INFO, handlers=[handler])
else:
    logging.basicConfig(level=logging.INFO)

# Evento de startup para inicializar componentes essenciais
@app.on_event("startup")
async def on_startup():
    """Executa ações na inicialização da API, como carregar configurações."""
    logging.info("--- Executando tarefas de inicialização da API ---")
    user_crud.init_db()
    retriever_config_manager.load_configurations()
    pipeline_config_manager.load_configurations()
    # Inicializar o FastAPI-Limiter (rate limiting)
    try:
        redis = from_url(settings.redis_url, encoding="utf-8", decode_responses=True)
        await FastAPILimiter.init(redis)
        logging.info("--- FastAPI-Limiter (rate limiting) ativado com Redis ---")
    except RedisConnectionError as e:
        logging.warning(f"[AVISO] Não foi possível conectar ao Redis para rate limiting: {e}")
        logging.warning("[AVISO] O rate limiting está DESATIVADO. Para ativar, configure o Redis corretamente.")
    # A carga dos prompts e contextos já acontece na importação dos seus módulos CRUD
    logging.info("--- Inicialização concluída ---")

# Configuração do CORS para permitir requisições de diferentes origens
allowed_origins = [origin.strip() for origin in settings.cors_allowed_origins.split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão dos routers para organizar os endpoints
logging.info("--- Incluindo routers na aplicação ---")
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(documents.router)
app.include_router(system.router)
app.include_router(retrievers.router)
app.include_router(pipelines.router)
app.include_router(chat.router)
app.include_router(contexts.router)
app.include_router(prompts.router)
logging.info("--- Routers incluídos com sucesso ---")


@app.get('/', tags=["Root"], summary="Verificar o status da API")
def read_root():
    """Endpoint raiz que retorna uma mensagem de boas-vindas e o status da API."""
    return success_response(
        data={"docs_url": "/docs"},
        message="API online e funcionando!"
    )

@app.get('/health', tags=["Monitoramento"], summary="Healthcheck da API", description="Endpoint para monitoramento automatizado. Retorna 200 se a API estiver online.")
def healthcheck():
    return success_response(message="API saudável", data={"status": "ok"})

@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return error_response(
        message=exc.detail if exc.detail else "Erro HTTP",
        status_code=exc.status_code,
        error_code=str(exc.status_code),
        details={"path": request.url.path}
    )

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return error_response(
        message="Erro de validação nos dados enviados.",
        status_code=422,
        error_code="validation_error",
        details=exc.errors()
    )

@app.exception_handler(Exception)
def generic_exception_handler(request: Request, exc: Exception):
    logging.exception(f"Erro inesperado: {exc}")
    return error_response(
        message="Erro interno inesperado.",
        status_code=500,
        error_code="internal_error",
        details={"exception": str(exc), "path": request.url.path}
    )
