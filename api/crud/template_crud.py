import json
from typing import List, Optional
from ..schemas.template import Template, TemplateUpdate

TEMPLATES_FILE = "templates.json"
_templates_cache: dict[str, Template] = {}

def _load_templates():
    """Carrega os templates do arquivo JSON para o cache em memória."""
    global _templates_cache
    try:
        with open(TEMPLATES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            _templates_cache = {item['name']: Template(**item) for item in data}
        print(f"✅ Templates carregados de '{TEMPLATES_FILE}'.")
    except (FileNotFoundError, json.JSONDecodeError):
        _templates_cache = {}
        print(f"ℹ️ Arquivo '{TEMPLATES_FILE}' não encontrado ou vazio. Iniciando com cache limpo.")

def _save_templates():
    with open(TEMPLATES_FILE, 'w', encoding='utf-8') as f:
        json.dump([template.model_dump() for template in _templates_cache.values()], f, indent=4, ensure_ascii=False)

_load_templates()

def get_all_templates() -> List[Template]:
    return list(_templates_cache.values())

def get_template_by_name(name: str) -> Optional[Template]:
    return _templates_cache.get(name)

def create_template(template_in: Template) -> Template:
    _templates_cache[template_in.name] = template_in
    _save_templates()
    return template_in

def update_template(name: str, template_update: TemplateUpdate) -> Optional[Template]:
    existing_template = _templates_cache.get(name)
    if not existing_template:
        return None
    
    update_data = template_update.model_dump(exclude_unset=True)
    updated_template = existing_template.model_copy(update=update_data)
    _templates_cache[name] = updated_template
    _save_templates()
    return updated_template

def delete_template(name: str) -> bool:
    if name in _templates_cache:
        del _templates_cache[name]
        _save_templates()
        return True
    return False