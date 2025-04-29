from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from database.vectorstore_handler import get_vectorstore
from memory.memory_handler import get_session_history, save_session_history
from prompt.prompt_template import prompt_template_with_memory
from config.utils import join_documents

def create_pipeline_with_memory():
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_type='similarity', search_kwargs={'k': 18, 'fetch_k': 22})

    rag_chain_content_preparation = RunnableParallel({
        'pergunta': lambda x: x['pergunta'],
        'contexto': lambda x: join_documents({'contexto': retriever.invoke(x['pergunta'])}),
        'memoria': lambda x: x['memoria']
    })

    core_rag_chain = (
        rag_chain_content_preparation
        | prompt_template_with_memory
        | ChatOpenAI(model='gpt-4o-mini', temperature=0.2, max_tokens=5500, model_kwargs={"stream": True})
        | StrOutputParser()
    )

    return RunnableWithMessageHistory(
        core_rag_chain,
        get_session_history,
        input_messages_key='pergunta',
        history_messages_key='memoria',
        save_history=save_session_history
    )

def get_response_stream(question: str, session_id: str):
    print(f"[DEBUG] Iniciando processamento para a pergunta: {question} | Sessão: {session_id}")
    chain = create_pipeline_with_memory()
    response = chain.stream({'pergunta': question, 'memoria': []}, config={'configurable': {'session_id': session_id}})
    print(f"[DEBUG] Processamento concluído para a sessão: {session_id}")
    return response