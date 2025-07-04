import re
from langchain_core.documents import Document


def process_estrutura_markdown(markdown_text, filepath):
    documents = []

    if 'estrutura_processos_structured.md' in filepath:
        sections = re.split(r'(## GERIR[^\n]*)', markdown_text)
        if len(sections) <= 1:
            raise ValueError(
                "❌ O arquivo Markdown não possui seções '## GERIR:' no formato esperado."
            )

        for i in range(1, len(sections), 2):
            section_title = sections[i].strip()
            section_content = (
                sections[i + 1].strip() if i + 1 < len(sections) else ''
            )
            match = re.match(
                r'## GERIR[: ]*(.*)', section_title, re.IGNORECASE
            )
            section_name = match.group(1).strip() if match else section_title

            print(f'[DEBUG] Processando seção: {section_name}')

            combined_text = f'{section_title}\n{section_content}'
            documents.append(
                Document(
                    page_content=combined_text,
                    metadata={'gerir_section': section_name},
                )
            )
    else:
        raise ValueError(
            "❌ O arquivo fornecido não é 'estatuto_social_structured.md'."
        )

    return documents
