from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from retriever.retrievers import (
    get_iniciativas_retriever,
    get_iesgo_retriever,
    get_imgg_retriever,
    get_indicadores_retriever,
    get_diagnostico_imgg_retriever
)
from prompt.prompt_template import prompt_template_with_memory
from memory.memory_handler import get_session_history, save_session_history

def create_pipeline_with_separated_vectorstores():
    """
    Cria o pipeline principal que combina múltiplos retrievers para contextos separados e
    gera respostas com base em um modelo de linguagem.
    """
    # Instanciar os retrievers
    iniciativas_retriever = get_iniciativas_retriever()
    iesgo_retriever = get_iesgo_retriever()
    imgg_retriever = get_imgg_retriever()
    indicadores_retriever = get_indicadores_retriever()
    diagnostico_imgg = get_diagnostico_imgg_retriever()

    # Preparação de conteúdos de diferentes retrievers
    content_preparation = RunnableParallel({
        'pergunta': lambda x: x['pergunta'],
        'iniciativas_contexto': lambda x: iniciativas_retriever.invoke(x['pergunta']),
        'iesgo_contexto': lambda x: iesgo_retriever.invoke(x['pergunta']),
        'imgg_contexto': lambda x: imgg_retriever.invoke(x['pergunta']),
        'indicadores_contexto': lambda x: indicadores_retriever.invoke(x['pergunta']),
        'diagnostico_imgg': lambda x: diagnostico_imgg.invoke(x['pergunta']),
        'memoria': lambda x: x['memoria'],
    })

    # Combinar os contextos em uma única entrada para o modelo
    combine_contexts = (
        content_preparation
        | (lambda inputs: {
            "pergunta": inputs["pergunta"],
            "contexto": "\n\n".join([
                "\n".join(doc.page_content for doc in inputs["iniciativas_contexto"]),
                "\n".join(doc.page_content for doc in inputs["iesgo_contexto"]),
                "\n".join(doc.page_content for doc in inputs["imgg_contexto"]),
                "\n".join(doc.page_content for doc in inputs["indicadores_contexto"]),
                "\n".join(doc.page_content for doc in inputs["diagnostico_imgg"]),
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
            max_tokens=7000,
            model_kwargs={"stream": True},
            request_timeout=300
        )
        | StrOutputParser()
    )

    # Adicionar histórico de mensagens ao pipeline
    return RunnableWithMessageHistory(
        core_rag_chain,
        get_session_history,
        input_messages_key='pergunta',
        history_messages_key='memoria',
        save_history=save_session_history
    )


def get_response_stream(question: str, session_id: str):
    print(f"[DEBUG] Iniciando processamento para a pergunta: {question} | Sessão: {session_id}")

    # Criar o pipeline principal
    pipeline = create_pipeline_with_separated_vectorstores()

    # Recuperar histórico da sessão
    history = get_session_history(session_id)

    # Processar a entrada e gerar resposta
    response = pipeline.stream(
        {'pergunta': question, 'memoria': history.messages},
        config={'configurable': {'session_id': session_id}}
    )

    print(f"[DEBUG] Processamento concluído para a sessão: {session_id}")
    return response