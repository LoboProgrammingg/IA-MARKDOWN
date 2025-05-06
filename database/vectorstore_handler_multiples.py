import os
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings
from config.config import MARKDOWN_PATH, VECTORSTORE_DIR, FAISS_INDEX_PATH
from database.file_handler import load_markdown, needs_update
from database.metadata.markdown_processor_iniciativas import process_iniciativas_markdown

def create_or_update_vectorstore():
    print("🔄 Atualizando o vectorstore...")
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)

    all_documents = []

    for filename in os.listdir(MARKDOWN_PATH):
        full_path = os.path.join(MARKDOWN_PATH, filename)

        if not filename.endswith(".md"):
            continue

        markdown_text = load_markdown(full_path)

        if "Iniciativas.md" in filename:
            all_documents += process_iniciativas_markdown(markdown_text, full_path)

    full_index_path = os.path.join(VECTORSTORE_DIR, "full_index")
    FAISS.from_documents(all_documents, OpenAIEmbeddings(model='text-embedding-3-large')).save_local(full_index_path)
    print(f"✅ Vectorstore único atualizado e salvo em {full_index_path}.")

def get_vectorstore():
    if needs_update(MARKDOWN_PATH, FAISS_INDEX_PATH):
        create_or_update_vectorstore()

    print("✅ Carregando vectorstore salvo de 'full_index'.")
    vectorstore_dir = os.path.join(VECTORSTORE_DIR, "full_index")
    return FAISS.load_local(vectorstore_dir, OpenAIEmbeddings(model='text-embedding-3-large'), allow_dangerous_deserialization=True)
