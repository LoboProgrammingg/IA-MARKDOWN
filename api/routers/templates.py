from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..schemas.template import Template, TemplateUpdate
from ..crud import template_crud
from api.keycloak import require_roles

router = APIRouter(
    prefix="/templates",
    tags=["Template Management"],
    dependencies=[Depends(require_roles("admin"))], # Apenas admins podem gerenciar templates
)

@router.get(
    "/",
    response_model=List[Template],
    summary="Listar todos os templates",
    description="Lista todos os templates configurados no sistema. Protegido por JWT e requer role 'admin'. Respostas de erro: 401 (não autenticado), 403 (sem permissão)."
)
def get_all_templates():
    """Retorna uma lista de todos os templates configurados no sistema."""
    return template_crud.get_all_templates()

@router.post(
    "/",
    response_model=Template,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo template",
    description="Cria um novo template para a IA. Protegido por JWT e role admin.\n\nExemplo de payload:\n```json\n{\n  \"name\": \"resumo_tecnico\",\n  \"content\": \"Resuma o seguinte texto: {texto}\",\n  \"description\": \"Template para resumos técnicos.\"\n}\n```\nRespostas de erro: 401 (não autenticado), 403 (sem permissão), 409 (template já existe)."
)
def create_new_template(template_in: Template):
    """Cria um novo template e o salva no arquivo de configuração."""
    if template_crud.get_template_by_name(template_in.name):
        raise HTTPException(status.HTTP_409_CONFLICT, f"O template com o nome '{template_in.name}' já existe.")
    return template_crud.create_template(template_in)

@router.put(
    "/{template_name}",
    response_model=Template,
    summary="Atualizar um template",
    description="Atualiza o conteúdo ou a descrição de um template existente. Protegido por JWT e role admin.\n\nExemplo de payload:\n```json\n{\n  \"content\": \"Novo conteúdo do template...\",\n  \"description\": \"Nova descrição...\"\n}\n```\nRespostas de erro: 401 (não autenticado), 403 (sem permissão), 404 (template não encontrado)."
)
def update_existing_template(template_name: str, template_update: TemplateUpdate):
    """Atualiza o conteúdo ou a descrição de um template existente."""
    updated_template = template_crud.update_template(template_name, template_update)
    if not updated_template:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Template '{template_name}' não encontrado.")
    return updated_template

@router.delete(
    "/{template_name}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar um template",
    description="Remove um template do sistema pelo nome. Protegido por JWT e role admin. Respostas de erro: 401 (não autenticado), 403 (sem permissão), 404 (template não encontrado)."
)
def delete_existing_template(template_name: str):
    """Remove um template do sistema."""
    if not template_crud.delete_template(template_name):
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Template '{template_name}' não encontrado.")
    return