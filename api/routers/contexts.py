from fastapi import APIRouter, Depends, status
from api.schemas.context import ContextCreate
from api.keycloak import get_current_user

router = APIRouter(prefix="/contexts", tags=["Contexts"])

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo contexto para IA",
    description="Cria um novo contexto para a IA. Protegido por JWT.\n\nExemplo de payload:\n```json\n{\n  \"nome\": \"Contexto de Teste\",\n  \"descricao\": \"Contexto para testes de integração\",\n  \"dados\": {\"chave\": \"valor\"}\n}\n```\nRespostas de erro: 401 (não autenticado), 422 (payload inválido)."
)
def create_context(context: ContextCreate, user=Depends(get_current_user)):
    """
    Cria um novo contexto para a IA.
    - Protegido por JWT.
    - Exemplo de payload:
      {
        "nome": "Contexto de Teste",
        "descricao": "Contexto para testes de integração",
        "dados": {"chave": "valor"}
      }
    - Respostas de erro: 401 (não autenticado), 422 (payload inválido).
    """
    return {"msg": "Contexto criado com sucesso", "context": context, "user": user["sub"]}