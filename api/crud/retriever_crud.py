from typing import Dict, Optional, Callable
from retriever import config_manager
from retriever.section import Section
from retriever.default_configs import DEFAULT_RETRIEVER_CONFIGS
from ..schemas.retriever import RetrieverConfig, RetrieverConfigUpdate

def get_all_configs() -> Dict[Section, RetrieverConfig]:
    raw_configs = config_manager.get_configurations()
    return {Section[key]: RetrieverConfig(**value) for key, value in raw_configs.items()}

def get_config_by_section(section: Section) -> Optional[RetrieverConfig]:
    config_dict = config_manager.get_configuration(section)
    if config_dict:
        return RetrieverConfig(**config_dict)
    return None

def get_vectorstore_getter(section: Section) -> Optional[Callable]:
    if section in DEFAULT_RETRIEVER_CONFIGS:
        return DEFAULT_RETRIEVER_CONFIGS[section][0]
    return None

def update_config(section: Section, new_config: RetrieverConfigUpdate) -> RetrieverConfig:
    update_data = new_config.model_dump(exclude_unset=True)
    updated_config_dict = config_manager.update_configuration(section, update_data)
    if updated_config_dict:
        return RetrieverConfig(**updated_config_dict)
    return None