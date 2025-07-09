from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from google.genai import types

from retriever.retrievers import (
    get_iniciativas_retriever,
    get_iesgo_retriever,
    get_imgg_retriever,
    get_indicadores_retriever,
    get_diagnostico_imgg_retriever,
    get_diagnostico_iesgo_retriever,
    get_oms_retriever,
    get_padroes_retriever,
    get_pta_retriever,
    get_riscos_retriever,
    get_estatuto_social_retriever,
    get_estrutura_processos_retriever,
    get_regimento_interno_retriever,
    get_gerentes_retriever,
)
from prompt.prompt_template import prompt_template_with_memory
from memory.memory_handler import get_session_history
from .utils import validate_env_variable, safe_invoke, combine_contexts


def create_pipeline_with_separated_vectorstores():

    iniciativas_retriever = get_iniciativas_retriever()
    iesgo_retriever = get_iesgo_retriever()
    imgg_retriever = get_imgg_retriever()
    indicadores_retriever = get_indicadores_retriever()
    diagnostico_imgg_retriever = get_diagnostico_imgg_retriever()
    diagnostico_iesgo_retriever = get_diagnostico_iesgo_retriever()
    oms_retriever = get_oms_retriever()
    padroes_retriever = get_padroes_retriever()
    pta_retriever = get_pta_retriever()
    riscos_retriever = get_riscos_retriever()
    estatuto_social_retriever = get_estatuto_social_retriever()
    estrutura_processos_retriever = get_estrutura_processos_retriever()
    regimento_interno_retriever = get_regimento_interno_retriever()
    gerentes_retriever = get_gerentes_retriever()

    content_preparation = RunnableParallel(
        {
            'pergunta': lambda x: x['pergunta'],
            'memoria': lambda x: x['memoria'],
            'iniciativas_contexto': lambda x: safe_invoke(
                iniciativas_retriever, x['pergunta']
            ),
            'iesgo_contexto': lambda x: safe_invoke(
                iesgo_retriever, x['pergunta']
            ),
            'imgg_contexto': lambda x: safe_invoke(
                imgg_retriever, x['pergunta']
            ),
            'indicadores_contexto': lambda x: safe_invoke(
                indicadores_retriever, x['pergunta']
            ),
            'diagnostico_imgg_contexto': lambda x: safe_invoke(
                diagnostico_imgg_retriever, x['pergunta']
            ),
            'diagnostico_iesgo_contexto': lambda x: safe_invoke(
                diagnostico_iesgo_retriever, x['pergunta']
            ),
            'oms_contexto': lambda x: safe_invoke(
                oms_retriever, x['pergunta']
            ),
            'padroes_contexto': lambda x: safe_invoke(
                padroes_retriever, x['pergunta']
            ),
            'pta_contexto': lambda x: safe_invoke(
                pta_retriever, x['pergunta']
            ),
            'riscos_contexto': lambda x: safe_invoke(
                riscos_retriever, x['pergunta']
            ),
            'estatuto_social_contexto': lambda x: safe_invoke(
                estatuto_social_retriever, x['pergunta']
            ),
            'estrutura_processos_contexto': lambda x: safe_invoke(
                estrutura_processos_retriever, x['pergunta']
            ),
            'regimento_interno_contexto': lambda x: safe_invoke(
                regimento_interno_retriever, x['pergunta']
            ),
            'gerentes_contexto': lambda x: safe_invoke(
                gerentes_retriever, x['pergunta']
            ),
        }
    )

    combine_contexts_step = content_preparation | combine_contexts

    gemini_api_key = validate_env_variable('GEMINI_API_KEY')

    generation_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True, thinking_budget=2000
        )
    )

    core_rag_chain = (
        combine_contexts_step
        | prompt_template_with_memory
        | ChatGoogleGenerativeAI(
            model='gemini-2.5-pro',
            temperature=0.2,
            max_output_tokens=65536,
            google_api_key=gemini_api_key,
            model_kwargs={'generation_config': generation_config},
        )
        | StrOutputParser()
    )

    return RunnableWithMessageHistory(
        core_rag_chain,
        get_session_history,
        input_messages_key='pergunta',
        history_messages_key='memoria',
    )


