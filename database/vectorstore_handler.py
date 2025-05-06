import os
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings
from config.config import MARKDOWN_PATH, VECTORSTORE_DIR, FAISS_INDEX_PATH
from database.file_handler import load_markdown, needs_update
from database.metadata.markdown_processor_iniciativas import process_iniciativas_markdown
from database.metadata.markdown_iesgo import process_iesgo_markdown
from database.metadata.markdown_imgg import process_imgg_markdown


def create_or_update_vectorstore():
    print("🔄 Atualizando o vectorstore...")
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)

    all_documents = []

    for markdown_file in MARKDOWN_PATH:
        if not os.path.isfile(markdown_file):
            print(f"⚠️ Arquivo não encontrado ou inválido: {markdown_file}. Ignorando...")
            continue

        markdown_text = load_markdown(markdown_file)

        # Processar diferentes tipos de arquivos Markdown
        if "Iniciativas.md" in markdown_file:
            all_documents += process_iniciativas_markdown(markdown_text, markdown_file)
        elif "iesgo_structured.md" in markdown_file:
            all_documents += process_iesgo_markdown(markdown_text, markdown_file)
        elif "imgg_structured.md" in markdown_file:
            all_documents += process_imgg_markdown(markdown_text, markdown_file)
        else:
            print(f"⚠️ Arquivo Markdown não reconhecido: {markdown_file}. Ignorando...")

    if not all_documents:
        raise ValueError("❌ Nenhum documento processado. Verifique os arquivos Markdown.")

    full_index_path = os.path.join(VECTORSTORE_DIR, "full_index")
    FAISS.from_documents(all_documents, OpenAIEmbeddings(model='text-embedding-3-large')).save_local(full_index_path)
    print(f"✅ Vectorstore atualizado e salvo em {full_index_path}.")

def get_vectorstore():
    if needs_update(MARKDOWN_PATH, FAISS_INDEX_PATH):
        create_or_update_vectorstore()

    print("✅ Carregando vectorstore salvo de 'full_index'.")
    vectorstore_dir = os.path.join(VECTORSTORE_DIR, "full_index")
    return FAISS.load_local(vectorstore_dir, OpenAIEmbeddings(model='text-embedding-3-large'), allow_dangerous_deserialization=True)