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


def save_session_history(
    session_id: str,
    history: InMemoryChatMessageHistory,
    summary: str = None,
    max_tokens: int = 1000,
    keep_last_n: int = 6,
):
    non_system_msgs = [
        msg for msg in history.messages if msg['role'] != 'system'
    ]
    if summary:
        summary_msg = {'role': 'system', 'content': summary, 'type': 'summary'}
        last_messages = non_system_msgs[-keep_last_n:]
        history.messages = [summary_msg] + last_messages
    else:
        history.messages = non_system_msgs[-keep_last_n:]
        truncate_history_by_tokens(history, max_tokens=max_tokens)
    session_histories[session_id] = history


def build_memory_for_prompt(session_id: str, max_last_n: int = 6):
    history = get_session_history(session_id)
    summary = None
    last_msgs = []
    for msg in history.messages:
        if msg.get('role') == 'system' and msg.get('type') == 'summary':
            summary = msg
        elif msg.get('role') != 'system':
            last_msgs.append(msg)

    def serialize(messages):
        output = []
        for m in messages:
            role = m.get('role', 'user').capitalize()
            content = m.get('content', '')
            output.append(f'{role}: {content}')
        return '\n'.join(output)

    parts = []
    if summary:
        parts.append(serialize([summary]))
    if last_msgs:
        parts.append(serialize(last_msgs[-max_last_n:]))
    return '\n\n'.join(parts)


def add_message_to_history(
    session_id: str,
    message: dict,
    max_tokens: int = 1000,
    summary_threshold: int = 10,
    keep_last_n: int = 6,
):
    history = get_session_history(session_id)
    history.add_message(message)
    compact_consecutive_messages(history)
    filter_irrelevant_messages(history)
    non_system_messages = [
        msg for msg in history.messages if msg['role'] != 'system'
    ]
    if len(non_system_messages) > summary_threshold:
        summary = summarize_history(history)
        save_session_history(
            session_id,
            history,
            summary=summary,
            max_tokens=max_tokens,
            keep_last_n=keep_last_n,
        )
    else:
        save_session_history(
            session_id, history, max_tokens=max_tokens, keep_last_n=keep_last_n
        )
