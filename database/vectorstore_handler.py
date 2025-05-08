import os
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings
from config.config import MARKDOWN_PATH, VECTORSTORE_DIR
from database.file_handler import load_markdown, needs_update
from database.metadata_split.markdown_processor_iniciativas import process_iniciativas_markdown
from database.metadata_split.markdown_iesgo import process_iesgo_markdown
from database.metadata_split.markdown_imgg import process_imgg_markdown
from database.metadata_split.markdown_indicadores import process_indicadores_markdown
from database.metadata_split.markdown_processor_diagnostico_imgg import process_diagnostico_imgg_markdown


def create_or_update_specific_vectorstore(document_type, markdown_file, processor_function):
    print(f"🔄 Atualizando o vectorstore para {document_type}...")
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)

    if not os.path.isfile(markdown_file):
        print(f"⚠️ Arquivo não encontrado ou inválido: {markdown_file}. Ignorando...")
        return

    markdown_text = load_markdown(markdown_file)
    documents = processor_function(markdown_text, markdown_file)

    if not documents:
        raise ValueError(f"❌ Nenhum documento processado para {document_type}. Verifique o arquivo Markdown.")

    index_path = os.path.join(VECTORSTORE_DIR, f"{document_type}_index")
    FAISS.from_documents(documents, OpenAIEmbeddings(model='text-embedding-3-large')).save_local(index_path)
    print(f"✅ Vectorstore atualizado e salvo em {index_path}.")


def get_vectorstore(document_type, markdown_file, processor_function):
    index_path = os.path.join(VECTORSTORE_DIR, f"{document_type}_index")

    if needs_update([markdown_file], index_path):
        create_or_update_specific_vectorstore(document_type, markdown_file, processor_function)

    print(f"✅ Carregando vectorstore salvo de '{index_path}'.")
    return FAISS.load_local(index_path, OpenAIEmbeddings(model='text-embedding-3-large'), allow_dangerous_deserialization=True)


def get_iniciativas_vectorstore():
    markdown_file = next((f for f in MARKDOWN_PATH if "Iniciativas.md" in f), None)
    if not markdown_file:
        raise ValueError("❌ Arquivo 'Iniciativas.md' não encontrado em MARKDOWN_PATH.")
    return get_vectorstore("iniciativas", markdown_file, process_iniciativas_markdown)

def get_iesgo_vectorstore():
    markdown_file = next((f for f in MARKDOWN_PATH if "iesgo_structured.md" in f), None)
    if not markdown_file:
        raise ValueError("❌ Arquivo 'iesgo_structured.md' não encontrado em MARKDOWN_PATH.")
    return get_vectorstore("iesgo", markdown_file, process_iesgo_markdown)

def get_imgg_vectorstore():
    markdown_file = next((f for f in MARKDOWN_PATH if "imgg_structured.md" in f), None)
    if not markdown_file:
        raise ValueError("❌ Arquivo 'imgg_structured.md' não encontrado em MARKDOWN_PATH.")
    return get_vectorstore("imgg", markdown_file, process_imgg_markdown)

def get_indicadores_vectorstore():
    markdown_file = next((f for f in MARKDOWN_PATH if "indicadores_structured.md" in f), None)
    if not markdown_file:
        raise ValueError("❌ Arquivo 'indicadores_structured.md' não encontrado em MARKDOWN_PATH.")
    return get_vectorstore("indicadores", markdown_file, process_indicadores_markdown)

def get_diagnostico_imgg_vectorstore():
    markdown_file = next((f for f in MARKDOWN_PATH if "diagnostico_imgg_structured.md" in f), None)
    if not markdown_file:
        raise ValueError("❌ Arquivo 'diagnostico_imgg_structured.md' não encontrado em MARKDOWN_PATH.")
    return get_vectorstore("diagnostico_imgg", markdown_file, process_diagnostico_imgg_markdown)