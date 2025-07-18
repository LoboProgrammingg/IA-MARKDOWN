import os

MARKDOWN_PATH = [
    'documentation/Iniciativas.md',
    'documentation/iesgo_structured.md',
    'documentation/imgg_structured.md',
    'documentation/indicadores_structured.md',
    'documentation/diagnostico_imgg_structured.md',
    'documentation/diagnostico_iesgo_structured.md',
    'documentation/oms_unidade.md',
    'documentation/riscos_structured.md',
    'documentation/padroes.md',
    'documentation/pta_descricao_structured.md',
    'documentation/estatuto_social_structured.md',
    'documentation/estrutura_processos_structured.md',
    'documentation/regimento_interno_structured.md',
    'documentation/colaborador_unidade_structured.md',
]

VECTORSTORE_DIR = 'vectorstore'
FAISS_INDEX_PATH = os.path.join(VECTORSTORE_DIR, 'faiss_index')

USERS_FILE = 'user.json'
