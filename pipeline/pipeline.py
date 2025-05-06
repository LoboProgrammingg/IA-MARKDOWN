from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from retriever.retrievers import get_iniciativas_retriever, get_iesgo_retriever, get_imgg_retriever
from prompt.prompt_template import prompt_template_with_memory
from memory.memory_handler import get_session_history, save_session_history

def create_pipeline_with_separated_vectorstores():
    iniciativas_retriever = get_iniciativas_retriever()
    iesgo_retriever = get_iesgo_retriever()
    imgg_retriever = get_imgg_retriever()

    content_preparation = RunnableParallel({
        'pergunta': lambda x: x['pergunta'],
        'iniciativas_contexto': lambda x: iniciativas_retriever.get_relevant_documents(x['pergunta']),
        'iesgo_contexto': lambda x: iesgo_retriever.get_relevant_documents(x['pergunta']),
        'imgg_contexto': lambda x: imgg_retriever.get_relevant_documents(x['pergunta']),
        'memoria': lambda x: x['memoria'],
    })

    combine_contexts = (
        content_preparation
        | (lambda inputs: {
            "pergunta": inputs["pergunta"],
            "contexto": "\n\n".join([
                "\n".join(doc.page_content for doc in inputs["iniciativas_contexto"]),
                "\n".join(doc.page_content for doc in inputs["iesgo_contexto"]),
                "\n".join(doc.page_content for doc in inputs["imgg_contexto"]),
            ]),
            "memoria": inputs["memoria"]
        })
    )

    core_rag_chain = (
        combine_contexts
        | prompt_template_with_memory
        | ChatOpenAI(
            model='gpt-4o-mini',
            temperature=0.1,
            max_tokens=4500,
            model_kwargs={"stream": True}
        )
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

    pipeline = create_pipeline_with_separated_vectorstores()

    response = pipeline.stream(
        {'pergunta': question, 'memoria': []},
        config={'configurable': {'session_id': session_id}}
    )

    print(f"[DEBUG] Processamento concluído para a sessão: {session_id}")
    return response
