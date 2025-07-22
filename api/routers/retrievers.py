from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas.retriever import (
    AllRetrieverConfigsResponse,
    RetrieverConfig,
    RetrieverConfigUpdate,
)
from ..crud import retriever_crud
from retriever.retrievers import _retriever_cache
from retriever.section import Section
from api.keycloak import require_roles

router = APIRouter(
    prefix="/retrievers",
    tags=["Retrievers"],
    dependencies=[Depends(require_roles("admin"))],
)

@router.put(
    "/configurations/{section}",
    response_model=RetrieverConfig,
    summary="Atualizar a configuração de um retriever",
    description="Atualiza a configuração de um retriever para uma seção específica. Protegido por JWT e requer role 'admin'. Respostas de erro: 401 (não autenticado), 403 (sem permissão), 404 (seção não encontrada)."
)
def update_retriever_configuration(
    section: Section,
    config_in: RetrieverConfigUpdate,
):
    updated_config = retriever_crud.update_config(section, config_in)
    if not updated_config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Configuração para a seção '{section.value}' não encontrada.",
        )
    
    if section in _retriever_cache:
        del _retriever_cache[section]
        print(f"ℹ️ Cache do retriever para a seção '{section.name}' invalidado.")
        
    return updated_config

@router.get(
    "/configurations",
    response_model=AllRetrieverConfigsResponse,
    summary="Listar configurações de todos os retrievers",
    description="Lista todas as configurações de retrievers disponíveis. Protegido por JWT e requer role 'admin'. Respostas de erro: 401 (não autenticado), 403 (sem permissão)."
)
def get_retriever_configurations():
    configs = retriever_crud.get_all_configs()
    return AllRetrieverConfigsResponse(configurations=configs)

@router.get(
    "/configurations/{section}",
    response_model=RetrieverConfig,
    summary="Obter configuração de um retriever específico",
    description="Obtém a configuração de um retriever para uma seção específica. Protegido por JWT e requer role 'admin'. Respostas de erro: 401 (não autenticado), 403 (sem permissão), 404 (seção não encontrada)."
)
def get_single_retriever_configuration(section: Section):
    config = retriever_crud.get_config_by_section(section)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Configuração para a seção '{section.value}' não encontrada.",
        )
    return config