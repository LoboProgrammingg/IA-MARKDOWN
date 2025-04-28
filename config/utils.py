def join_documents(input: dict) -> dict:
    if 'contexto' in input and isinstance(input['contexto'], list):
        input['contexto'] = '\n\n'.join([doc.page_content for doc in input['contexto']])
    return input