import os
import re
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores.faiss import FAISS
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# Configurações de caminho e arquivos
MARKDOWN_PATH = "documentation/Iniciativas.md"
VECTORSTORE_DIR = "vectorstore"
FAISS_INDEX_PATH = os.path.join(VECTORSTORE_DIR, "faiss_index")

def needs_update():
    """Verifica se o vetorstore precisa ser atualizado."""
    if not os.path.exists(FAISS_INDEX_PATH):
        return True
    markdown_mtime = os.path.getmtime(MARKDOWN_PATH)
    vectorstore_mtime = os.path.getmtime(FAISS_INDEX_PATH)
    return markdown_mtime > vectorstore_mtime

def normalize_unidade(unidade_name):
    """Normaliza o nome da unidade removendo sufixos desnecessários."""
    return unidade_name.split('_')[0] if '_' in unidade_name else unidade_name

def get_vectorstore():
    """Carrega ou cria a vectorstore baseado no arquivo Markdown."""
    if not os.path.exists(MARKDOWN_PATH):
        raise FileNotFoundError(f"Arquivo não encontrado: {MARKDOWN_PATH}")

    if not needs_update():
        print("✅ Carregando o vectorstore salvo.")
        return FAISS.load_local(
            FAISS_INDEX_PATH,
            OpenAIEmbeddings(model='text-embedding-3-large'),
            allow_dangerous_deserialization=True
        )
    else:
        print("🔄 Alterações detectadas no arquivo. Atualizando o vectorstore...")

        os.makedirs(VECTORSTORE_DIR, exist_ok=True)

        try:
            with open(MARKDOWN_PATH, 'r', encoding='utf-8') as f:
                markdown_text = f.read()
            print("✅ Arquivo Markdown carregado como texto!")
        except Exception as e:
            print(f"❌ Erro ao carregar o arquivo Markdown: {e}")
            raise

        # Processa o markdown em documentos
        documents = []
        unidades = re.split(r"(## Unidade:)", markdown_text)
        if len(unidades) <= 1:
            raise ValueError("❌ O arquivo Markdown não possui unidades no formato esperado.")

        for i in range(1, len(unidades), 2):
            unidade_header = unidades[i]
            unidade_content = unidades[i+1]
            unidade_full = unidade_content.split('\n', 1)[0].strip()
            unidade_name = normalize_unidade(unidade_full)
            combined_text = f"## Unidade: {unidade_full}\n{unidade_content.strip()}"
            documents.append(Document(page_content=combined_text, metadata={"unidade": unidade_name}))

        vectorstore = FAISS.from_documents(
            documents=documents,
            embedding=OpenAIEmbeddings(model='text-embedding-3-large')
        )

        vectorstore.save_local(FAISS_INDEX_PATH)
        print("✅ Vectorstore recriado e salvo na pasta 'vectorstore'.")
        return vectorstore