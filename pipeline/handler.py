from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from google.genai import types

from retriever.retrievers import get_retriever
from retriever.section import Section
from prompt.prompt_template import prompt_template_with_memory
from memory.memory_handler import get_session_history
from .utils import validate_env_variable, safe_invoke, combine_contexts
from . import config_manager # Importa o novo gerenciador de config do pipeline

def create_pipeline_with_separated_vectorstores():
    """Cria um pipeline de RAG que consulta todos os vectorstores em paralelo."""
    config = config_manager.get_configuration("multi_vectorstore")
    
    retriever_map = {f"{s.name.lower()}_contexto": get_retriever(s) for s in Section}
    content_preparation_steps = {'pergunta': lambda x: x['pergunta'], 'memoria': lambda x: x['memoria']}
    for key, retriever in retriever_map.items():
        content_preparation_steps[key] = lambda x, r=retriever: safe_invoke(r, x['pergunta'])
    
    content_preparation = RunnableParallel(content_preparation_steps)
    combine_contexts_step = content_preparation | combine_contexts
    gemini_api_key = validate_env_variable('GEMINI_API_KEY')
    
    generation_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True, thinking_budget=config["thinking_budget"]
        )
    )
    
    core_rag_chain = (
        combine_contexts_step
        | prompt_template_with_memory
        | ChatGoogleGenerativeAI(
            model=config["model"],
            temperature=config["temperature"],
            max_output_tokens=config["max_output_tokens"],
            google_api_key=gemini_api_key,
            model_kwargs={'generation_config': generation_config},
        )
        | StrOutputParser()
    )
    
    return RunnableWithMessageHistory(
        core_rag_chain, get_session_history,
        input_messages_key='pergunta', history_messages_key='memoria',
    )

def create_pipeline_single_vectorstore(vectorstore_name: str):
    """Cria um pipeline de RAG que consulta um único vectorstore especificado."""
    config = config_manager.get_configuration("single_vectorstore")

    try:
        section = Section[vectorstore_name.upper()]
    except KeyError:
        valid_sections = ', '.join([s.name.lower() for s in Section])
        raise ValueError(f"Nome de vectorstore inválido: {vectorstore_name}. Disponíveis: {valid_sections}")

    retriever = get_retriever(section)
    if not retriever:
        raise ValueError(f"Não foi possível carregar o retriever para: {vectorstore_name}")

    def prepare_single_context(inputs):
        docs = safe_invoke(retriever, inputs['pergunta'])
        contexto_str = '\n'.join(doc.page_content for doc in docs if doc and hasattr(doc, 'page_content'))
        return {
            'pergunta': inputs['pergunta'],
            'contexto': contexto_str or 'Nenhum contexto relevante encontrado.',
            'memoria': inputs['memoria'],
        }

    gemini_api_key = validate_env_variable('GEMINI_API_KEY')
    generation_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True, thinking_budget=config["thinking_budget"]
        )
    )

    single_chain = (
        prepare_single_context
        | prompt_template_with_memory
        | ChatGoogleGenerativeAI(
            model=config["model"],
            temperature=config["temperature"],
            max_output_tokens=config["max_output_tokens"],
            google_api_key=gemini_api_key,
            model_kwargs={'generation_config': generation_config},
        )
        | StrOutputParser()
    )
    
    return RunnableWithMessageHistory(
        single_chain, get_session_history,
        input_messages_key='pergunta', history_messages_key='memoria',
    )