def create_pipeline_single_vectorstore(vectorstore_name: str):

    retrievers_map = {
        'iniciativas': get_iniciativas_retriever(),
        'iesgo': get_iesgo_retriever(),
        'imgg': get_imgg_retriever(),
        'indicadores': get_indicadores_retriever(),
        'diagnostico_imgg': get_diagnostico_imgg_retriever(),
        'diagnostico_iesgo': get_diagnostico_iesgo_retriever(),
        'oms': get_oms_retriever(),
        'padroes': get_padroes_retriever(),
        'pta': get_pta_retriever(),
        'riscos': get_riscos_retriever(),
        'estatuto_social': get_estatuto_social_retriever(),
        'estrutura_processos': get_estrutura_processos_retriever(),
        'regimento_interno': get_regimento_interno_retriever(),
        'gerentes': get_gerentes_retriever(),
    }

    retriever = retrievers_map.get(vectorstore_name)
    if not retriever:
        raise ValueError(
            f'Nome de vectorstore inválido: {vectorstore_name}. Vectorstores disponíveis: {list(retrievers_map.keys())}'
        )

    def prepare_single_context(inputs):
        docs = safe_invoke(retriever, inputs['pergunta'])
        contexto_str = '\n'.join(
            doc.page_content
            for doc in docs
            if doc and hasattr(doc, 'page_content')
        )
        return {
            'pergunta': inputs['pergunta'],
            'contexto': contexto_str
            if contexto_str
            else 'Nenhum contexto relevante encontrado.',
            'memoria': inputs['memoria'],
        }

    gemini_api_key = validate_env_variable('GEMINI_API_KEY')

    generation_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True, thinking_budget=3300
        )
    )

    single_chain = (
        prepare_single_context
        | prompt_template_with_memory
        | ChatGoogleGenerativeAI(
            model='gemini-2.5-pro',
            temperature=0.3,
            max_output_tokens=65536,
            google_api_key=gemini_api_key,
            model_kwargs={'generation_config': generation_config},
        )
        | StrOutputParser()
    )

    return RunnableWithMessageHistory(
        single_chain,
        get_session_history,
        input_messages_key='pergunta',
        history_messages_key='memoria',
    )


if __name__ == '__main__':
    print('🧪 Testando a criação dos pipelines (conceitual)...')

    try:
        pipeline_multi_vs = create_pipeline_with_separated_vectorstores()
        print(
            f'✅ Pipeline com múltiplos vectorstores criado: {type(pipeline_multi_vs)}'
        )
    except Exception as e:
        print(f'❌ Erro ao criar pipeline com múltiplos vectorstores: {e}')

    try:
        pipeline_single_vs_estatuto = create_pipeline_single_vectorstore(
            'estatuto_social'
        )
        print(
            f"✅ Pipeline com single vectorstore ('estatuto_social') criado: {type(pipeline_single_vs_estatuto)}"
        )

        pipeline_single_vs_processos = create_pipeline_single_vectorstore(
            'estrutura_processos'
        )
        print(
            f"✅ Pipeline com single vectorstore ('estrutura_processos') criado: {type(pipeline_single_vs_processos)}"
        )

        pipeline_single_vs_regimento = create_pipeline_single_vectorstore(
            'regimento_interno'
        )
        print(
            f"✅ Pipeline com single vectorstore ('regimento_interno') criado: {type(pipeline_single_vs_regimento)}"
        )

        pipeline_single_vs_gerentes = create_pipeline_single_vectorstore(
            'gerentes'
        )
        print(
            f"✅ Pipeline com single vectorstore ('gerentes') criado: {type(pipeline_single_vs_gerentes)}"
        )

    except ValueError as ve:
        print(
            f'🔶 Erro de valor ao criar pipeline com single vectorstore: {ve}'
        )
    except Exception as e:
        print(f'❌ Erro ao criar pipeline com single vectorstore: {e}')

    print('\n✅ Testes conceituais de criação de pipeline concluídos.')
