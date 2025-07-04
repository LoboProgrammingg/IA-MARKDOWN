import re
from langchain_core.documents import Document


def process_oms_markdown(markdown_text, filepath):
    documents = []

    if 'oms_unidade.md' in filepath:
        unidades = re.split(r'(## Unidade:)', markdown_text)
        if len(unidades) <= 1:
            raise ValueError(
                '❌ O arquivo Markdown não possui unidades no formato esperado.'
            )

        for i in range(1, len(unidades), 2):
            try:
                unidade_content = unidades[i + 1].strip()
                unidade_name = (
                    unidade_content.split('\n', 1)[0].split('_')[0].strip()
                )

                print(f'[DEBUG] Processando Unidade: {unidade_name}')

                combined_text = (
                    f'{unidades[i]} {unidade_name}\n{unidade_content.strip()}'
                )
                documents.append(
                    Document(
                        page_content=combined_text,
                        metadata={'unidade': unidade_name},
                    )
                )
            except IndexError:
                print(f'[ERRO] Não foi possível processar a unidade em {i}')

    else:
        raise ValueError("❌ O arquivo fornecido não é 'oms_unidade.md'.")

    return documents
