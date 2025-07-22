from fastapi import APIRouter, Depends, HTTPException, status, Body
from api.schemas.prompt import Prompt
from api.crud import prompt_crud
from api.keycloak import require_roles
from prompt.prompt_template import PROMPT_SISTEMA_MTI_FINAL

router = APIRouter(
    prefix="/prompts",
    tags=["Prompt Management"],
    dependencies=[Depends(require_roles("admin"))],
)

@router.post(
    "/",
    response_model=Prompt,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo prompt",
    description="Cria um novo prompt para a IA. Protegido por JWT e role admin.\n\nExemplo de payload:\n```json\n{\n  \"name\": \"resumo_geral\",\n  \"content\": \"Resuma o seguinte texto: {texto}\",\n  \"description\": \"Prompt para resumos gerais.\",\n  \"tags\": [\"resumo\", \"geral\"]\n}\n```\nRespostas de erro: 401 (não autenticado), 403 (sem permissão), 409 (prompt já existe)."
)
def create_new_prompt(prompt_in: Prompt):
    if prompt_crud.get_prompt_by_name(prompt_in.name):
        raise HTTPException(status.HTTP_409_CONFLICT, f"O prompt com o nome '{prompt_in.name}' já existe.")
    return prompt_crud.create_prompt(prompt_in)

@router.put(
    "/{prompt_name}",
    response_model=Prompt,
    summary="Atualizar um prompt",
    description="Atualiza o conteúdo de um prompt, garantindo padrão do template base IA. Protegido por JWT e role admin.\n\nExemplo de payload:\n```json\n{\n  \"content\": \"Novo conteúdo do prompt...\"\n}\n```\nRespostas de erro: 401 (não autenticado), 403 (sem permissão), 404 (prompt não encontrado)."
)
def update_prompt(prompt_name: str, prompt_update: dict = Body(...)):
    updated = prompt_crud.update_prompt(prompt_name, prompt_update, template_base=PROMPT_SISTEMA_MTI_FINAL)
    if not updated:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Prompt '{prompt_name}' não encontrado.")
    return updated 