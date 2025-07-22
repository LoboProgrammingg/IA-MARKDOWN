from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas.pipeline import (
    AllPipelineConfigsResponse,
    PipelineConfig,
    PipelineConfigUpdate,
    PipelineName,
)
from ..crud import pipeline_crud
from api.keycloak import require_roles

router = APIRouter(
    prefix="/pipelines",
    tags=["Pipelines"],
    dependencies=[Depends(require_roles("admin"))],
)

@router.get(
    "/configurations",
    response_model=AllPipelineConfigsResponse,
    summary="Listar configurações de todos os pipelines",
    description="Lista todas as configurações de pipelines disponíveis. Protegido por JWT e requer role 'admin'. Respostas de erro: 401 (não autenticado), 403 (sem permissão)."
)
def get_pipeline_configurations():
    configs = pipeline_crud.get_all_configs()
    return AllPipelineConfigsResponse(configurations=configs)

@router.get(
    "/configurations/{pipeline_name}",
    response_model=PipelineConfig,
    summary="Obter configuração de um pipeline específico",
    description="Obtém a configuração de um pipeline pelo nome. Protegido por JWT e requer role 'admin'. Respostas de erro: 401 (não autenticado), 403 (sem permissão), 404 (pipeline não encontrado)."
)
def get_single_pipeline_configuration(pipeline_name: PipelineName):
    config = pipeline_crud.get_config_by_name(pipeline_name)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Configuração para o pipeline '{pipeline_name.value}' não encontrada.",
        )
    return config

@router.put(
    "/configurations/{pipeline_name}",
    response_model=PipelineConfig,
    summary="Atualizar a configuração de um pipeline",
    description="Atualiza a configuração de um pipeline pelo nome. Protegido por JWT e requer role 'admin'. Respostas de erro: 401 (não autenticado), 403 (sem permissão), 404 (pipeline não encontrado)."
)
def update_pipeline_configuration(
    pipeline_name: PipelineName,
    config_in: PipelineConfigUpdate,
):
    updated_config = pipeline_crud.update_config(pipeline_name, config_in)
    if not updated_config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Configuração para o pipeline '{pipeline_name.value}' não encontrada.",
        )
    return updated_config