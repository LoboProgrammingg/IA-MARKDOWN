import re
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from database.vectorstore_handler import get_vectorstore
from prompt.prompt_template import prompt_template

def create_pipeline():
    """Configura o pipeline utilizando a vectorstore."""
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(
        search_type='similarity',
        search_kwargs={'k': 10, 'fetch_k': 50}
    )

    setup = RunnableParallel({
        'pergunta': RunnablePassthrough(),
        'contexto': retriever
    })

    chain = setup | prompt_template | ChatOpenAI(
        model='gpt-4o-mini',
        temperature=0.3,
        max_tokens=8000,
        model_kwargs={"stream": True}
    ) | StrOutputParser()

    return chain

def get_response_stream(question: str):
    """Função para obter a resposta do pipeline com streaming."""
    chain = create_pipeline()
    return chain.stream(question)
