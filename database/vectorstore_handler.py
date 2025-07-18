import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from typing import List
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


# --- Configuração Central ---

# O diretório dos vectorstores agora fica dentro da pasta 'database'
# para melhor organização.
VECTORSTORE_DIR = os.path.join('database', 'vector_data')

def validate_env_variable(var_name: str) -> str:
    """Valida e retorna uma variável de ambiente, levantando um erro se não for encontrada."""
    value = os.getenv(var_name)
    if not value:
        raise ValueError(f"A variável de ambiente '{var_name}' não está definida.")
    return value

# Instancia o modelo de embedding do Gemini.
print("--- Carregando modelo de embedding do Gemini... ---")
try:
    gemini_api_key = validate_env_variable('GEMINI_API_KEY')
    
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=gemini_api_key
    )
    print("✅ Modelo de embedding do Gemini carregado com sucesso.")
except Exception as e:
    print(f"❌ Falha crítica ao carregar o modelo de embedding do Gemini: {e}")
    embeddings = None

# --- Funções de Manipulação do Vectorstore ---

def get_vectorstore_path_by_name(name: str) -> str:
    """Gera o caminho completo para um vectorstore específico."""
    return os.path.join(VECTORSTORE_DIR, name)

def create_vectorstore(chunks: List[Document], path: str):
    """Cria e salva um novo vectorstore FAISS a partir de uma lista de documentos."""
    if not embeddings:
        raise RuntimeError("O modelo de embedding não foi carregado.")
    
    print(f"   - Criando vectorstore FAISS com {len(chunks)} chunks...")
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(path)
    print(f"   - Vectorstore salvo localmente em: {path}")

def load_vectorstore(path: str):
    """Carrega um vectorstore FAISS existente do disco."""
    if not embeddings:
        raise RuntimeError("O modelo de embedding não foi carregado.")
    
    if not os.path.exists(path):
        return None
    
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)

# --- Funções Getter para cada Vectorstore ---
# CORREÇÃO: Os nomes foram alinhados com os gerados pelo ingestion.py

def get_iniciativas_vectorstore():
    return load_vectorstore(get_vectorstore_path_by_name("iniciativas"))

def get_iesgo_vectorstore():
    return load_vectorstore(get_vectorstore_path_by_name("iesgo"))

def get_imgg_vectorstore():
    return load_vectorstore(get_vectorstore_path_by_name("imgg"))

def get_indicadores_vectorstore():
    return load_vectorstore(get_vectorstore_path_by_name("indicadores"))

def get_diagnostico_imgg_vectorstore():
    return load_vectorstore(get_vectorstore_path_by_name("diagnostico_imgg"))

def get_diagnostico_iesgo_vectorstore():
    return load_vectorstore(get_vectorstore_path_by_name("diagnostico_iesgo"))

def get_oms_vectorstore():
    # Corrigido de "oms" para "oms_unidade"
    return load_vectorstore(get_vectorstore_path_by_name("oms_unidade"))

def get_padroes_vectorstore():
    return load_vectorstore(get_vectorstore_path_by_name("padroes"))

def get_pta_vectorstore():
    # Corrigido de "pta" para "pta_descricao"
    return load_vectorstore(get_vectorstore_path_by_name("pta_descricao"))

def get_riscos_vectorstore():
    return load_vectorstore(get_vectorstore_path_by_name("riscos"))

def get_estatuto_social_vectorstore():
    return load_vectorstore(get_vectorstore_path_by_name("estatuto_social"))

def get_estrutura_processos_vectorstore():
    return load_vectorstore(get_vectorstore_path_by_name("estrutura_processos"))

def get_regimento_interno_vectorstore():
    return load_vectorstore(get_vectorstore_path_by_name("regimento_interno"))

def get_gerentes_vectorstore():
    # Corrigido de "gerentes" para "colaborador_unidade"
    return load_vectorstore(get_vectorstore_path_by_name("colaborador_unidade"))

# Esta função já estava correta, mas a mantemos para consistência
def get_colaborador_unidade_vectorstore():
    return load_vectorstore(get_vectorstore_path_by_name("colaborador_unidade"))