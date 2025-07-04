import re
from langchain_core.documents import Document


def process_regimento_markdown(
    markdown_text: str, filepath: str
) -> list[Document]:
    documents = []

    if 'regimento_interno_structured.md' in filepath:
        unidades = re.split(r'(## Unidade:)', markdown_text)

        if len(unidades) <= 1:
            raise ValueError(
                "❌ O arquivo Markdown do regimento não possui '## Unidade:' no formato esperado."
            )

        for i in range(1, len(unidades), 2):
            unidade_delimiter = unidades[i]
            unidade_content = unidades[i + 1]

            unidade_name = unidade_content.split('\n', 1)[0].strip()

            print(f'[DEBUG] Processando Unidade: {unidade_name}')

            combined_text = f'{unidade_delimiter}{unidade_content.strip()}'

            documents.append(
                Document(
                    page_content=combined_text,
                    metadata={'unidade': unidade_name},
                )
            )
    else:
        raise ValueError("❌ O arquivo fornecido não é 'regimento_interno.md'.")

    return documents
