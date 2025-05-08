import re
from langchain_core.documents import Document

def process_indicadores_markdown(markdown_text, filepath):
    documents = []

    if "indicadores_structured.md" in filepath:
        unidades = re.split(r"(## Unidade:)", markdown_text)
        if len(unidades) <= 1:
            raise ValueError("❌ O arquivo Markdown não possui unidades no formato esperado.")

        for i in range(1, len(unidades), 2):
            unidade_content = unidades[i + 1]
            unidade_name = unidade_content.split('\n', 1)[0].split('_')[0].strip()

            print(f"[DEBUG] Processando Unidade: {unidade_name}")

            combined_text = f"## Unidade: {unidade_name}\n{unidade_content.strip()}"
            documents.append(Document(
                page_content=combined_text,
                metadata={"unidade": unidade_name}
            ))
    else:
        raise ValueError("❌ O arquivo fornecido não é 'indicadores_structured.md'.")

    return documents