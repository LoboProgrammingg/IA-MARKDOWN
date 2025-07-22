from pydantic import BaseModel, Field
from typing import Optional, List

class Prompt(BaseModel):
    name: str = Field(..., description="Nome único do prompt.", example="resumo_geral")
    content: str = Field(..., description="Conteúdo do prompt.", example="Resuma o seguinte texto: {texto}")
    description: Optional[str] = Field(None, description="Descrição opcional do prompt.", example="Prompt para resumos gerais.")
    tags: Optional[List[str]] = Field(None, description="Tags para organização do prompt.", example=["resumo", "geral"]) 