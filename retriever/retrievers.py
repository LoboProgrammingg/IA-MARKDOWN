from database.vectorstore_handler import get_iniciativas_vectorstore, get_iesgo_vectorstore, get_imgg_vectorstore

def get_iniciativas_retriever():
    return get_iniciativas_vectorstore().as_retriever(
        search_type="mmr", search_kwargs={"k": 7, "fetch_k": 23}
    )

def get_iesgo_retriever():
    return get_iesgo_vectorstore().as_retriever(
        search_type="mmr", search_kwargs={"k": 2, "fetch_k": 11}
    )

def get_imgg_retriever():
    return get_imgg_vectorstore().as_retriever(
        search_type="mmr", search_kwargs={"k": 1, "fetch_k": 2}
    )