import re
import streamlit as st
import uuid
from pipeline.pipeline import get_response_stream

st.set_page_config(page_title="MTI Assistente Estratégico", page_icon="🤖", layout="wide")

def process_response_text(text):
    text = re.sub(r"(Unidade:.*)", r"<span style='color: #f4b41a; font-weight: bold; font-size: 1.3rem;'>\1</span>", text)
    text = re.sub(r"(Objetivo Estratégico:.*)", r"<span style='color: #f4b41a; font-weight: bold; font-size: 1.3rem;'>\1</span>", text)
    text = re.sub(r"(Perspectiva:.*)", r"<span style='color: #f4b41a; font-weight: bold; font-size: 1.3rem;'>\1</span>", text)
    text = re.sub(r"(Risco Estratégico:.*)", r"<span style='color: #f4b41a; font-weight: bold; font-size: 1.3rem;'>\1</span>", text)
    text = re.sub(r"(Plano de Negócio:.*)", r"<span style='color: #f4b41a; font-weight: bold; font-size: 1.3rem;'>\1</span>", text)
    text = re.sub(r'##', '', text)
    return text

def set_page_style():
    st.markdown("""
    <style>
    body {
        background-color: #121212;
        font-family: 'Arial', sans-serif;
    }
    header, footer {
        visibility: hidden;
    }
    .chat-title {
        font-size: 2rem;
        font-weight: bold;
        color: #f4b41a;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .chat-container {
        background-color: #1c1c1c;
        border-radius: 16px;
        height: 70vh;
        overflow-y: auto;
        padding: 2rem;
        box-shadow: 0 0 12px rgba(244, 180, 26, 0.2);
        margin-bottom: 1rem;
        font-size: 1.2rem;
        color: #fff;
        display: flex;
        flex-direction: column;
    }
    .chat-bubble {
        padding: 16px 24px;
        border-radius: 20px;
        margin: 10px 0;
        font-size: 1.1rem;
        line-height: 1.6;
        word-wrap: break-word;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
        width: 100%;
    }
    .user {
        background-color: #f4b41a;
        color: #000;
        align-self: flex-end;
        border-bottom-right-radius: 0;
    }
    .ai {
        background-color: #143d59;
        color: #fff;
        align-self: flex-start;
        border-bottom-left-radius: 0;
    }
    .chat-scroll {
        display: flex;
        flex-direction: column;
        height: 100%;
        justify-content: flex-end;
    }
    </style>
    """, unsafe_allow_html=True)

def display_chat():
    with st.container():
        st.markdown('<div class="chat-container chat-scroll">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            css_class = "user" if msg["role"] == "user" else "ai"
            content = process_response_text(msg["content"]) if msg["role"] == "ai" else msg["content"]
            st.markdown(f'<div class="chat-bubble {css_class}">{content}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def handle_user_input(user_input):
    st.session_state.messages.append({"role": "user", "content": user_input})

    st.markdown(f'<div class="chat-bubble user">{user_input}</div>', unsafe_allow_html=True)

    placeholder = st.empty()
    response_text = ""

    try:
        session_id = st.session_state.session_id
        for chunk in get_response_stream(user_input, session_id):
            response_text += chunk
            processed_text = process_response_text(response_text)
            placeholder.markdown(f'<div class="chat-bubble ai">{processed_text}</div>', unsafe_allow_html=True)
    except Exception as e:
        response_text = "Desculpe, ocorreu um erro ao processar sua solicitação."
        st.error(f"Erro: {e}")
        print(f"[DEBUG] Erro durante o processamento: {e}")

    st.session_state.messages.append({"role": "ai", "content": response_text})

set_page_style()
st.markdown('<div class="chat-title">🤖 MTI Assistente Estratégico</div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

display_chat()

user_input = st.chat_input("Digite sua pergunta ...")
if user_input:
    handle_user_input(user_input)