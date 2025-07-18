import json
import os
from typing import Dict, Any

CONFIG_FILE_PATH = "pipeline_configs.json"

# Configurações padrão para os pipelines
DEFAULT_PIPELINE_CONFIGS = {
    "multi_vectorstore": {
        "model": "gemini-2.5-pro",
        "temperature": 0.2,
        "max_output_tokens": 64000,
        "thinking_budget": 2000
    },
    "single_vectorstore": {
        "model": "gemini-1.5-pro",
        "temperature": 0.3,
        "max_output_tokens": 8192,
        "thinking_budget": 3300
    }
}

# Cache em memória para as configurações
_current_configs: Dict[str, Any] = {}

def load_configurations():
    """
    Carrega as configurações do pipeline do arquivo JSON para o cache em memória.
    Se o arquivo não existir, ele o cria a partir dos valores padrão.
    """
    global _current_configs
    if os.path.exists(CONFIG_FILE_PATH):
        try:
            with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
                _current_configs = json.load(f)
            print(f"✅ Configurações do pipeline carregadas de '{CONFIG_FILE_PATH}'.")
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️ Erro ao ler '{CONFIG_FILE_PATH}': {e}. Carregando configurações padrão.")
            _current_configs = DEFAULT_PIPELINE_CONFIGS
            save_configurations()
    else:
        print(f"ℹ️ Arquivo '{CONFIG_FILE_PATH}' não encontrado. Criando com configurações padrão.")
        _current_configs = DEFAULT_PIPELINE_CONFIGS
        save_configurations()

def save_configurations():
    """Salva as configurações atuais em memória no arquivo JSON."""
    try:
        with open(CONFIG_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(_current_configs, f, indent=4, ensure_ascii=False)
        print(f"💾 Configurações do pipeline salvas em '{CONFIG_FILE_PATH}'.")
    except IOError as e:
        print(f"❌ Erro crítico ao salvar configurações em '{CONFIG_FILE_PATH}': {e}")

def get_configurations() -> Dict[str, Any]:
    """Retorna todas as configurações de pipeline atuais."""
    return _current_configs

def get_configuration(pipeline_name: str) -> Dict[str, Any]:
    """Retorna a configuração para um pipeline específico."""
    return _current_configs.get(pipeline_name)

def update_configuration(pipeline_name: str, new_config_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Atualiza a configuração para um pipeline específico e a salva no arquivo.
    """
    if pipeline_name not in _current_configs:
        return None
    
    _current_configs[pipeline_name].update(new_config_data)
    save_configurations()
    return _current_configs[pipeline_name]