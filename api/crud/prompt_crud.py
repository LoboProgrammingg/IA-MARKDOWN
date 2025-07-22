import json
from typing import List, Optional
from ..schemas.prompt import Prompt

PROMPTS_FILE = "prompts.json"
_prompts_cache: dict[str, Prompt] = {}

def _load_prompts():
    global _prompts_cache
    try:
        with open(PROMPTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            _prompts_cache = {item['name']: Prompt(**item) for item in data}
    except (FileNotFoundError, json.JSONDecodeError):
        _prompts_cache = {}

def _save_prompts():
    with open(PROMPTS_FILE, 'w', encoding='utf-8') as f:
        json.dump([prompt.model_dump() for prompt in _prompts_cache.values()], f, indent=4, ensure_ascii=False)

_load_prompts()

def get_all_prompts() -> List[Prompt]:
    return list(_prompts_cache.values())

def get_prompt_by_name(name: str) -> Optional[Prompt]:
    return _prompts_cache.get(name)

def create_prompt(prompt_in: Prompt) -> Prompt:
    _prompts_cache[prompt_in.name] = prompt_in
    _save_prompts()
    return prompt_in

def delete_prompt(name: str) -> bool:
    if name in _prompts_cache:
        del _prompts_cache[name]
        _save_prompts()
        return True
    return False

def update_prompt(name: str, prompt_update: dict, template_base: str = None):
    existing_prompt = _prompts_cache.get(name)
    if not existing_prompt:
        return None
    update_data = prompt_update.copy()
    # Se atualizar o content, garantir que inclui o template base
    if "content" in update_data and template_base:
        if template_base not in update_data["content"]:
            update_data["content"] = template_base + "\n" + update_data["content"]
    updated_prompt = existing_prompt.model_copy(update=update_data)
    _prompts_cache[name] = updated_prompt
    _save_prompts()
    return updated_prompt 