import tiktoken
from langchain.chat_models import ChatOpenAI

def filter_and_combine_documents(documents, max_combined_tokens=2000, model="gpt-4o-mini"):
    encoder = tiktoken.encoding_for_model(model)
    combined_text = []
    total_tokens = 0

    for doc in documents:
        doc_content = doc.page_content if hasattr(doc, 'page_content') else doc
        doc_tokens = len(encoder.encode(doc_content))
        if total_tokens + doc_tokens > max_combined_tokens:
            break
        combined_text.append(doc_content)
        total_tokens += doc_tokens

    return "\n\n".join(combined_text)

def summarize_documents_in_one_call(documents, model="gpt-4o-mini", max_tokens_summary=700, max_combined_tokens=2000):
    combined_text = filter_and_combine_documents(documents, max_combined_tokens=max_combined_tokens, model=model)

    llm = ChatOpenAI(model=model, temperature=0, max_tokens=max_tokens_summary)
    prompt = f"Resuma sobre o IMGG e retorne um contexto coeso para a IA:\n\n{combined_text}"
    return llm.predict(prompt)