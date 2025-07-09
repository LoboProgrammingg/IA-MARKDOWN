import os

from langchain_community.vectorstores.faiss import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from config.config import MARKDOWN_PATH, VECTORSTORE_DIR

from database.file_handler import load_markdown, needs_update
from database.metadata_split.markdown_processor_iniciativas import (
    process_iniciativas_markdown,
)
from database.metadata_split.markdown_recursive import markdown_recursive_split
from database.metadata_split.markdown_indicadores import (
    process_indicadores_markdown,
)
from database.metadata_split.markdown_processor_oms import process_oms_markdown
from database.metadata_split.markdown_padroes import process_padroes_markdown
from database.metadata_split.markdown_processor_pta import process_pta_markdown
from database.metadata_split.markdown_riscos import process_riscos_markdown
from database.metadata_split.markdown_processor_estatuto_social import (
    process_estatuto_markdown,
)
from database.metadata_split.markdown_regimento import (
    process_regimento_markdown,
)
from database.metadata_split.markdown_gerente import process_gerentes_markdown

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


def create_or_update_specific_vectorstore(
    document_type, markdown_file, processor_function
):
    print(f'🔄 Atualizando o vectorstore para {document_type}...')
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)

    if not os.path.isfile(markdown_file):
        print(
            f'⚠️ Arquivo não encontrado ou inválido: {markdown_file}. Ignorando...'
        )
        return

    markdown_text = load_markdown(markdown_file)
    documents = processor_function(markdown_text, markdown_file)

    if not documents:
        print(
            f'❌ Nenhum documento processado para {document_type} a partir de {markdown_file}. Verifique o arquivo Markdown. Vectorstore não será criado/atualizado.'
        )
        return

    index_path = os.path.join(VECTORSTORE_DIR, f'{document_type}_index')

    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if not gemini_api_key:
        raise ValueError(
            '❌ GEMINI_API_KEY não encontrada nas variáveis de ambiente. Verifique seu arquivo .env.'
        )

    embeddings = GoogleGenerativeAIEmbeddings(
        model='models/embedding-001', google_api_key=gemini_api_key
    )

    try:
        FAISS.from_documents(documents, embeddings).save_local(index_path)
        print(
            f'✅ Vectorstore para {document_type} atualizado e salvo em {index_path}.'
        )
    except Exception as e:
        print(
            f'❌ Erro ao criar ou salvar o vectorstore para {document_type}: {e}'
        )


def get_vectorstore(document_type, markdown_file, processor_function):
    index_path = os.path.join(VECTORSTORE_DIR, f'{document_type}_index')

    if not os.path.exists(index_path) or needs_update(
        [markdown_file], index_path
    ):
        print(
            f'ℹ️ Vectorstore para {document_type} não encontrado ou desatualizado. Criando/atualizando...'
        )
        create_or_update_specific_vectorstore(
            document_type, markdown_file, processor_function
        )
        if not os.path.exists(index_path):
            print(
                f'❌ Falha ao criar o vectorstore para {document_type}. Não foi possível carregar de {index_path}.'
            )
            return None

    print(f"✅ Carregando vectorstore salvo de '{index_path}'.")

    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if not gemini_api_key:
        raise ValueError(
            '❌ GEMINI_API_KEY não encontrada nas variáveis de ambiente ao tentar carregar o vectorstore. Verifique seu arquivo .env.'
        )

    embeddings = GoogleGenerativeAIEmbeddings(
        model='models/embedding-001', google_api_key=gemini_api_key
    )

    try:
        return FAISS.load_local(
            index_path, embeddings, allow_dangerous_deserialization=True
        )
    except Exception as e:
        print(f'❌ Erro ao carregar o vectorstore de {index_path}: {e}')
        print(f'ℹ️ Tentando recriar o vectorstore para {document_type}...')
        if not os.path.isfile(markdown_file):
            print(
                f'❌ Arquivo Markdown {markdown_file} não encontrado. Não é possível recriar o vectorstore.'
            )
            return None
        create_or_update_specific_vectorstore(
            document_type, markdown_file, processor_function
        )
        if os.path.exists(index_path):
            try:
                return FAISS.load_local(
                    index_path,
                    embeddings,
                    allow_dangerous_deserialization=True,
                )
            except Exception as e_retry:
                print(
                    f'❌ Erro ao carregar o vectorstore de {index_path} após recriação: {e_retry}'
                )
                return None
        else:
            print(
                f'❌ Falha ao recriar e carregar o vectorstore para {document_type}.'
            )
            return None


