from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.retrievers import ContextualCompressionRetriever
from langchain_community.document_compressors.flashrank_rerank import (
    FlashrankRerank,
)

from database.vectorstore_handler import (
    get_iniciativas_vectorstore,
    get_iesgo_vectorstore,
    get_imgg_vectorstore,
    get_indicadores_vectorstore,
    get_diagnostico_imgg_vectorstore,
    get_diagnostico_iesgo_vectorstore,
    get_oms_vectorstore,
    get_padroes_vectorstore,
    get_pta_vectorstore,
    get_riscos_vectorstore,
    get_estatuto_social_vectorstore,
    get_estrutura_processos_vectorstore,
    get_regimento_interno_vectorstore,
    get_gerentes_vectorstore,
)
from .section import Section

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

    print(
        f'ℹ️ Tentando inicializar FlashrankRerank para {vectorstore_getter.__name__} com top_n={rerank_top_n}.'
    )
    try:
        compressor = FlashrankRerank(top_n=rerank_top_n)
    except Exception as e:
        print(
            f'❌ Falha ao inicializar FlashrankRerank com top_n={rerank_top_n}: {e}. Re-ranking desabilitado. Usando base_retriever.'
        )
        return base_retriever

    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=base_retriever
    )
    print(
        f'✅ FlashrankRerank inicializado para {vectorstore_getter.__name__}.'
    )
    return compression_retriever


RETRIEVER_CONFIGS = {
    Section.INICIATIVAS: (
        get_iniciativas_vectorstore,
        dict(
            search_type='mmr',
            k=4,
            fetch_k=18,
            rerank_top_n=2,
            use_reranker=False,
        ),
    ),
    Section.IESGO: (
        get_iesgo_vectorstore,
        dict(
            search_type='mmr',
            k=6,
            fetch_k=25,
            rerank_top_n=3,
            use_reranker=False,
        ),
    ),
    Section.IMGG: (
        get_imgg_vectorstore,
        dict(
            search_type='mmr',
            k=2,
            fetch_k=15,
            rerank_top_n=2,
            use_reranker=False,
        ),
    ),
    Section.INDICADORES: (
        get_indicadores_vectorstore,
        dict(
            search_type='mmr',
            k=4,
            fetch_k=18,
            rerank_top_n=2,
            use_reranker=False,
        ),
    ),
    Section.DIAGNOSTICO_IMGG: (
        get_diagnostico_imgg_vectorstore,
        dict(
            search_type='mmr',
            k=8,
            fetch_k=25,
            rerank_top_n=3,
            use_reranker=False,
        ),
    ),
    Section.DIAGNOSTICO_IESGO: (
        get_diagnostico_iesgo_vectorstore,
        dict(
            search_type='mmr',
            k=8,
            fetch_k=25,
            rerank_top_n=3,
            use_reranker=False,
        ),
    ),
    Section.OMS: (
        get_oms_vectorstore,
        dict(
            search_type='mmr',
            k=4,
            fetch_k=18,
            rerank_top_n=2,
            use_reranker=False,
        ),
    ),
    Section.PADROES: (
        get_padroes_vectorstore,
        dict(
            search_type='mmr',
            k=4,
            fetch_k=18,
            rerank_top_n=2,
            use_reranker=False,
        ),
    ),
    Section.PTA: (
        get_pta_vectorstore,
        dict(
            search_type='mmr',
            k=4,
            fetch_k=18,
            rerank_top_n=2,
            use_reranker=False,
        ),
    ),
    Section.RISCOS: (
        get_riscos_vectorstore,
        dict(
            search_type='mmr',
            k=4,
            fetch_k=18,
            rerank_top_n=2,
            use_reranker=False,
        ),
    ),
    Section.ESTATUTO_SOCIAL: (
        get_estatuto_social_vectorstore,
        dict(
            search_type='mmr',
            k=4,
            fetch_k=10,
            rerank_top_n=3,
            use_reranker=False,
        ),
    ),
    Section.ESTRUTURA_PROCESSOS: (
        get_estrutura_processos_vectorstore,
        dict(
            search_type='mmr',
            k=8,
            fetch_k=25,
            rerank_top_n=3,
            use_reranker=False,
        ),
    ),
    Section.REGIMENTO_INTERNO: (
        get_regimento_interno_vectorstore,
        dict(
            search_type='mmr',
            k=5,
            fetch_k=45,
            rerank_top_n=3,
            use_reranker=False,
        ),
    ),
    Section.GERENTES: (
        get_gerentes_vectorstore,
        dict(
            search_type='mmr',
            k=6,
            fetch_k=24,
            rerank_top_n=3,
            use_reranker=False,
        ),
    ),
}

_retriever_cache = {}


