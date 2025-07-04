import uvicorn
from fastapi import FastAPI, HTTPException, Path, Form
from pydantic import BaseModel
from typing import List

from fastapi.middleware.cors import CORSMiddleware

from pipeline.handler import (
    create_pipeline_with_separated_vectorstores,
    create_pipeline_single_vectorstore,
)

app = FastAPI(
    title='API do Chatbot com RAG',
    description='Uma API para interagir com um sistema de IA que utiliza múltiplos Vectorstores.',
    version='3.0.0',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


class ChatResponse(BaseModel):
    resposta: str
    session_id: str


try:
    pipeline_multi_vs = create_pipeline_with_separated_vectorstores()
    print('✅ Pipeline com múltiplos vectorstores carregado com sucesso.')
except Exception as e:
    print(f'❌ Erro ao carregar o pipeline multi-vectorstore: {e}')
    pipeline_multi_vs = None


@app.get('/', summary='Endpoint raiz para verificar o status da API')
def read_root():
    return {'status': 'API online e funcionando!'}


@app.post(
    '/chat/multi',
    response_model=ChatResponse,
    summary='Conversar usando todos os Vectorstores',
)
async def chat_with_all_vectorstores(
    pergunta: str = Form(...), session_id: str = Form(...)
):
    if not pipeline_multi_vs:
        raise HTTPException(
            status_code=500,
            detail='Pipeline principal não foi inicializado corretamente.',
        )

    try:
        config = {'configurable': {'session_id': session_id}}

        response_content = pipeline_multi_vs.invoke(
            {'pergunta': pergunta}, config=config
        )

        return ChatResponse(resposta=response_content, session_id=session_id)
    except Exception as e:
        print(f'!!! [FASTAPI] ERRO DURANTE A INVOCAÇÃO DO PIPELINE: {e}')
        raise HTTPException(
            status_code=500,
            detail=f'Ocorreu um erro ao processar sua pergunta na API: {e}',
        )


if __name__ == '__main__':
    uvicorn.run('main_api:app', host='0.0.0.0', port=8001, reload=True)

# API