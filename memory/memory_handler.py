from langchain_core.chat_history import InMemoryChatMessageHistory

# Dicionário para armazenar históricos de sessões
session_histories = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """
    Retorna o histórico de mensagens da sessão especificada.
    Se a sessão não existir, cria um novo histórico.
    """
    if session_id not in session_histories:
        session_histories[session_id] = InMemoryChatMessageHistory()

    return session_histories[session_id]

def save_session_history(session_id: str, history: InMemoryChatMessageHistory):
    """
    Salva o histórico de mensagens da sessão especificada e
    limita o histórico a no máximo 5 mensagens.
    """
    # Limitar o histórico a no máximo 5 mensagens
    truncate_history(history, max_messages=5)

    # Salvar o histórico atualizado na sessão
    session_histories[session_id] = history

def add_message_to_history(session_id: str, message: dict):
    """
    Adiciona uma mensagem ao histórico e garante que o histórico
    não contenha mais de 5 mensagens.
    """
    # Recuperar o histórico da sessão
    history = get_session_history(session_id)

    # Adicionar a nova mensagem ao histórico
    history.add_message(message)

    # Salvar o histórico atualizado
    save_session_history(session_id, history)

def truncate_history(history: InMemoryChatMessageHistory, max_messages: int):
    """
    Trunca o histórico de mensagens para manter apenas as `max_messages` mais recentes.
    """
    if len(history.messages) > max_messages:
        # Manter apenas as últimas `max_messages` mensagens
        history.messages = history.messages[-max_messages:]