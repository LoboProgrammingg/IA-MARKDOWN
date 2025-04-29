import os
import re
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores.faiss import FAISS
from dotenv import load_dotenv
from config.config import MARKDOWN_PATH, VECTORSTORE_DIR, FAISS_INDEX_PATH

load_dotenv()

def load_markdown(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def needs_update(markdown_path, vectorstore_path):
    return (not os.path.exists(vectorstore_path) or 
            os.path.getmtime(markdown_path) > os.path.getmtime(vectorstore_path))

def process_markdown(markdown_text):
    unidades = re.split(r"(## Unidade:)", markdown_text)
    if len(unidades) <= 1:
        raise ValueError("❌ O arquivo Markdown não possui unidades no formato esperado.")

    documents = []
    for i in range(1, len(unidades), 2):
        unidade_content = unidades[i + 1]
        unidade_name = unidade_content.split('\n', 1)[0].split('_')[0].strip()
        combined_text = f"## Unidade: {unidade_name}\n{unidade_content.strip()}"
        documents.append(Document(page_content=combined_text, metadata={"unidade": unidade_name}))
    return documents

def create_or_update_vectorstore():
    print("🔄 Atualizando o vectorstore...")
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    documents = process_markdown(load_markdown(MARKDOWN_PATH))
    FAISS.from_documents(documents, OpenAIEmbeddings(model='text-embedding-3-large')).save_local(FAISS_INDEX_PATH)
    print("✅ Vectorstore atualizado e salvo.")

def get_vectorstore():
    if needs_update(MARKDOWN_PATH, FAISS_INDEX_PATH):
        create_or_update_vectorstore()
    print("✅ Carregando vectorstore salvo.")
    return FAISS.load_local(FAISS_INDEX_PATH, OpenAIEmbeddings(model='text-embedding-3-large'), allow_dangerous_deserialization=True)