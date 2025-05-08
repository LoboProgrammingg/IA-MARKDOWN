import re
from langchain_core.documents import Document

def process_iesgo_markdown(markdown_text, filepath):
    documents = []

    if "iesgo_structured.md" in filepath:
        temas = re.split(r"(## Tema:)", markdown_text)
        if len(temas) <= 1:
            raise ValueError("❌ O arquivo Markdown não possui temas no formato esperado.")

        for i in range(1, len(temas), 2):
            tema_content = temas[i + 1]
            tema_name = tema_content.split('\n', 1)[0].strip()

            indicadores = re.findall(r"### Indicador:\s*(.+)", tema_content)
            
            combined_text = f"## Tema: {tema_name}\n{tema_content.strip()}"
            documents.append(Document(page_content=combined_text, metadata={"tema": tema_name, "indicadores": indicadores}))

    return documents