import json
import os
from typing import Dict, Any
from .default_configs import DEFAULT_RETRIEVER_CONFIGS # CORREÇÃO: Importa do novo arquivo
from .section import Section

CONFIG_FILE_PATH = "retriever_configs.json"

# Cache em memória para as configurações
_current_configs: Dict[str, Any] = {}

def _get_default_configs_as_dict() -> Dict[str, Any]:
    """Converte a estrutura de tupla de configuração padrão em um dicionário simples."""
    defaults = {}
    for section, config_tuple in DEFAULT_RETRIEVER_CONFIGS.items():
        # A chave da seção deve ser uma string para compatibilidade com JSON
        defaults[section.name] = config_tuple[1]
    return defaults

def load_configurations():
    """
    Carrega as configurações do arquivo JSON para o cache em memória.
    Se o arquivo não existir, ele o cria a partir dos valores padrão.
    """
    global _current_configs
    if os.path.exists(CONFIG_FILE_PATH):
        try:
            with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
                _current_configs = json.load(f)
            print(f"✅ Configurações do retriever carregadas de '{CONFIG_FILE_PATH}'.")
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️ Erro ao ler '{CONFIG_FILE_PATH}': {e}. Carregando configurações padrão.")
            _current_configs = _get_default_configs_as_dict()
            save_configurations()
    else:
        print(f"ℹ️ Arquivo '{CONFIG_FILE_PATH}' não encontrado. Criando com configurações padrão.")
        _current_configs = _get_default_configs_as_dict()
        save_configurations()

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
    
    # Atualiza apenas as chaves fornecidas
    _current_configs[section.name].update(new_config_data)
    save_configurations()
    return _current_configs[section.name]
