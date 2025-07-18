from pydantic import BaseModel, Field
from typing import Dict, Optional, List, Any
from retriever.section import Section

class RetrieverConfigBase(BaseModel):
    search_type: str = Field(description="Tipo de busca (ex: 'mmr', 'similarity').")
    k: int = Field(description="Número de documentos a serem retornados no final.")
    fetch_k: int = Field(description="Número de documentos a serem buscados inicialmente.")
    rerank_top_n: int = Field(description="Número de documentos para o reranker.")
    use_reranker: bool = Field(description="Opção de usar ou não o reranker.")

class RetrieverConfig(RetrieverConfigBase):
    pass

class RetrieverConfigUpdate(BaseModel):
    search_type: Optional[str] = None
    k: Optional[int] = None
    fetch_k: Optional[int] = None
    rerank_top_n: Optional[int] = None
    use_reranker: Optional[bool] = None

class AllRetrieverConfigsResponse(BaseModel):
    configurations: Dict[Section, RetrieverConfig]