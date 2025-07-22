from .section import Section
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


DEFAULT_RETRIEVER_CONFIGS = {
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