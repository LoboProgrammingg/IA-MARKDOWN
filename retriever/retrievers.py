from database.vectorstore_handler import get_iniciativas_vectorstore, get_iesgo_vectorstore, get_imgg_vectorstore

def get_iniciativas_retriever():
    return get_iniciativas_vectorstore().as_retriever(
        search_type="similarity", search_kwargs={"k": 4, "fetch_k": 23}
    )

def get_iesgo_retriever():
    return get_iesgo_vectorstore().as_retriever(
        search_type="similarity", search_kwargs={"k": 4}
    )

def get_imgg_retriever():
    return get_imgg_vectorstore().as_retriever(
        search_type="similarity", search_kwargs={"k": 1}
    )