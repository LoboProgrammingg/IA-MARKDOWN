import os
import shutil
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .vectorstore_handler import (
    create_vectorstore,
    get_vectorstore_path_by_name,
    VECTORSTORE_DIR # Importa a constante atualizada
)

# --- Importação dos Processadores Customizados ---
from .metadata_split.markdown_gerente import process_gerentes_markdown
from .metadata_split.markdown_indicadores import process_indicadores_markdown
from .metadata_split.markdown_padroes import process_padroes_markdown
from .metadata_split.markdown_processor_estatuto_social import process_estatuto_markdown
from .metadata_split.markdown_processor_estrutura import process_estrutura_markdown
from .metadata_split.markdown_processor_iniciativas import process_iniciativas_markdown
from .metadata_split.markdown_processor_oms import process_oms_markdown
from .metadata_split.markdown_processor_pta import process_pta_markdown
from .metadata_split.markdown_regimento import process_regimento_markdown
from .metadata_split.markdown_riscos import process_riscos_markdown
from .metadata_split.markdown_recursive import markdown_recursive_split

DOCUMENTATION_DIR = "documentation"

# --- Mapeamento de Processadores ---
PROCESSOR_MAP = {
    "colaborador_unidade_structured.md": process_gerentes_markdown,
    "indicadores_structured.md": process_indicadores_markdown,
    "padroes.md": process_padroes_markdown,
    "estatuto_social_structured.md": process_estatuto_markdown,
    "estrutura_processos_structured.md": process_estrutura_markdown,
    "Iniciativas.md": process_iniciativas_markdown,
    "oms_unidade.md": process_oms_markdown,
    "pta_descricao_structured.md": process_pta_markdown,
    "regimento_interno_structured.md": process_regimento_markdown,
    "riscos_structured.md": process_riscos_markdown,
    "diagnostico_imgg_structured.md": markdown_recursive_split,
    "diagnostico_iesgo_structured.md": markdown_recursive_split,
    "iesgo_structured.md": markdown_recursive_split,
    "imgg_structured.md": markdown_recursive_split
}

def discover_markdown_files() -> list[str]:
    """Descobre todos os arquivos .md no diretório de documentação."""
    if not os.path.exists(DOCUMENTATION_DIR):
        print(f"⚠️ Diretório '{DOCUMENTATION_DIR}' não encontrado.")
        return []
    return [os.path.join(DOCUMENTATION_DIR, f) for f in os.listdir(DOCUMENTATION_DIR) if f.endswith('.md')]

def process_and_ingest_documents():
    """
    Função principal que orquestra todo o processo de reindexação.
    """
    print("🚀 Iniciando processo de reindexação para FAISS...")

    # CORREÇÃO: Adiciona a lógica de limpeza para garantir uma reindexação limpa
    if os.path.exists(VECTORSTORE_DIR):
        print(f"🧹 Limpando diretório de vectorstore antigo: '{VECTORSTORE_DIR}'")
        shutil.rmtree(VECTORSTORE_DIR)
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    print(f"✅ Diretório de vectorstore '{VECTORSTORE_DIR}' recriado.")

    markdown_files = discover_markdown_files()
    if not markdown_files:
        print("🟡 Nenhum documento para processar. Processo de reindexação concluído.")
        return {"status": "success", "message": "Nenhum documento encontrado para processar."}

    print(f"📚 Encontrados {len(markdown_files)} documentos para processar.")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    for file_path in markdown_files:
        try:
            file_name = os.path.basename(file_path)
            vectorstore_name = os.path.splitext(file_name)[0].lower().replace('_structured', '')
            
            print(f"\n📄 Processando '{file_name}' para o vectorstore '{vectorstore_name}'...")
            
            chunks = []
            if file_name in PROCESSOR_MAP:
                processor_func = PROCESSOR_MAP[file_name]
                print(f"   - Usando processador customizado: {processor_func.__name__}")
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                chunks = processor_func(content, file_path)
                print(f"   - Processador customizado gerou {len(chunks)} documentos (chunks).")
            else:
                print(f"   - 🟡 Nenhum processador customizado mapeado. Usando carregador genérico.")
                loader = UnstructuredMarkdownLoader(file_path, mode="elements")
                docs = loader.load()
                chunks = text_splitter.split_documents(docs)
                print(f"   - Carregador genérico dividiu o documento em {len(chunks)} chunks.")

            if not chunks:
                print(f"   - 🟡 Nenhum chunk gerado para '{file_name}'. Pulando.")
                continue

            # A função get_vectorstore_path_by_name usará a nova constante VECTORSTORE_DIR
            vectorstore_path = get_vectorstore_path_by_name(vectorstore_name)
            create_vectorstore(chunks, vectorstore_path)
            
            print(f"   - ✅ Vectorstore para '{vectorstore_name}' criado com sucesso.")

        except Exception as e:
            print(f"   - ❌ Erro ao processar o arquivo '{file_path}': {e}")

    print("\n🎉 Processo de reindexação para FAISS concluído com sucesso!")
    return {"status": "success", "message": f"{len(markdown_files)} documentos processados."}