from langchain_core.chat_history import InMemoryChatMessageHistory

def filter_irrelevant_messages(history: InMemoryChatMessageHistory):
    filtered_messages = []
    for message in history.messages:
        if len(message["content"].strip()) < 5:
            continue
        if message["content"].lower() in ["ok", "entendi", "certo"]:
            continue
        filtered_messages.append(message)
    history.messages = filtered_messages