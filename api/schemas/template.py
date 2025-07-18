from pydantic import BaseModel, Field
from typing import Optional

class Template(BaseModel):
    """Schema para um template."""
    name: str = Field(..., description="Nome único do template.", example="resumo_tecnico")
    content: str = Field(..., description="O conteúdo do template.", example="Resuma o seguinte texto: {texto}")
    description: Optional[str] = Field(None, description="Descrição opcional do propósito do template.", example="Template para resumos técnicos.")

class TemplateUpdate(BaseModel):
    """Schema para atualizar um template. Todos os campos são opcionais."""
    content: Optional[str] = None
    description: Optional[str] = None