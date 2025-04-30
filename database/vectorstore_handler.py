import os
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings
from config.config import MARKDOWN_PATH, VECTORSTORE_DIR, FAISS_INDEX_PATH
from database.file_handler import load_markdown, needs_update
from database.metadata.markdown_processor_iniciativas import process_iniciativas_markdown
from database.metadata.markdown_processor_riscos import process_riscos_markdown

def create_or_update_vectorstore():
    print("🔄 Atualizando o vectorstore...")
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)

    markdown_text = load_markdown(MARKDOWN_PATH)

    if "Iniciativas.md" in MARKDOWN_PATH:
        iniciativas_documents = process_iniciativas_markdown(markdown_text, MARKDOWN_PATH)
        iniciativas_path = os.path.join(VECTORSTORE_DIR, "iniciativas_faiss_index")
        FAISS.from_documents(iniciativas_documents, OpenAIEmbeddings(model='text-embedding-3-large')).save_local(iniciativas_path)
        print(f"✅ Vectorstore para 'Iniciativas.md' atualizado e salvo em {iniciativas_path}.")

    if "riscos_operacionais.md" in MARKDOWN_PATH:
        riscos_documents = process_riscos_markdown(markdown_text, MARKDOWN_PATH)
        riscos_path = os.path.join(VECTORSTORE_DIR, "riscos_faiss_index")
        FAISS.from_documents(riscos_documents, OpenAIEmbeddings(model='text-embedding-3-large')).save_local(riscos_path)
        print(f"✅ Vectorstore para 'riscos_operacionais.md' atualizado e salvo em {riscos_path}.")

def get_vectorstore(file_type="iniciativas"):
    if needs_update(MARKDOWN_PATH, FAISS_INDEX_PATH):
        create_or_update_vectorstore()

    print(f"✅ Carregando vectorstore salvo para '{file_type}'.")
    vectorstore_dir = os.path.join(VECTORSTORE_DIR, f"{file_type}_faiss_index")
    return FAISS.load_local(vectorstore_dir, OpenAIEmbeddings(model='text-embedding-3-large'), allow_dangerous_deserialization=True)