from langchain_core.chat_history import InMemoryChatMessageHistory

session_histories = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in session_histories:
        session_histories[session_id] = InMemoryChatMessageHistory()

    return session_histories[session_id]

def save_session_history(session_id: str, history: InMemoryChatMessageHistory):
    session_histories[session_id] = history

    if len(history.messages) > 5:
        history.messages = history.messages[-5:]
