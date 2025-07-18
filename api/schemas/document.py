from pydantic import BaseModel, Field
from typing import List

class Document(BaseModel):
    file_name: str = Field(..., description="Nome do arquivo do documento (ex: 'iniciativas.md').")
    content: str = Field(..., description="Conteúdo completo do arquivo Markdown.")

class DocumentMetadata(BaseModel):
    file_name: str

class DocumentListResponse(BaseModel):
    documents: List[DocumentMetadata]