# retriever/config_manager.py
import json
import os
from typing import Dict, Any
from .default_configs import DEFAULT_RETRIEVER_CONFIGS
from .section import Section

CONFIG_FILE_PATH = "retriever_configs.json"

# Cache em memória para as configurações
_current_configs: Dict[str, Any] = {}

def _get_default_configs_as_dict() -> Dict[str, Any]:
    """Converte a estrutura de tupla de configuração padrão em um dicionário simples."""
    defaults = {}
    for section, config_tuple in DEFAULT_RETRIEVER_CONFIGS.items():
        defaults[section.name] = config_tuple[1]
    return defaults

def load_configurations():
    """
    Carrega as configurações do arquivo JSON e as mescla com as configurações padrão
    para garantir que todos os valores sejam válidos e existentes.
    """
    global _current_configs
    default_configs = _get_default_configs_as_dict()
    
    # Começa com uma cópia completa das configurações padrão como base segura
    _current_configs = default_configs.copy()

    if os.path.exists(CONFIG_FILE_PATH):
        try:
            with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
                loaded_configs = json.load(f)
            
            # Atualiza a base de configurações padrão com os valores do arquivo carregado
            for section_name, loaded_section_config in loaded_configs.items():
                if section_name in _current_configs:
                    # O método .update() sobrescreve as chaves padrão com as do arquivo
                    _current_configs[section_name].update(loaded_section_config)
            
            print(f"✅ Configurações do retriever carregadas e mescladas de '{CONFIG_FILE_PATH}'.")

        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️ Erro ao ler '{CONFIG_FILE_PATH}': {e}. Usando configurações padrão.")
            # _current_configs já está definido com os padrões, então nenhuma ação é necessária
    else:
        print(f"ℹ️ Arquivo '{CONFIG_FILE_PATH}' não encontrado. Criando com configurações padrão.")
        # Salva o arquivo pela primeira vez com as configurações padrão completas
        save_configurations()

    # Etapa final de validação para garantir que valores críticos não sejam inválidos
    for section_name, config in _current_configs.items():
        if config.get("search_type") not in ('similarity', 'mmr', 'similarity_score_threshold'):
            print(f"⚠️ Valor inválido para 'search_type' na seção '{section_name}'. Revertendo para o padrão.")
            config["search_type"] = default_configs[section_name]["search_type"]
        if not isinstance(config.get("k"), int) or config.get("k") <= 0:
            print(f"⚠️ Valor inválido para 'k' na seção '{section_name}'. Revertendo para o padrão.")
            config["k"] = default_configs[section_name]["k"]


def save_configurations():
    """Salva as configurações atuais em memória no arquivo JSON."""
    try:
        with open(CONFIG_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(_current_configs, f, indent=4, ensure_ascii=False)
        print(f"💾 Configurações do retriever salvas em '{CONFIG_FILE_PATH}'.")
    except IOError as e:
        print(f"❌ Erro crítico ao salvar configurações em '{CONFIG_FILE_PATH}': {e}")

def get_configurations() -> Dict[str, Any]:
    """Retorna todas as configurações atuais do cache em memória."""
    return _current_configs

def get_configuration(section: Section) -> Dict[str, Any]:
    """Retorna a configuração para uma seção específica do cache."""
    return _current_configs.get(section.name)

def update_configuration(section: Section, new_config_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Atualiza a configuração para uma seção específica no cache e a salva no arquivo.
    """
    if section.name not in _current_configs:
        return None
    
    _current_configs[section.name].update(new_config_data)
    save_configurations()
    return _current_configs[section.name]
