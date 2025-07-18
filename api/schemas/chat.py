from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    pergunta: str = Field(..., description="A pergunta do usuário para o chatbot.")
    session_id: str = Field(..., description="O ID da sessão para manter o histórico da conversa.")

class ChatResponse(BaseModel):
    resposta: str
    session_id: str