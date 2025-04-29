import os

def load_markdown(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def needs_update(markdown_path, vectorstore_path):
    return (not os.path.exists(vectorstore_path) or 
            os.path.getmtime(markdown_path) > os.path.getmtime(vectorstore_path))