import os

def load_markdown(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def needs_update(markdown_paths, vectorstore_path):
    if not os.path.exists(vectorstore_path):
        return True

    for markdown_file in markdown_paths:
        if not os.path.isfile(markdown_file):
            continue  # Ignora arquivos inválidos ou inexistentes
        if os.path.getmtime(markdown_file) > os.path.getmtime(vectorstore_path):
            return True

    return False