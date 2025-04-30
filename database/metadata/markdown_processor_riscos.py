import re
from langchain_core.documents import Document

def process_riscos_markdown(markdown_text, filepath):
    documents = []

    if "riscos_operacionais.md" in filepath:
        unidades = re.split(r"(## Riscos:)", markdown_text)
        if len(unidades) <= 1:
            raise ValueError("❌ O arquivo Markdown não possui riscos no formato esperado.")

        for i in range(1, len(unidades), 2):
            risco_content = unidades[i + 1]
            risco_name = risco_content.split('\n', 1)[0].split('_')[0].strip()
            combined_text = f"## Riscos: {risco_name}\n{risco_content.strip()}"
            documents.append(Document(page_content=combined_text, metadata={"risco": risco_name}))

    return documents