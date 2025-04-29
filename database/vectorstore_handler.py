import os
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings
from config.config import MARKDOWN_PATH, VECTORSTORE_DIR, FAISS_INDEX_PATH
from database.file_handler import load_markdown, needs_update
from database.markdown_processor import process_markdown

def create_or_update_vectorstore():
    print("🔄 Atualizando o vectorstore...")
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    markdown_text = load_markdown(MARKDOWN_PATH)
    documents = process_markdown(markdown_text, MARKDOWN_PATH)
    FAISS.from_documents(documents, OpenAIEmbeddings(model='text-embedding-3-large')).save_local(FAISS_INDEX_PATH)
    print("✅ Vectorstore atualizado e salvo.")

def get_vectorstore():
    if needs_update(MARKDOWN_PATH, FAISS_INDEX_PATH):
        create_or_update_vectorstore()
    print("✅ Carregando vectorstore salvo.")
    return FAISS.load_local(FAISS_INDEX_PATH, OpenAIEmbeddings(model='text-embedding-3-large'), allow_dangerous_deserialization=True)