from fastapi import APIRouter, Depends, status, BackgroundTasks
from ..schemas.system import ReindexResponse
from ..dependencies import get_current_admin_user, get_pipeline_multi_vs
from database.ingestion import process_and_ingest_documents
from retriever.retrievers import _retriever_cache

router = APIRouter(
    prefix="/system",
    tags=["System Operations"],
    dependencies=[Depends(get_current_admin_user)],
)

def reindex_and_clear_caches():
    print("--- INICIANDO TAREFA DE REINDEXAÇÃO EM BACKGROUND ---")
    process_and_ingest_documents()
    print("--- TAREFA DE INGESTÃO CONCLUÍDA ---")

    print("🧹 Limpando caches da API em memória...")
    _retriever_cache.clear()
    get_pipeline_multi_vs.cache_clear()
    print("✅ Caches limpos. A API usará os novos dados na próxima requisição.")
    print("--- TAREFA DE REINDEXAÇÃO EM BACKGROUND CONCLUÍDA ---")


@router.post(
    "/reindex",
    response_model=ReindexResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Disparar a reindexação da base de conhecimento",
    description="""
    Dispara um processo assíncrono em background para recriar todos os vectorstores
    a partir dos arquivos encontrados no diretório `/documentation`.

    Este processo pode ser demorado. A API responderá imediatamente com um status
    de 'aceito', e a reindexação ocorrerá em segundo plano.

    **Este é o passo crucial após adicionar ou remover um documento para que a IA
    se torne ciente da mudança.**

    - **Acesso**: Apenas Administradores.
    """,
)
def trigger_reindexing(background_tasks: BackgroundTasks):
    print("⚡ Endpoint de reindexação acionado. Adicionando tarefa em background.")
    background_tasks.add_task(reindex_and_clear_caches)
    
    return {
        "status": "accepted",
        "message": "O processo de reindexação foi iniciado em segundo plano. Verifique os logs do servidor para acompanhar o progresso."
    }