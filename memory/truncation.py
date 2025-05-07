import tiktoken
from langchain_core.chat_history import InMemoryChatMessageHistory

def truncate_history_by_tokens(history: InMemoryChatMessageHistory, max_tokens: int):
    encoder = tiktoken.encoding_for_model("gpt-4o-mini")
    total_tokens = 0
    truncated_messages = []
    for message in reversed(history.messages):
        message_tokens = len(encoder.encode(message["content"]))
        if total_tokens + message_tokens > max_tokens:
            break
        truncated_messages.append(message)
        total_tokens += message_tokens
    history.messages = list(reversed(truncated_messages))