import re
from langchain_core.documents import Document

def process_iesgo_markdown(markdown_text, filepath):
    documents = []

    if "iesgo_structured.md" in filepath:
        unidades = re.split(r"(## Tema:)", markdown_text)
        if len(unidades) <= 1:
            raise ValueError("❌ O arquivo Markdown não possui temas no formato esperado.")

        for i in range(1, len(unidades), 2):
            iesgo_content = unidades[i + 1]
            iesgo_metadata = iesgo_content.split('\n', 1)[0].split('_')[0].strip()
            combined_text = f"## Riscos: {iesgo_metadata}\n{iesgo_content.strip()}"
            documents.append(Document(page_content=combined_text, metadata={"tema": iesgo_metadata}))

    return documents