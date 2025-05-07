from langchain_core.chat_history import InMemoryChatMessageHistory
from memory.truncation import truncate_history_by_tokens
from memory.summarization import summarize_history
from memory.compaction import compact_consecutive_messages
from memory.filters import filter_irrelevant_messages

session_histories = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in session_histories:
        session_histories[session_id] = InMemoryChatMessageHistory()
    return session_histories[session_id]

def save_session_history(session_id: str, history: InMemoryChatMessageHistory, summary: str = None, max_tokens: int = 1000):
    if summary:
        history.messages = [{"role": "system", "content": summary}]
    else:
        truncate_history_by_tokens(history, max_tokens=max_tokens)
    session_histories[session_id] = history

def add_message_to_history(session_id: str, message: dict, max_tokens: int = 1000, summary_threshold: int = 10):
    history = get_session_history(session_id)
    history.add_message(message)
    compact_consecutive_messages(history)
    filter_irrelevant_messages(history)
    if len(history.messages) > summary_threshold:
        summary = summarize_history(history)
        save_session_history(session_id, history, summary=summary, max_tokens=max_tokens)
    else:
        save_session_history(session_id, history, max_tokens=max_tokens)