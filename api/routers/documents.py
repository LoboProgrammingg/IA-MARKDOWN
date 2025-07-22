import os
from fastapi import APIRouter, HTTPException, status, Body
from typing import List
from ..schemas.document import Document, DocumentListResponse, DocumentMetadata
from api.keycloak import get_current_user
from fastapi import Depends

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

DOCUMENTATION_PATH = "./documentation/"

@router.get(
    "/",
    response_model=DocumentListResponse,
    summary="Listar todos os documentos",
    description="Lista todos os documentos markdown disponíveis. Protegido por JWT. Respostas de erro: 401 (não autenticado), 404 (diretório não encontrado)."
)
def list_documents(user=Depends(get_current_user)):
    try:
        files = [f for f in os.listdir(DOCUMENTATION_PATH) if f.endswith('.md')]
        document_metadata = [{"file_name": f} for f in files]
        return {"documents": document_metadata}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Diretório de documentação não encontrado.")

@router.get(
    "/{file_name}",
    response_model=Document,
    summary="Obter um documento específico",
    description="Obtém o conteúdo de um documento markdown pelo nome do arquivo. Protegido por JWT. Respostas de erro: 401 (não autenticado), 404 (documento não encontrado)."
)
def get_document(file_name: str, user=Depends(get_current_user)):
    file_path = os.path.join(DOCUMENTATION_PATH, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Documento não encontrado.")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return {"file_name": file_name, "content": content}

@router.post(
    "/",
    response_model=Document,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo documento",
    description="Cria um novo documento markdown. Protegido por JWT. Respostas de erro: 401 (não autenticado), 409 (documento já existe).\n\nExemplo de payload:\n```json\n{\n  \"file_name\": \"exemplo.md\",\n  \"content\": \"Conteúdo do documento...\"\n}\n```"
)
def create_document(doc: Document, user=Depends(get_current_user)):
    file_path = os.path.join(DOCUMENTATION_PATH, doc.file_name)
    if os.path.exists(file_path):
        raise HTTPException(status_code=409, detail="Documento com este nome já existe.")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(doc.content)
    return doc

@router.put(
    "/{file_name}",
    response_model=Document,
    summary="Atualizar um documento existente",
    description="Atualiza o conteúdo de um documento markdown existente. Protegido por JWT. Respostas de erro: 401 (não autenticado), 404 (documento não encontrado)."
)
def update_document(file_name: str, content: str = Body(..., embed=True), user=Depends(get_current_user)):
    file_path = os.path.join(DOCUMENTATION_PATH, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return {"file_name": file_name, "content": content}

@router.delete(
    "/{file_name}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar um documento",
    description="Remove um documento markdown pelo nome do arquivo. Protegido por JWT. Respostas de erro: 401 (não autenticado), 404 (documento não encontrado)."
)
def delete_document(file_name: str, user=Depends(get_current_user)):
    file_path = os.path.join(DOCUMENTATION_PATH, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Documento não encontrado.")
    os.remove(file_path)
    return None