def get_iniciativas_vectorstore():
    markdown_file = next(
        (f for f in MARKDOWN_PATH if 'Iniciativas.md' in f), None
    )
    if not markdown_file:
        print(
            "⚠️ Arquivo 'Iniciativas.md' não encontrado em MARKDOWN_PATH. Vectorstore não será carregado."
        )
        return None
    return get_vectorstore(
        'iniciativas', markdown_file, process_iniciativas_markdown
    )


def get_iesgo_vectorstore():
    markdown_file = next(
        (f for f in MARKDOWN_PATH if 'iesgo_structured.md' in f), None
    )
    if not markdown_file:
        print(
            "⚠️ Arquivo 'iesgo_structured.md' não encontrado em MARKDOWN_PATH. Vectorstore não será carregado."
        )
        return None
    return get_vectorstore('iesgo', markdown_file, markdown_recursive_split)


def get_imgg_vectorstore():
    markdown_file = next(
        (f for f in MARKDOWN_PATH if 'imgg_structured.md' in f), None
    )
    if not markdown_file:
        print(
            "⚠️ Arquivo 'imgg_structured.md' não encontrado em MARKDOWN_PATH. Vectorstore não será carregado."
        )
        return None
    return get_vectorstore('imgg', markdown_file, markdown_recursive_split)


def get_indicadores_vectorstore():
    markdown_file = next(
        (f for f in MARKDOWN_PATH if 'indicadores_structured.md' in f), None
    )
    if not markdown_file:
        print(
            "⚠️ Arquivo 'indicadores_structured.md' não encontrado em MARKDOWN_PATH. Vectorstore não será carregado."
        )
        return None
    return get_vectorstore(
        'indicadores', markdown_file, process_indicadores_markdown
    )


def get_diagnostico_imgg_vectorstore():
    markdown_file = next(
        (f for f in MARKDOWN_PATH if 'diagnostico_imgg_structured.md' in f),
        None,
    )
    if not markdown_file:
        print(
            "⚠️ Arquivo 'diagnostico_imgg_structured.md' não encontrado em MARKDOWN_PATH. Vectorstore não será carregado."
        )
        return None
    return get_vectorstore(
        'diagnostico_imgg', markdown_file, markdown_recursive_split
    )


def get_diagnostico_iesgo_vectorstore():
    markdown_file = next(
        (f for f in MARKDOWN_PATH if 'diagnostico_iesgo_structured.md' in f),
        None,
    )
    if not markdown_file:
        print(
            "⚠️ Arquivo 'diagnostico_iesgo_structured.md' não encontrado em MARKDOWN_PATH. Vectorstore não será carregado."
        )
        return None
    return get_vectorstore(
        'diagnostico_iesgo', markdown_file, markdown_recursive_split
    )


def get_oms_vectorstore():
    markdown_file = next(
        (f for f in MARKDOWN_PATH if 'oms_unidade.md' in f), None
    )
    if not markdown_file:
        print(
            "⚠️ Arquivo 'oms_unidade.md' não encontrado em MARKDOWN_PATH. Vectorstore não será carregado."
        )
        return None
    return get_vectorstore('oms', markdown_file, process_oms_markdown)


def get_padroes_vectorstore():
    markdown_file = next((f for f in MARKDOWN_PATH if 'padroes.md' in f), None)
    if not markdown_file:
        print(
            "⚠️ Arquivo 'padroes.md' não encontrado em MARKDOWN_PATH. Vectorstore não será carregado."
        )
        return None
    return get_vectorstore('padroes', markdown_file, process_padroes_markdown)


def get_pta_vectorstore():
    markdown_file = next(
        (f for f in MARKDOWN_PATH if 'pta_descricao_structured.md' in f), None
    )
    if not markdown_file:
        print(
            "⚠️ Arquivo 'pta_descricao_structured.md' não encontrado em MARKDOWN_PATH. Vectorstore não será carregado."
        )
        return None
    return get_vectorstore('pta', markdown_file, process_pta_markdown)


