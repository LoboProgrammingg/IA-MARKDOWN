import os
import re
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores.faiss import FAISS
from dotenv import load_dotenv, find_dotenv
from config.config import MARKDOWN_PATH, VECTORSTORE_DIR, FAISS_INDEX_PATH

_ = load_dotenv(find_dotenv())

def load_markdown_as_text(filepath):
    """Carrega o conteúdo do arquivo Markdown como texto."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def needs_update(markdown_path, vectorstore_path):
    """Verifica se o vectorstore precisa ser atualizado."""
    if not os.path.exists(vectorstore_path):
        return True
    return os.path.getmtime(markdown_path) > os.path.getmtime(vectorstore_path)

def normalize_unidade(unidade_name):
    """Normaliza o nome da unidade removendo sufixos desnecessários."""
    return unidade_name.split('_')[0] if '_' in unidade_name else unidade_name

def process_markdown_to_documents(markdown_text):
    documents = []
    unidades = re.split(r"(## Unidade:)", markdown_text)
    if len(unidades) <= 1:
        raise ValueError("❌ O arquivo Markdown não possui unidades no formato esperado.")

    for i in range(1, len(unidades), 2):
        unidade_content = unidades[i + 1]
        unidade_full = unidade_content.split('\n', 1)[0].strip()
        unidade_name = normalize_unidade(unidade_full)
        combined_text = f"## Unidade: {unidade_full}\n{unidade_content.strip()}"
        documents.append(Document(page_content=combined_text, metadata={"unidade": unidade_name}))
    return documents

def create_or_update_vectorstore():
    """Cria ou atualiza o vectorstore a partir do arquivo Markdown."""
    print("🔄 Alterações detectadas no arquivo. Atualizando o vectorstore...")
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)

    markdown_text = load_markdown_as_text(MARKDOWN_PATH)
    documents = process_markdown_to_documents(markdown_text)

    vectorstore = FAISS.from_documents(
        documents=documents,
        embedding=OpenAIEmbeddings(model='text-embedding-3-large')
    )

    vectorstore.save_local(FAISS_INDEX_PATH)
    print("✅ Vectorstore recriado e salvo na pasta 'vectorstore'.")
    return vectorstore

def get_vectorstore():
    """Carrega ou cria o vectorstore baseado no arquivo Markdown."""
    if needs_update(MARKDOWN_PATH, FAISS_INDEX_PATH):
        return create_or_update_vectorstore()

    print("✅ Carregando o vectorstore salvo.")
    return FAISS.load_local(
        FAISS_INDEX_PATH,
        OpenAIEmbeddings(model='text-embedding-3-large'),
        allow_dangerous_deserialization=True
    )