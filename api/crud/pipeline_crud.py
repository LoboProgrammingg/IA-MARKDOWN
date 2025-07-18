from typing import Dict, Optional
from pipeline import config_manager
from ..schemas.pipeline import PipelineConfig, PipelineConfigUpdate, PipelineName

def get_all_configs() -> Dict[PipelineName, PipelineConfig]:
    raw_configs = config_manager.get_configurations()
    return {PipelineName(key): PipelineConfig(**value) for key, value in raw_configs.items()}

def get_config_by_name(pipeline_name: PipelineName) -> Optional[PipelineConfig]:
    config_dict = config_manager.get_configuration(pipeline_name.value)
    if config_dict:
        return PipelineConfig(**config_dict)
    return None

def update_config(pipeline_name: PipelineName, new_config: PipelineConfigUpdate) -> PipelineConfig:
    update_data = new_config.model_dump(exclude_unset=True)
    updated_config_dict = config_manager.update_configuration(pipeline_name.value, update_data)
    if updated_config_dict:
        return PipelineConfig(**updated_config_dict)
    return None