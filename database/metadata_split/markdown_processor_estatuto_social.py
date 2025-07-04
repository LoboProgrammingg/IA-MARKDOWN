import re
from langchain_core.documents import Document


def process_estatuto_markdown(
    markdown_text: str, filepath: str
) -> list[Document]:
    documents = []

    if 'estatuto_social_structured.md' in filepath:
        capitulos_content = re.findall(
            r'(## CAPÍTULO:.*?)(?=## CAPÍTULO:|\Z)', markdown_text, re.DOTALL
        )

        if not capitulos_content:
            raise ValueError(
                "❌ O arquivo Markdown do estatuto não encontrou nenhum padrão '## CAPÍTULO:' para iniciar a divisão."
            )

        for content in capitulos_content:
            capitulo_name = (
                content.split('\n', 1)[0].replace('## CAPÍTULO:', '').strip()
            )

            print(f'[DEBUG] Processando Capítulo: {capitulo_name}')

            document_text = content.strip()

            documents.append(
                Document(
                    page_content=document_text,
                    metadata={'capitulo': capitulo_name},
                )
            )
    else:
        raise ValueError(
            "❌ O arquivo fornecido não é 'estatuto_social_structured.md'."
        )

    return documents
