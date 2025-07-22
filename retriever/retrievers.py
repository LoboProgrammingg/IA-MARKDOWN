from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.retrievers import ContextualCompressionRetriever
from langchain_community.document_compressors.flashrank_rerank import FlashrankRerank

from .section import Section
from . import config_manager
from .default_configs import DEFAULT_RETRIEVER_CONFIGS

prompt_template = PromptTemplate(
    input_variables=['section', 'question', 'connections'],
    template="""\
    Você está lidando com informações relacionadas à seção: {section}.

    Pergunta: {question}

    Conexões relevantes com outros documentos:
    {connections}

    Por favor, forneça uma resposta clara e bem detalhada com base nos dados disponíveis.
    """,
)

def create_retriever(
    vectorstore_getter,
    search_type='mmr',
    k=15,
    fetch_k=50,
    rerank_top_n=10,
    use_reranker=True,
):
    """
    Cria uma instância de retriever (com ou sem reranker) com base nos parâmetros fornecidos.
    """
    vectorstore = vectorstore_getter()
    if vectorstore is None:
        print(
            f'⚠️ Falha ao obter vectorstore para {vectorstore_getter.__name__}. O retriever pode não funcionar.'
        )
        return None

    base_retriever = vectorstore.as_retriever(
        search_type=search_type, search_kwargs={'k': k, 'fetch_k': fetch_k}
    )

    if not use_reranker:
        print(
            f'ℹ️ Re-ranking desabilitado para {vectorstore_getter.__name__}. Usando base_retriever.'
        )
        return base_retriever

    try:
        compressor = FlashrankRerank(top_n=rerank_top_n)
    except Exception as e:
        print(
            f'❌ Falha ao inicializar FlashrankRerank com top_n={rerank_top_n}: {e}. Re-ranking desabilitado.'
        )
        return base_retriever

    return ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=base_retriever
    )

_retriever_cache = {}

def get_retriever(section: Section):
    """
    Obtém uma instância de retriever para a seção especificada, usando a configuração atual.
    Utiliza um cache para evitar a recriação em chamadas subsequentes, a menos que a config mude.
    """
    if section not in _retriever_cache:
        config_data = config_manager.get_configuration(section)
        if not config_data:
            print(f'❌ Configuração de retriever não encontrada para a seção: {section}')
            return None

        if section not in DEFAULT_RETRIEVER_CONFIGS:
            print(f'❌ Getter de vectorstore não encontrado para a seção: {section}')
            return None
        getter = DEFAULT_RETRIEVER_CONFIGS[section][0]

        retriever_instance = create_retriever(getter, **config_data)
        if retriever_instance is None:
            print(f'⚠️ Não foi possível criar o retriever para a seção: {section}')
            return None
        _retriever_cache[section] = retriever_instance
    return _retriever_cache[section]

def fetch_connections(question: str):
    connections = []
    for section_member in Section:
        retriever = get_retriever(section_member)
        if retriever:
            try:
                relevant_docs = retriever.invoke(question)
                if relevant_docs:
                    connections.append(
                        f"Dados relacionados podem existir no vectorstore '{section_member.value}'."
                    )
            except Exception as e:
                print(
                    f"⚠️ Erro ao buscar documentos relevantes para '{section_member.value}': {e}"
                )
    return (
        connections
        if connections
        else [
            'Nenhuma conexão com outros documentos foi identificada como relevante para esta pergunta.'
        ]
    )

def answer_with_connections(section_name: str, question: str, llm_model):
    try:
        section = Section[section_name.upper()]
    except KeyError:
        valid_sections = ', '.join([s.name for s in Section])
        return f"Seção desconhecida: '{section_name}'. Forneça uma seção válida entre: {valid_sections}."

    retriever = get_retriever(section)
    if not retriever:
        return f"Não foi possível carregar o retriever para a seção '{section_name}'."

    connections = fetch_connections(question)
    connections_text = '\n'.join(connections)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm_model,
        retriever=retriever,
        chain_type='stuff',
        chain_type_kwargs={'prompt': prompt_template},
        return_source_documents=True,
    )

    result = qa_chain.invoke(
        {
            'query': question,
            'section': section.value,
            'connections': connections_text,
        }
    )
    return result['result']