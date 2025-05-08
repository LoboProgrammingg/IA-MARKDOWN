from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from database.vectorstore_handler import (
    get_iniciativas_vectorstore,
    get_iesgo_vectorstore,
    get_imgg_vectorstore,
    get_indicadores_vectorstore,
    get_diagnostico_imgg_vectorstore,
)

def get_iniciativas_retriever():
    return get_iniciativas_vectorstore().as_retriever(
        search_type="mmr", search_kwargs={"k": 4, "fetch_k": 23}
    )

def get_iesgo_retriever():
    return get_iesgo_vectorstore().as_retriever(
        search_type="mmr", search_kwargs={"k": 2, "fetch_k": 11}
    )

def get_imgg_retriever():
    return get_imgg_vectorstore().as_retriever(
        search_type="mmr", search_kwargs={"k": 1}
    )

def get_indicadores_retriever():
    return get_indicadores_vectorstore().as_retriever(
        search_type="mmr", search_kwargs={"k": 5, "fetch_k": 10}
    )

def get_diagnostico_imgg_retriever():
    return get_diagnostico_imgg_vectorstore().as_retriever(
        search_type="mmr", search_kwargs={"k": 4, "fetch_k": 20}
    )

# Instanciar os retrievers
iniciativas_retriever = get_iniciativas_retriever()
iesgo_retriever = get_iesgo_retriever()
imgg_retriever = get_imgg_retriever()
indicadores_retriever = get_indicadores_retriever()
diagnostico_imgg_retriever = get_diagnostico_imgg_retriever()

# Prompt Template para lidar com conexões
prompt_template = PromptTemplate(
    input_variables=["section", "question", "connections"],
    template="""
    Você está lidando com informações relacionadas à seção: {section}.
    
    Pergunta: {question}
    
    Conexões relevantes com outros documentos:
    {connections}
    
    Por favor, forneça uma resposta clara e bem detalhada com base nos dados disponíveis.
    """
)

def fetch_connections(question):
    connections = []
    
    iniciativas_results = iniciativas_retriever.get_relevant_documents(question)
    iesgo_results = iesgo_retriever.get_relevant_documents(question)
    imgg_results = imgg_retriever.get_relevant_documents(question)
    indicadores_results = indicadores_retriever.get_relevant_documents(question)
    diagnostico_imgg_results = diagnostico_imgg_retriever.get_relevant_documents(question)

    # Adicionar conexões relevantes às respostas
    if iniciativas_results:
        connections.append("Dados relacionados do vectorstore 'Iniciativas'.")
    if iesgo_results:
        connections.append("Dados relacionados do vectorstore 'iESGo'.")
    if imgg_results:
        connections.append("Dados relacionados do vectorstore 'IMGG'.")
    if indicadores_results:
        connections.append("Dados relacionados do vectorstore 'Indicadores'.")
    if diagnostico_imgg_results:
        connections.append("Dados relacionados do vectorstore 'Diagnóstico IMGG'.")

    return connections

def answer_with_connections(section, question):
    connections = fetch_connections(question)
    
    connections_text = "\n".join(connections) if connections else "Nenhuma conexão encontrada."

    if section == "Iniciativas":
        qa_chain = RetrievalQA.from_chain_type(retriever=iniciativas_retriever, chain_type="stuff", chain_type_kwargs={"prompt": prompt_template})
    elif section == "iESGo":
        qa_chain = RetrievalQA.from_chain_type(retriever=iesgo_retriever, chain_type="stuff", chain_type_kwargs={"prompt": prompt_template})
    elif section == "IMGG":
        qa_chain = RetrievalQA.from_chain_type(retriever=imgg_retriever, chain_type="stuff", chain_type_kwargs={"prompt": prompt_template})
    elif section == "Indicadores":
        qa_chain = RetrievalQA.from_chain_type(retriever=indicadores_retriever, chain_type="stuff", chain_type_kwargs={"prompt": prompt_template})
    elif section == "Diagnóstico IMGG":
        qa_chain = RetrievalQA.from_chain_type(retriever=diagnostico_imgg_retriever, chain_type="stuff", chain_type_kwargs={"prompt": prompt_template})
    else:
        return "Seção desconhecida. Por favor, forneça uma seção válida."

    return qa_chain.run({"section": section, "question": question, "connections": connections_text})