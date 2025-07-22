from fastapi import APIRouter, Depends, HTTPException, status
from langchain_core.runnables.base import Runnable
from ..schemas.chat import ChatRequest, ChatResponse
from api.keycloak import get_current_user
from ..schemas.user import User
from ..dependencies import get_active_pipeline, get_current_active_user

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
    dependencies=[Depends(get_current_user)]
)

@router.post(
    "/multi",
    response_model=ChatResponse,
    summary="Conversar com a IA utilizando todos os Vectorstores",
    description="Envia uma pergunta para a IA, utilizando todos os vectorstores configurados. Protegido por JWT. Retorna a resposta da IA e o session_id.\n\nExemplo de payload:\n```json\n{\n  \"pergunta\": \"Quais são os principais riscos da UGGOV?\",\n  \"session_id\": \"abc123\"\n}\n```\nRespostas de erro: 401 (não autenticado), 500 (erro interno de processamento)."
)
async def chat_with_all_vectorstores(
    request: ChatRequest,
    pipeline_multi_vs: Runnable = Depends(get_active_pipeline),
    current_user: User = Depends(get_current_active_user)
):
    """
    Envia uma pergunta para a IA, utilizando todos os vectorstores configurados.
    - Protegido por JWT.
    - Retorna a resposta da IA e o session_id.
    - Exemplo de payload:
      {
        "pergunta": "Quais são os principais riscos da UGGOV?",
        "session_id": "abc123"
      }
    - Respostas de erro: 401 (não autenticado), 500 (erro interno de processamento).
    """
    try:
        config = {'configurable': {'session_id': request.session_id}}
        response_content = pipeline_multi_vs.invoke(
            {'pergunta': request.pergunta}, config=config
        )
        return ChatResponse(resposta=response_content, session_id=request.session_id)
    except Exception as e:
        print(f"!!! [API CHAT] ERRO DURANTE A INVOCAÇÃO DO PIPELINE: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro interno ao processar sua pergunta: {e}",
        )
