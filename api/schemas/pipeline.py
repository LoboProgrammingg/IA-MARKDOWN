from pydantic import BaseModel, Field
from typing import Dict, Optional
from enum import Enum

class PipelineName(str, Enum):
    MULTI_VECTORSTORE = "multi_vectorstore"
    SINGLE_VECTORSTORE = "single_vectorstore"

class PipelineConfig(BaseModel):
    model: str = Field(description="O nome do modelo de linguagem a ser usado.")
    temperature: float = Field(description="A temperatura para a geração de texto (criatividade).")
    max_output_tokens: int = Field(description="O número máximo de tokens na resposta.")
    thinking_budget: int = Field(description="O orçamento de 'pensamento' para o modelo.")

class PipelineConfigUpdate(BaseModel):
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_output_tokens: Optional[int] = None
    thinking_budget: Optional[int] = None

class AllPipelineConfigsResponse(BaseModel):
    configurations: Dict[PipelineName, PipelineConfig]