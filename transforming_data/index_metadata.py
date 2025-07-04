import re
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_metadata(text: str) -> dict:
    metadata = {}

    unidade_match = re.search(r"## Unidade: (.+)", text)
    diretoria_match = re.search(r"### Diretoria: (.+)", text)
    objetivo_match = re.search(r"### Objetivo Estratégico: (.+)", text)
    perspectiva_match = re.search(r"#### Perspectiva: (.+)", text)

    if unidade_match:
        metadata["unidade"] = unidade_match.group(1).strip()
    if diretoria_match:
        metadata["diretoria"] = diretoria_match.group(1).strip()
    if objetivo_match:
        metadata["objetivo_estrategico"] = objetivo_match.group(1).strip()
    if perspectiva_match:
        metadata["perspectiva"] = perspectiva_match.group(1).strip()

    return metadata

def index_markdown_file(filepath: str, index_path: str = "faiss_index"):
    loader = TextLoader(filepath, encoding='utf-8')
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    for doc in chunks:
        text = doc.page_content
        doc.metadata.update(extract_metadata(text))

    vectorstore = FAISS.from_documents(chunks, embedding=OpenAIEmbeddings())
    vectorstore.save_local(index_path)
    print(f"[INFO] Indexação concluída e salva em: {index_path}")

if __name__ == "__main__":
    index_markdown_file("documentation/Iniciativas.md")