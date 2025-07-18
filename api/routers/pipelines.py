from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas.pipeline import (
    AllPipelineConfigsResponse,
    PipelineConfig,
    PipelineConfigUpdate,
    PipelineName,
)
from ..dependencies import get_current_admin_user
from ..crud import pipeline_crud

router = APIRouter(
    prefix="/pipelines",
    tags=["Pipelines"],
    dependencies=[Depends(get_current_admin_user)],
)

@router.get(
    "/configurations",
    response_model=AllPipelineConfigsResponse,
    summary="Listar configurações de todos os pipelines (Admin Only)",
)
def get_pipeline_configurations():
    configs = pipeline_crud.get_all_configs()
    return AllPipelineConfigsResponse(configurations=configs)

@router.get(
    "/configurations/{pipeline_name}",
    response_model=PipelineConfig,
    summary="Obter configuração de um pipeline específico (Admin Only)",
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
    summary="Atualizar a configuração de um pipeline (Admin Only)",
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