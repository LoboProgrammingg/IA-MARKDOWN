import os

MARKDOWN_PATH = [
    "documentation\Iniciativas.md",
    "documentation\iesgo_structured.md",
    "documentation\imgg_structured.md",
]

VECTORSTORE_DIR = "vectorstore"
FAISS_INDEX_PATH = os.path.join(VECTORSTORE_DIR, "faiss_index")
