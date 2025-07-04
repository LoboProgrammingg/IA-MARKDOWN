from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from prompt.prompt_template import CHAT_SUMMARIZATION_PROMPT


def summarize_history(history: InMemoryChatMessageHistory) -> str:
    llm = ChatGoogleGenerativeAI(
        model='gemini-2.5-flash-preview-04-17', temperature=0, max_tokens=800
    )
    full_history = '\n'.join(
        [f"{msg['role']}: {msg['content']}" for msg in history.messages]
    )
    summary = llm(CHAT_SUMMARIZATION_PROMPT.format(history=full_history))
    return summary
