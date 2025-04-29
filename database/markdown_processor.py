import re
from langchain_core.documents import Document
import os

def process_markdown(markdown_text, filepath):
    documents = []

    if "Iniciativas.md" in filepath:
        unidades = re.split(r"(## Unidade:)", markdown_text)
        if len(unidades) <= 1:
            raise ValueError("❌ O arquivo Markdown não possui unidades no formato esperado.")

        for i in range(1, len(unidades), 2):
            unidade_content = unidades[i + 1]
            unidade_name = unidade_content.split('\n', 1)[0].split('_')[0].strip()
            combined_text = f"## Unidade: {unidade_name}\n{unidade_content.strip()}"
            documents.append(Document(page_content=combined_text, metadata={"unidade": unidade_name}))

    elif "riscos_operacionais.md" in filepath:
        unidades = re.split(r"(## Riscos:)", markdown_text)
        if len(unidades) <= 1:
            raise ValueError("❌ O arquivo Markdown não possui riscos no formato esperado.")

        for i in range(1, len(unidades), 2):
            risco_content = unidades[i + 1]
            risco_name = risco_content.split('\n', 1)[0].split('_')[0].strip()
            combined_text = f"## Riscos: {risco_name}\n{risco_content.strip()}"
            documents.append(Document(page_content=combined_text, metadata={"risco": risco_name}))

    else:
        sections = re.split(r"(## .+)", markdown_text)
        if len(sections) <= 1:
            documents.append(Document(page_content=markdown_text.strip(), metadata={"source": os.path.basename(filepath)}))
        else:
            for i in range(1, len(sections), 2):
                section_title = sections[i].strip()
                section_content = sections[i + 1].strip()
                documents.append(Document(page_content=f"{section_title}\n{section_content}", metadata={"source": os.path.basename(filepath)}))
    
    return documents