import logging
from memory.memory_handler import get_session_history
from .handler import (
    create_pipeline_with_separated_vectorstores,
    create_pipeline_single_vectorstore,
)
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


def get_response_stream(question: str, session_id: str):
    logging.debug(
        f'Iniciando processamento para a pergunta: {question} | Sessão: {session_id}'
    )
    pipeline = create_pipeline_with_separated_vectorstores()
    history = get_session_history(session_id)
    try:
        response = pipeline.stream(
            {'pergunta': question, 'memoria': history.messages},
            config={'configurable': {'session_id': session_id}},
        )
        logging.debug(f'Processamento concluído para a sessão: {session_id}')
        return response
    except Exception as e:
        logging.error(f'[ERROR] Falha ao processar a pergunta: {str(e)}')
        return None


def get_response_stream_single_vectorstore(
    question: str, session_id: str, vectorstore: str
):
    logging.debug(
        f'Iniciando processamento filtrado para a pergunta: {question} | Sessão: {session_id}, Vectorstore: {vectorstore}'
    )
    pipeline = create_pipeline_single_vectorstore(vectorstore)
    history = get_session_history(session_id)
    try:
        response = pipeline.stream(
            {'pergunta': question, 'memoria': history.messages},
            config={'configurable': {'session_id': session_id}},
        )
        logging.debug(
            f'Processamento filtrado concluído para a sessão: {session_id}'
        )
        return response
    except Exception as e:
        logging.error(
            f'[ERROR] Falha ao processar a pergunta filtrada: {str(e)}'
        )
        return None
