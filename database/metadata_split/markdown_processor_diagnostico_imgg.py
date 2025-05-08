from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def process_diagnostico_imgg_markdown(markdown_text, filepath, chunk_size=1500, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = text_splitter.split_text(markdown_text)

    documents = [
        Document(page_content=chunk.strip(), metadata={"source": filepath})
        for chunk in chunks
    ]

    return documents