def get_riscos_vectorstore():
    markdown_file = next(
        (f for f in MARKDOWN_PATH if 'riscos_structured.md' in f), None
    )
    if not markdown_file:
        print(
            "⚠️ Arquivo 'riscos_structured.md' não encontrado em MARKDOWN_PATH. Vectorstore não será carregado."
        )
        return None
    return get_vectorstore('riscos', markdown_file, process_riscos_markdown)


def get_estatuto_social_vectorstore():
    markdown_file = next(
        (f for f in MARKDOWN_PATH if 'estatuto_social_structured.md' in f),
        None,
    )
    if not markdown_file:
        print(
            "⚠️ Arquivo 'estatuto_social_structured.md' não encontrado em MARKDOWN_PATH. Vectorstore não será carregado."
        )
        return None
    return get_vectorstore(
        'estatuto_social', markdown_file, process_estatuto_markdown
    )


def get_estrutura_processos_vectorstore():
    markdown_file = next(
        (f for f in MARKDOWN_PATH if 'estrutura_processos_structured.md' in f),
        None,
    )
    if not markdown_file:
        print(
            "⚠️ Arquivo 'estrutura_processos_structured.md' não encontrado em MARKDOWN_PATH. Vectorstore não será carregado."
        )
        return None
    return get_vectorstore(
        'estrutura_processos', markdown_file, markdown_recursive_split
    )


def get_regimento_interno_vectorstore():
    markdown_file = next(
        (f for f in MARKDOWN_PATH if 'regimento_interno_structured.md' in f),
        None,
    )
    if not markdown_file:
        print(
            "⚠️ Arquivo 'regimento_interno_structured.md' não encontrado em MARKDOWN_PATH. Vectorstore não será carregado."
        )
        return None
    return get_vectorstore(
        'regimento_interno', markdown_file, process_regimento_markdown
    )


# >>>>>>>>>>>> ADICIONE ESTA FUNÇÃO <<<<<<<<<<<<<<
def get_gerentes_vectorstore():
    markdown_file = next(
        (f for f in MARKDOWN_PATH if 'colaborador_unidade_structured.md' in f),
        None,
    )
    if not markdown_file:
        print(
            "⚠️ Arquivo 'colaborador_unidade_structured.md' não encontrado em MARKDOWN_PATH. Vectorstore não será carregado."
        )
        return None
    return get_vectorstore(
        'gerentes', markdown_file, process_gerentes_markdown
    )


