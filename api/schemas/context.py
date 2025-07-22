from pydantic import BaseModel, Field
from typing import Dict, Any

class ContextCreate(BaseModel):
    nome: str = Field(..., description="Nome do contexto")
    descricao: str = Field(..., description="Descrição do contexto")
    dados: Dict[str, Any] = Field(..., description="Dados do contexto (livre)") 