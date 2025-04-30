import re
from langchain_core.documents import Document

def process_iniciativas_markdown(markdown_text, filepath):
    documents = []

    if "Iniciativas.md" in filepath:
        unidades = re.split(r"(## Unidade:)", markdown_text)
        if len(unidades) <= 1:
            raise ValueError("❌ O arquivo Markdown não possui unidades no formato esperado.")

        for i in range(1, len(unidades), 2):
            unidade_content = unidades[i + 1]
            unidade_name = unidade_content.split('\n', 1)[0].split('_')[0].strip()

            diretorias = re.split(r"(### Diretoria:)", unidade_content)
            if len(diretorias) <= 1:
                combined_text = f"## Unidade: {unidade_name}\n{unidade_content.strip()}"
                documents.append(Document(page_content=combined_text, metadata={"unidade": unidade_name}))
            else:
                for j in range(1, len(diretorias), 2):
                    diretoria_content = diretorias[j + 1]
                    diretoria_name = diretoria_content.split('\n', 1)[0].strip()

                    combined_text = f"## Unidade: {unidade_name}\n### Diretoria: {diretoria_name}\n{diretoria_content.strip()}"
                    documents.append(Document(page_content=combined_text, metadata={
                        "unidade": unidade_name,
                        "diretoria": diretoria_name
                    }))

    return documents