if __name__ == '__main__':
    print('Tentando inicializar e carregar todos os vectorstores...')

    if not MARKDOWN_PATH or not VECTORSTORE_DIR:
        print(
            '❌ MARKDOWN_PATH ou VECTORSTORE_DIR não estão configurados em config.config.py. Testes não podem prosseguir.'
        )
    else:
        base_doc_path = ''
        if (
            MARKDOWN_PATH
            and isinstance(MARKDOWN_PATH, list)
            and len(MARKDOWN_PATH) > 0
        ):
            first_path_dir = os.path.dirname(MARKDOWN_PATH[0])
            if first_path_dir:
                base_doc_path = first_path_dir
            else:
                base_doc_path = '.'

        elif MARKDOWN_PATH and isinstance(MARKDOWN_PATH, str):
            base_doc_path = os.path.dirname(MARKDOWN_PATH)
            if not base_doc_path:
                base_doc_path = '.'

        if not base_doc_path:
            print(
                '⚠️ Não foi possível determinar um diretório base para os arquivos Markdown de exemplo a partir de MARKDOWN_PATH.'
            )
            base_doc_path = 'documentation'

        os.makedirs(base_doc_path, exist_ok=True)
        print(
            f'ℹ️ Diretório base para arquivos de exemplo: {os.path.abspath(base_doc_path)}'
        )

        sample_files_content = {
            'Iniciativas.md': '# Iniciativa 1\nConteúdo da iniciativa 1.',
            'iesgo_structured.md': '# IESGO\nConteúdo sobre IESGO.',
            'imgg_structured.md': '# IMGG\nConteúdo sobre IMGG.',
            'indicadores_structured.md': '# Indicador X\nDetalhes do indicador X.',
            'diagnostico_imgg_structured.md': '# Diagnóstico IMGG\nAnálise IMGG.',
            'diagnostico_iesgo_structured.md': '# Diagnóstico IESGO\nAnálise IESGO.',
            'oms_unidade.md': '# OMS Unidade\nInformações OMS.',
            'padroes.md': '# Padrão Y\nDescrição do Padrão Y.',
            'pta_descricao_structured.md': '# PTA\nPlano de Trabalho Anual.',
            'riscos_structured.md': '# Risco Z\nAnálise de Risco Z.',
            'estatuto_social_structured.md': '## ESTATUTO SOCIAL\nConteúdo do estatuto social.',
            'estrutura_processos_structured.md': '## ESTRUTURA DE PROCESSOS\nConteúdo da estrutura de processos.',
            'regimento_interno_structured.md': '## REGIMENTO INTERNO\nConteúdo do regimento interno.',
            'colaborador_unidade_structured.md': '## Unidade: Exemplo Unidade\nResponsável: Fulano\nEquipe: Fulano, Beltrano',
        }

        for filename_pattern, content in sample_files_content.items():
            actual_file_path_from_config = next(
                (f for f in MARKDOWN_PATH if filename_pattern in f), None
            )

            if actual_file_path_from_config:
                target_file_path = actual_file_path_from_config
            else:
                target_file_path = os.path.join(
                    base_doc_path, filename_pattern
                )
                print(
                    f"❓ Padrão de arquivo '{filename_pattern}' não encontrado em MARKDOWN_PATH. Usando caminho de exemplo: {target_file_path}"
                )

            os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

            if not os.path.exists(target_file_path):
                try:
                    with open(target_file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f'📄 Arquivo de exemplo criado: {target_file_path}')
                except Exception as e:
                    print(
                        f'❌ Erro ao criar arquivo de exemplo {target_file_path}: {e}'
                    )

        vs_iniciativas = get_iniciativas_vectorstore()
        if vs_iniciativas:
            print(
                f'👍 Vectorstore de Iniciativas carregado: {type(vs_iniciativas)}'
            )

        vs_iesgo = get_iesgo_vectorstore()
        if vs_iesgo:
            print(f'👍 Vectorstore IESGO carregado: {type(vs_iesgo)}')

        vs_imgg = get_imgg_vectorstore()
        if vs_imgg:
            print(f'👍 Vectorstore IMGG carregado: {type(vs_imgg)}')

        vs_indicadores = get_indicadores_vectorstore()
        if vs_indicadores:
            print(
                f'👍 Vectorstore Indicadores carregado: {type(vs_indicadores)}'
            )

        vs_diag_imgg = get_diagnostico_imgg_vectorstore()
        if vs_diag_imgg:
            print(
                f'👍 Vectorstore Diagnóstico IMGG carregado: {type(vs_diag_imgg)}'
            )

        vs_diag_iesgo = get_diagnostico_iesgo_vectorstore()
        if vs_diag_iesgo:
            print(
                f'👍 Vectorstore Diagnóstico IESGO carregado: {type(vs_diag_iesgo)}'
            )

        vs_oms = get_oms_vectorstore()
        if vs_oms:
            print(f'👍 Vectorstore OMS carregado: {type(vs_oms)}')

        vs_padroes = get_padroes_vectorstore()
        if vs_padroes:
            print(f'👍 Vectorstore Padrões carregado: {type(vs_padroes)}')

        vs_pta = get_pta_vectorstore()
        if vs_pta:
            print(f'👍 Vectorstore PTA carregado: {type(vs_pta)}')

        vs_riscos = get_riscos_vectorstore()
        if vs_riscos:
            print(f'👍 Vectorstore Riscos carregado: {type(vs_riscos)}')

        vs_estatuto = get_estatuto_social_vectorstore()
        if vs_estatuto:
            print(
                f'👍 Vectorstore Estatuto Social carregado: {type(vs_estatuto)}'
            )

        vs_estrutura_processos = get_estrutura_processos_vectorstore()
        if vs_estrutura_processos:
            print(
                f'👍 Vectorstore Estrutura de Processos carregado: {type(vs_estrutura_processos)}'
            )

        vs_regimento_interno = get_regimento_interno_vectorstore()
        if vs_regimento_interno:
            print(
                f'👍 Vectorstore Regimento Interno carregado: {type(vs_regimento_interno)}'
            )

        # >>>> Teste de carregamento do vectorstore de gerentes
        vs_gerentes = get_gerentes_vectorstore()
        if vs_gerentes:
            print(f'👍 Vectorstore Gerentes carregado: {type(vs_gerentes)}')

        print('\n✅ Teste de inicialização e carregamento concluído.')
