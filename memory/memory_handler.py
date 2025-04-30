from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import BaseMessage

class LimitedMemoryChatHistory(InMemoryChatMessageHistory):
    def __init__(self, max_messages=5):
        super().__init__()
        self.max_messages = max_messages

    def add_message(self, message: BaseMessage) -> None:
        super().add_message(message)
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

session_histories = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in session_histories:
        session_histories[session_id] = LimitedMemoryChatHistory(max_messages=5)
    return session_histories[session_id]

def save_session_history(session_id: str, history: InMemoryChatMessageHistory):
    session_histories[session_id] = history