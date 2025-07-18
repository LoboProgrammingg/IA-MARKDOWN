# api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ATUALIZAÇÃO: A importação de 'templates' foi substituída por 'prompts' e 'contexts'
from .routers import (
    auth,
    users,
    chat,
    documents,
    retrievers,
    pipelines,
    system,
)
from .crud import user_crud
from retriever import config_manager as retriever_config_manager
from pipeline import config_manager as pipeline_config_manager

# Instanciação da aplicação FastAPI com metadados para documentação
app = FastAPI(
    title="API do Chatbot com RAG",
    description="Uma API robusta para interagir com um sistema de IA, com gerenciamento completo de configurações, documentos e usuários.",
    version="8.0.0", # Versão final com gerenciamento de prompts e contextos
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

# Evento de startup para inicializar componentes essenciais
@app.on_event("startup")
def on_startup():
    """Executa ações na inicialização da API, como carregar configurações."""
    print("--- Executando tarefas de inicialização da API ---")
    user_crud.init_db()
    retriever_config_manager.load_configurations()
    pipeline_config_manager.load_configurations()
    # A carga dos prompts e contextos já acontece na importação dos seus módulos CRUD
    print("--- Inicialização concluída ---")

# Configuração do CORS para permitir requisições de diferentes origens
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, restrinja para os domínios do seu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão dos routers para organizar os endpoints
print("--- Incluindo routers na aplicação ---")
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(documents.router)
app.include_router(system.router)
app.include_router(retrievers.router)
app.include_router(pipelines.router)
app.include_router(chat.router)
print("--- Routers incluídos com sucesso ---")


@app.get('/', tags=["Root"], summary="Verificar o status da API")
def read_root():
    """Endpoint raiz que retorna uma mensagem de boas-vindas e o status da API."""
    return {'status': 'API online e funcionando!', 'docs_url': '/docs'}
