from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain.chat_models import ChatOpenAI
from prompt.prompt_template import CHAT_SUMMARIZATION_PROMPT

def summarize_history(history: InMemoryChatMessageHistory) -> str:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, max_tokens=1000)
    full_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history.messages])
    summary = llm(CHAT_SUMMARIZATION_PROMPT.format(history=full_history))
    return summary