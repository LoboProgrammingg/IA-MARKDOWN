from langchain_core.chat_history import InMemoryChatMessageHistory

session_histories = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in session_histories:
        session_histories[session_id] = InMemoryChatMessageHistory()

    return session_histories[session_id]

def save_session_history(session_id: str, history: InMemoryChatMessageHistory):
    truncate_history(history, max_messages=5)

    session_histories[session_id] = history

def add_message_to_history(session_id: str, message: dict):
    history = get_session_history(session_id)

    history.add_message(message)

    save_session_history(session_id, history)

def truncate_history(history: InMemoryChatMessageHistory, max_messages: int):
    if len(history.messages) > max_messages:
        history.messages = history.messages[-max_messages:]
