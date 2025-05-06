import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_markdown(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def needs_update(markdown_paths, vectorstore_path):
    if not os.path.exists(vectorstore_path):
        logging.info(f"Arquivo de vetor não encontrado: {vectorstore_path}. Atualização necessária.")
        return True

    for markdown_file in markdown_paths:
        if not os.path.isfile(markdown_file):
            logging.warning(f"Arquivo inválido ou inexistente: {markdown_file}. Ignorando...")
            continue

        if os.path.getmtime(markdown_file) > os.path.getmtime(vectorstore_path):
            logging.info(f"Arquivo Markdown atualizado: {markdown_file}. Atualização necessária.")
            return True

    logging.info("Nenhuma atualização necessária. Todos os arquivos estão atualizados.")
    return False