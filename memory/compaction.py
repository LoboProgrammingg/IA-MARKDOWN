from langchain_core.chat_history import InMemoryChatMessageHistory

def compact_consecutive_messages(history: InMemoryChatMessageHistory):
    compacted_messages = []
    for message in history.messages:
        if compacted_messages and compacted_messages[-1]["role"] == message["role"]:
            compacted_messages[-1]["content"] += f"\n{message['content']}"
        else:
            compacted_messages.append(message)
    history.messages = compacted_messages