def get_retriever(section: Section):
    if section not in _retriever_cache:
        if section not in RETRIEVER_CONFIGS:
            print(
                f'❌ Configuração de retriever não encontrada para a seção: {section}'
            )
            return None
        getter, kwargs = RETRIEVER_CONFIGS[section]
        retriever_instance = create_retriever(getter, **kwargs)
        if retriever_instance is None:
            print(
                f'⚠️ Não foi possível criar o retriever para a seção: {section}'
            )
            return None
        _retriever_cache[section] = retriever_instance
    return _retriever_cache[section]


def get_iniciativas_retriever():
    return get_retriever(Section.INICIATIVAS)


def get_iesgo_retriever():
    return get_retriever(Section.IESGO)


def get_imgg_retriever():
    return get_retriever(Section.IMGG)


def get_indicadores_retriever():
    return get_retriever(Section.INDICADORES)


def get_diagnostico_imgg_retriever():
    return get_retriever(Section.DIAGNOSTICO_IMGG)


def get_diagnostico_iesgo_retriever():
    return get_retriever(Section.DIAGNOSTICO_IESGO)


def get_oms_retriever():
    return get_retriever(Section.OMS)


def get_padroes_retriever():
    return get_retriever(Section.PADROES)


def get_pta_retriever():
    return get_retriever(Section.PTA)


def get_riscos_retriever():
    return get_retriever(Section.RISCOS)


def get_estatuto_social_retriever():
    return get_retriever(Section.ESTATUTO_SOCIAL)


def get_estrutura_processos_retriever():
    return get_retriever(Section.ESTRUTURA_PROCESSOS)


def get_regimento_interno_retriever():
    return get_retriever(Section.REGIMENTO_INTERNO)


def get_gerentes_retriever():
    return get_retriever(Section.GERENTES)


def fetch_connections(question: str):
    connections = []
    for section_member in Section:
        retriever = get_retriever(section_member)
        if retriever:
            try:
                relevant_docs = retriever.get_relevant_documents(question)
                if relevant_docs:
                    connections.append(
                        f"Dados relacionados podem existir no vectorstore '{section_member.value}'."
                    )
            except Exception as e:
                print(
                    f"⚠️ Erro ao buscar documentos relevantes para '{section_member.value}': {e}"
                )
        else:
            print(
                f"ℹ️ Retriever para '{section_member.value}' não disponível, pulando busca de conexões."
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
        return f"Não foi possível carregar o retriever para a seção '{section_name}'. A resposta não pode ser gerada."

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


if __name__ == '__main__':
    print('🧪 Iniciando teste do módulo retrievers...')

    class MockLLM:
        def invoke(self, input_dict_or_str):
            if isinstance(input_dict_or_str, dict):
                return f"Resposta mock para pergunta sobre a seção: {input_dict_or_str.get('section', 'N/A')}, Contexto: {str(input_dict_or_str.get('context', ''))[:100]}..."
            return f'Resposta mock para: {str(input_dict_or_str)}'

        def __call__(self, input_dict_or_str):
            return self.invoke(input_dict_or_str)

    mock_llm = MockLLM()

    try:
        if Section.ESTATUTO_SOCIAL in RETRIEVER_CONFIGS:
            print(
                '\n--- Testando Seção ESTATUTO_SOCIAL (Re-ranking pode estar desabilitado por padrão) ---'
            )
            test_question_estatuto = 'Qual o capital social da empresa MTI?'

            if Section.ESTATUTO_SOCIAL in _retriever_cache:
                del _retriever_cache[Section.ESTATUTO_SOCIAL]

            estatuto_retriever = get_estatuto_social_retriever()
            if estatuto_retriever:
                print(
                    f'Tipo do retriever para Estatuto Social: {type(estatuto_retriever)}'
                )
                retrieved_docs = estatuto_retriever.get_relevant_documents(
                    test_question_estatuto
                )
                print(
                    f"Documentos recuperados para '{test_question_estatuto}': {len(retrieved_docs)}"
                )
                for i, doc in enumerate(retrieved_docs):
                    print(f'  Doc {i+1}: {doc.page_content[:150]}...')
                    if (
                        hasattr(doc, 'metadata')
                        and 'relevance_score' in doc.metadata
                    ):
                        print(
                            f"    Score de Relevância (Flashrank): {doc.metadata['relevance_score']}"
                        )
            else:
                print(
                    'Não foi possível obter o retriever para Estatuto Social.'
                )
        else:
            print('⚠️ Seção ESTATUTO_SOCIAL não configurada para teste.')

    except Exception as e:
        print(f'❌ Erro durante o teste: {e}')
        import traceback

        traceback.print_exc()

    print('\n✅ Teste do módulo retrievers concluído.')
