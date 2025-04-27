from langchain_core.chat_history import InMemoryChatMessageHistory

store = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

def save_session_history(session_id: str, history: InMemoryChatMessageHistory):
    store[session_id] = history

def compact_history(history: InMemoryChatMessageHistory, max_messages=50):
    if len(history.messages) > max_messages:
        history.messages = history.messages[-max_messages:]