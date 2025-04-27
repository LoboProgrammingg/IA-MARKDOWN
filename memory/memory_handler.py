from langchain_core.chat_history import InMemoryChatMessageHistory

# Dicionário para manter o histórico em memória
session_histories = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """Obtém ou cria um histórico de mensagens para um ID de sessão."""
    if session_id not in session_histories:
        session_histories[session_id] = InMemoryChatMessageHistory()
    return session_histories[session_id]

def save_session_history(session_id: str, history: InMemoryChatMessageHistory):
    """Salva o histórico de mensagens na memória."""
    session_histories[session_id] = history