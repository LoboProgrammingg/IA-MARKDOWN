import re
import streamlit as st
import uuid  # Para gerar um identificador único para cada sessão
from pipeline.pipeline import get_response_stream

# Configurações da página
st.set_page_config(page_title="MTI Assistente Estratégico", page_icon="🤖", layout="wide")

# Função para processar o texto da resposta da IA
def process_response_text(text):
    """Destaca palavras-chave como 'Unidade', 'Objetivo Estratégico', etc., com formatação customizada."""
    text = re.sub(r"(Unidade:.*)", r"<span style='color: #f4b41a; font-weight: bold; font-size: 1.3rem;'>\1</span>", text)
    text = re.sub(r"(Objetivo Estratégico:.*)", r"<span style='color: #f4b41a; font-weight: bold; font-size: 1.3rem;'>\1</span>", text)
    text = re.sub(r"(Perspectiva:.*)", r"<span style='color: #f4b41a; font-weight: bold; font-size: 1.3rem;'>\1</span>", text)
    text = re.sub(r"(Risco Estratégico:.*)", r"<span style='color: #f4b41a; font-weight: bold; font-size: 1.3rem;'>\1</span>", text)
    text = re.sub(r"(Plano de Negócio:.*)", r"<span style='color: #f4b41a; font-weight: bold; font-size: 1.3rem;'>\1</span>", text)
    text = re.sub(r'##', '', text)  # Remove hashtags (##)
    return text

# Função para configurar o estilo da página
def set_page_style():
    """Define o estilo personalizado do Streamlit."""
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

# Função para exibir as mensagens do chat
def display_chat():
    """Exibe as mensagens no chat."""
    with st.container():
        st.markdown('<div class="chat-container chat-scroll">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            css_class = "user" if msg["role"] == "user" else "ai"
            content = process_response_text(msg["content"]) if msg["role"] == "ai" else msg["content"]
            st.markdown(f'<div class="chat-bubble {css_class}">{content}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Função para tratar o input do usuário e obter a resposta da IA
def handle_user_input(user_input):
    """Recebe o input do usuário, chama a IA e exibe a resposta."""
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Exibe a mensagem do usuário imediatamente
    st.markdown(f'<div class="chat-bubble user">{user_input}</div>', unsafe_allow_html=True)

    # Placeholder para resposta da IA
    placeholder = st.empty()
    response_text = ""

    try:
        # Obtém o ID da sessão
        session_id = st.session_state.session_id

        # Chama o pipeline com streaming
        for chunk in get_response_stream(user_input, session_id):
            response_text += chunk
            processed_text = process_response_text(response_text)
            placeholder.markdown(f'<div class="chat-bubble ai">{processed_text}</div>', unsafe_allow_html=True)
    except Exception as e:
        response_text = "Desculpe, ocorreu um erro ao processar sua solicitação."
        st.error(f"Erro: {e}")

    st.session_state.messages.append({"role": "ai", "content": response_text})

# Configuração da interface de usuário
set_page_style()
st.markdown('<div class="chat-title">🤖 MTI Assistente Estratégico</div>', unsafe_allow_html=True)

# Inicializa o estado da sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Gera um ID único para a sessão, se não existir
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())  # Gera um UUID único para a sessão

# Exibe o chat
display_chat()

# Captura a entrada do usuário
user_input = st.chat_input("Digite sua pergunta ...")
if user_input:
    handle_user_input(user_input)