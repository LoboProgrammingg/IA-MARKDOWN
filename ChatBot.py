import os
import sys
import json
import base64
import streamlit as st
import uuid
import datetime
from passlib.context import CryptContext
import markdown2

LOGO_PATH = "documentation/mti.png"
USERS_FILE = os.path.join("user.json")
HISTORY_DIR = "histories"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

THEME = {
    'PRIMARY': "#233458",
    'SECONDARY': "#2A3759",
    'ACCENT': "#69E5FF",
    'ACCENT2': "#7B61FF",
    'CYBER': "#46FFB9",
    'BACKGROUND': "#141926",
    'SURFACE': "rgba(38,44,71,0.93)",
    'GLASS': "rgba(40,49,80,0.62)",
    'TEXT': "#F5F8FD",
    'TEXT_SUB': "#AEB9C9",
    'BORDER': "#272F4C",
    'SIDEBAR_BG': "linear-gradient(140deg,#181C24 70%,#1B233F 100%)",
    'SIDEBAR_TEXT': "#C1CCDE",
    'CODE_BG': "#20263A",
    'DIVIDER': "#25294A",
    'SUCCESS': "#34d399",
    'WARNING': "#facc15",
    'ERROR': "#f87171",
}

VECTORSTORE_OPTIONS = [
    ("Geral", "Busca em todas as bases de conhecimento"),
    ("Iniciativas", "Projetos e ações estratégicas"),
    ("Indicadores", "Indicadores de desempenho"),
    ("OMS", "Conteúdo da Organização Mundial da Saúde"),
    ("Padrões", "Normas e padrões técnicos"),
    ("PTA", "Planejamento Tático Anual"),
    ("Riscos", "Gestão de Riscos Estratégicos"),
]
VECTORSTORE_MAP = {k: v.split(' ')[0].lower() if k != "Geral" else "Geral" for k, v in VECTORSTORE_OPTIONS}

st.set_page_config(
    page_title="MTI Assistente Estratégico",
    page_icon=LOGO_PATH if os.path.exists(LOGO_PATH) else "🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    from langchain_core.chat_history import InMemoryChatMessageHistory
    from pipeline.stream import get_response_stream, get_response_stream_single_vectorstore
    from memory.memory_handler import add_message_to_history, get_session_history
except ImportError:
    def get_response_stream(question, session_id):
        yield f"**Análise de Riscos para:** {question}\n\n- Risco: Falha na implementação de IA\n- Categoria: Estratégico\n"
    def get_response_stream_single_vectorstore(question, session_id, vectorstore_key):
        yield f"**Análise focada em {vectorstore_key.title()} para:** {question}\n"
    class InMemoryChatMessageHistory:
        def __init__(self): self.messages = []
        def add_message(self, msg): self.messages.append(msg)
    def add_message_to_history(session_id, message_obj): pass
    def get_session_history(session_id): return InMemoryChatMessageHistory()

def get_image_base64(path):
    if not os.path.exists(path): return ""
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except Exception: return ""

def load_users():
    if not os.path.exists(USERS_FILE):
        sample_users = { "admin": {"password_hash": pwd_context.hash("admin123"), "nome_completo": "Admin MTI"} }
        with open(USERS_FILE, "w", encoding="utf-8") as f: json.dump(sample_users, f, indent=4)
        return sample_users
    with open(USERS_FILE, "r", encoding="utf-8") as f: return json.load(f)
USERS_DATA = load_users()
def check_login(username, password):
    user_data = USERS_DATA.get(username)
    if user_data and "password_hash" in user_data:
        try: return pwd_context.verify(password, user_data["password_hash"])
        except Exception: return False
    return False

def load_global_styles(t):
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Orbitron:wght@700&display=swap');
body, .stApp {{
    background: {t['BACKGROUND']} !important;
    font-family: 'Inter', 'IBM Plex Sans', sans-serif;
    color: {t['TEXT']};
}}
[data-testid="stSidebar"] {{
    background: {t['SIDEBAR_BG']} !important;
    color: {t['SIDEBAR_TEXT']} !important;
    border-right: 1px solid {t['BORDER']};
    padding-top:2.2em!important;
}}
.sidebar-header {{
    text-align: center; color: {t['ACCENT']};
    letter-spacing: 1.5px; font-family: 'Orbitron', 'Inter', sans-serif;
    font-weight: 900; font-size: 1.48em; margin-bottom: 1.2em;
    text-shadow: 0 2px 10px #46FFB933;
}}
.sidebar-username {{
    text-align:center; color:{t['SIDEBAR_TEXT']}; font-size: 1.04em;
    font-weight: 600; margin-bottom: 0.7em; letter-spacing:1px;
}}
.usercard-status {{
    display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:7px;
    background:#46FFB9;box-shadow:0 0 7px #46FFB93a;
}}
.stButton>button, .stForm button {{
    background: linear-gradient(100deg, {t['ACCENT']} 80%, {t['ACCENT2']} 100%);
    color: #151B26 !important;
    border-radius: 9px !important;
    font-weight: 700; letter-spacing: .03em; padding: 0.52em 1.25em;
    box-shadow: 0 2px 12px #6ca2ff22;
    border: none!important;
    margin-bottom: .5em!important;
    transition: background 0.12s, color 0.12s, transform 0.14s;
}}
.stButton>button:hover, .stForm button:hover {{
    background: linear-gradient(100deg, {t['ACCENT2']} 80%, {t['ACCENT']} 100%);
    color: #fff!important; transform:scale(1.03);
}}
.stTextInput>div>input, .stSelectbox>div>div {{
    background: {t['GLASS']}!important;
    color: {t['TEXT']}!important;
    border: 1.2px solid {t['BORDER']}!important;
    border-radius: 8px;
    padding: 0.6em 1em;
}}
.stTextInput>div>input:focus, .stSelectbox>div>div:focus-within {{
    border: 1.5px solid {t['ACCENT']};
    box-shadow: 0 0 6px #6CA2FF55;
    outline: none!important;
}}
::-webkit-scrollbar {{ width: 8px; background: #232942; }}
::-webkit-scrollbar-thumb {{ border-radius: 14px; background: #36405844; }}
::-webkit-scrollbar-thumb:hover {{ background: #6CA2FF44; }}

.login-background {{
    position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
    background: linear-gradient(120deg, #151B26 0%, #22314C 100%);
    overflow:hidden;
    z-index: -1;
}}
#svg-circuit-bg {{
    position: absolute; left: 0; top: 0; width: 100vw; height: 100vh;
    opacity: 0.15; pointer-events: none;
    z-index:-1;
}}
.login-logo {{
    display: block; margin: 0 auto 2em auto; border-radius: 16px;
    background: #233458;
    padding: 12px; width: 86px; box-shadow: 0 2px 24px #46FFB922;
}}
.login-title {{
    text-align: center; color: #6CA2FF;
    font-family:'Orbitron', 'Inter',sans-serif; font-weight:900;
    letter-spacing:2px; font-size: 2.25em; margin-bottom: 0.4em;
    text-shadow: 0 0 16px #46FFB955;
}}
.login-sub {{
    text-align:center; color:{t['TEXT_SUB']}; font-size:1.13em; margin-top:-0.9em; margin-bottom:2.3em;
    font-weight:600;letter-spacing:.5px;
}}
.login-footer {{
    text-align:center; margin-top:2em; color:#6CA2FF; font-size:1.03em;
    opacity:0.7; letter-spacing:1px;
}}
.chat-header {{
    display:flex;align-items:center;justify-content:center;margin-bottom:2em;
}}
.ai-pulse {{
    width:16px;height:16px;border-radius:50%;background:#46FFB9;
    box-shadow:0 0 0 0 #46FFB966;animation:aiPulse 1.2s infinite;
    margin-right:10px;
}}
@keyframes aiPulse {{
    0% {{ box-shadow:0 0 0 0 #46FFB966; }}
    70%{{ box-shadow:0 0 0 9px #46FFB900; }}
    100%{{ box-shadow:0 0 0 0 #46FFB966; }}
}}
.chat-title {{
    font-family:'Orbitron', 'Inter',sans-serif; font-size:1.6em;
    letter-spacing:2px; font-weight:900; color:#6CA2FF;
    text-shadow: 0 2px 10px #46FFB933;
    margin-right:13px;
}}
.message-container {{
    margin-bottom: 1.18rem; display: flex; align-items: flex-start;
    animation: fadeIn 0.8s cubic-bezier(.39,.575,.565,1) both;
}}
@keyframes fadeIn {{
    0% {{ opacity:0; transform: translateY(18px); }}
    100% {{ opacity:1; transform: none; }}
}}
.user-message.message-container {{ margin-left: auto; max-width: 80%; justify-content: flex-end; }}
.bot-message.message-container {{ margin-right: auto; max-width: 87%; }}
.message {{
    padding: 17px 22px; border-radius: 20px; line-height: 1.6; font-size: 1.12rem; width: 100%;
    background: {t['CODE_BG']}; color: {t['TEXT']};
    box-shadow: 0 2px 20px #23294216; transition: box-shadow 0.2s;
    border: 1px solid transparent;
}}
.user-message .message {{
    background: linear-gradient(90deg, {t['ACCENT']} 70%, {t['ACCENT2']} 100%);
    color: #fff; font-weight: 600; border: 1px solid #32405e;
}}
.bot-message .message {{
    background: {t['SURFACE']}; border: 1.5px solid {t['BORDER']};
    position:relative;
}}
.avatar-mti {{
    width: 44px; height: 44px;
    border-radius: 50%; object-fit: cover;
    background: #233458; box-shadow: 0 0 0 2px {t['ACCENT']};
    border: 2px solid {t['BORDER']}; margin-top: 6px;
}}
.avatar-user {{
    width: 44px; height: 44px; border-radius: 50%;
    background: {t['ACCENT2']}; display: flex; align-items: center; justify-content: center;
    color: #fff; font-weight: 700; font-size: 1.14em;
    box-shadow: 0 0 0 2px {t['ACCENT2']};
    border: 2px solid {t['BORDER']}; margin-top: 6px;
}}
.suggestion-btn {{
    background: none; border: 1.5px solid {t['ACCENT']};
    color: {t['ACCENT']}; border-radius: 10px; font-weight: 600;
    margin: 0.3em 0.5em 0.3em 0; padding: 0.63em 1.17em;
    transition: border 0.15s, color 0.12s, background 0.13s;
    cursor: pointer; font-size:1.10em; box-shadow:0 2px 10px #46FFB911;
}}
.suggestion-btn:hover {{
    background: {t['ACCENT']}; color: #fff; border: 1.5px solid {t['ACCENT2']};
}}
hr {{
    border: none; height: 2.5px;
    background: linear-gradient(90deg,#233458,#6CA2FF44,#233458,#7B61FF);
    margin: 1.2em 0; opacity: .7;
}}
.bot-message .message h1,.bot-message .message h2,.bot-message .message h3,.bot-message .message h4 {{
    color: {t['ACCENT']}; font-weight: 800;
}}
.bot-message .message code,.bot-message .message pre {{
    background: #232942; color: {t['ACCENT']}; border-radius: 8px; padding: 0.13em 0.42em;
}}
.bot-message .message table {{
    width: 100%; border-collapse: collapse; background: rgba(33,39,50,0.83);
}}
.bot-message .message th, .bot-message .message td {{
    border: 1.2px solid #233458; padding: 0.58em; color: #F5F8FD;
}}
.bot-message .message th {{
    background: #151B26; color: {t['ACCENT']};
}}
.insight-block, .recommendation-block {{
    padding: 1.17rem; margin: 1.13rem 0; border-radius: 13px; border-left: 6px solid;
    background: linear-gradient(95deg, #181b22 0%, #22314C11 100%);
    box-shadow: 0 0 10px #23345818;
    font-size:1.11em;
}}
.insight-block::before {{
    content:"💡"; font-size:1.4em; margin-right:8px;vertical-align:-4px;
}}
.recommendation-block::before {{
    content:"🤖"; font-size:1.4em; margin-right:8px;vertical-align:-4px;
}}
.insight-block {{ border-color: {t['WARNING']}; }}
.recommendation-block {{ border-color: {t['SUCCESS']}; }}
.divider {{
    border: none; height: 3px; background: {t['DIVIDER']};
    margin: 2.2em 0 1.2em 0; border-radius: 7px;
}}
.ai-loader {{
    display: flex; align-items: center; justify-content: center;
    padding: 1.35em 0 0.7em 0;
}}
.ai-loader-dot {{
    width: 9px; height: 9px; margin: 0 4px; border-radius: 50%;
    background: {t['ACCENT2']}; opacity: 0.92;
    animation: aiLoader 1.06s infinite cubic-bezier(.4,0,.2,1);
}}
.ai-loader-dot:nth-child(2){{animation-delay:0.16s;}}
.ai-loader-dot:nth-child(3){{animation-delay:0.32s;}}
@keyframes aiLoader {{
    0%, 80%, 100% {{transform: scale(0.76);opacity:.5;}}
    40% {{transform: scale(1.2);opacity:1;}}
}}
::-webkit-input-placeholder {{ color:#8ca4de; }}
</style>
"""

def get_user_history_path(username):
    safe_username = "".join(c if c.isalnum() else "_" for c in username)
    return os.path.join(HISTORY_DIR, f"{safe_username}_chat_history.json")

def load_user_history(username):
    path = get_user_history_path(username)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("messages", [])
    return []

def save_user_history(username, messages):
    os.makedirs(HISTORY_DIR, exist_ok=True)
    path = get_user_history_path(username)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"messages": messages}, f, indent=2)

def process_response_text(text: str) -> str:
    if not isinstance(text, str) or not text.strip():
        return "<p>O assistente não forneceu uma resposta.</p>"
    return markdown2.markdown(text, extras=["fenced-code-blocks", "tables", "strike", "task_list", "header-ids"])

def readable_time(iso):
    dt = datetime.datetime.fromisoformat(iso)
    now = datetime.datetime.now()
    diff = now - dt
    if diff.days > 0: return dt.strftime("%d/%m/%Y %H:%M")
    if diff.seconds < 60: return "Agora"
    if diff.seconds < 3600: return f"{diff.seconds//60} min atrás"
    return dt.strftime("%H:%M")

def login_screen():
    st.markdown('<div class="login-background"></div>', unsafe_allow_html=True)
    st.markdown('''<svg id="svg-circuit-bg" width="100%" height="100%" viewBox="0 0 1200 800" fill="none" xmlns="http://www.w3.org/2000/svg">
      <g stroke="#46FFB9" stroke-width="1.2" opacity="0.25">
      <rect x="50" y="50" width="250" height="250" rx="35" />
      <rect x="900" y="120" width="210" height="300" rx="36"/>
      <rect x="350" y="590" width="500" height="120" rx="30"/>
      <circle cx="200" cy="700" r="50"/>
      <circle cx="1050" cy="600" r="40"/>
      <path d="M100 175 Q200 300 500 200" />
      <path d="M1150 620 Q1020 300 750 300" />
      <path d="M480 700 Q600 600 900 700" />
      </g>
    </svg>''', unsafe_allow_html=True)
    with st.container():
        _, col, _ = st.columns([1,1.5,1])
        with col:
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            if os.path.exists(LOGO_PATH):
                logo_b64 = get_image_base64(LOGO_PATH)
                st.markdown(f'<img src="data:image/png;base64,{logo_b64}" class="login-logo"/>', unsafe_allow_html=True)
            st.markdown('<div class="login-title">Assistente Estratégico MTI</div>', unsafe_allow_html=True)
            st.markdown('<div class="login-sub">Performance, inteligência e insights para sua estratégia.<br><span style="color:#6CA2FF;font-weight:700;">Acesso restrito</span></div>', unsafe_allow_html=True)
            if 'login_error' in st.session_state and st.session_state.login_error:
                st.error(st.session_state.login_error)
                st.session_state.login_error = None
            with st.form(key="login_form"):
                username = st.text_input("Usuário", key="login_user", label_visibility="collapsed", placeholder="Usuário")
                password = st.text_input("Senha", type="password", key="login_pass", label_visibility="collapsed", placeholder="Senha")
                if st.form_submit_button("Acessar Plataforma", use_container_width=True):
                    if check_login(username, password):
                        st.session_state.update({
                            "authenticated": True, "username": username,
                            "user_full_name": USERS_DATA.get(username, {}).get("nome_completo", username),
                            "messages": load_user_history(username),
                        })
                        st.rerun()
                    else:
                        st.session_state.login_error = "Credenciais inválidas."
                        st.rerun()
            st.markdown('<div class="login-footer">© MTI Inteligência 2025 • Powered by AI</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-header">MTI ESTRATÉGICO</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sidebar-username"><span class="usercard-status"></span>{st.session_state.user_full_name}</div>', unsafe_allow_html=True)
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.selectbox("Foco da Pesquisa", [opt[0] for opt in VECTORSTORE_OPTIONS], key="selected_vectorstore_label", label_visibility="collapsed")
        st.button("🧹 Nova Conversa", use_container_width=True, on_click=lambda: st.session_state.update(messages=[]))
        if st.button("🚪 Sair", use_container_width=True, type="secondary"):
            save_user_history(st.session_state.username, st.session_state.messages)
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        st.markdown("""<hr class='divider'>
        <div style="text-align:center;color:#6CA2FF;font-size:1.05em;opacity:0.67;">
            <span style="font-size:1.15em;">⚡</span> Powered by AI<br>
            <span style="font-size:0.97em;">Use <b>/ajuda</b> para comandos rápidos.</span>
        </div>
        """, unsafe_allow_html=True)

def display_chat_interface():
    st.markdown('<div class="chat-area-wrapper" id="chat-area">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="chat-header">
        <span class="ai-pulse"></span>
        <span class="chat-title">Assistente Estratégico</span>
        <svg width="27" height="27" fill="none" xmlns="http://www.w3.org/2000/svg">
            <g filter="url(#a)">
                <path d="M13.5 5L25 21H2L13.5 5Z" fill="#6CA2FF"/>
            </g>
            <defs>
                <filter id="a" x="0" y="0" width="27" height="27" filterUnits="userSpaceOnUse">
                    <feDropShadow dx="0" dy="0" stdDeviation="2" flood-color="#46FFB9" flood-opacity="0.67"/>
                </filter>
            </defs>
        </svg>
    </div>
    """, unsafe_allow_html=True)
    def handle_suggestion_click(prompt_text):
        st.session_state.processing_prompt = prompt_text

    if not st.session_state.get("messages"):
        st.markdown('<div style="text-align:center; padding: 2.2rem;"><h2 style="color: #6CA2FF; font-weight:800;">Como posso te auxiliar hoje?</h2></div>', unsafe_allow_html=True)
        suggestions = [
            ("🔍 Principais iniciativas", "principais iniciativas"),
            ("📊 Indicadores GADP", "indicadores GADP"),
            ("⚠️ Riscos operacionais", "riscos operacionais"),
            ("📅 Resumo semanal estratégico", "resumo semanal"),
        ]
        st.markdown('<div style="display:flex; flex-wrap:wrap; gap:0.5em; justify-content:center;">', unsafe_allow_html=True)
        for label, sug in suggestions:
            if st.button(label, use_container_width=True, key=f"sug_{sug}"):
                handle_suggestion_click(sug)
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    for i, msg in enumerate(st.session_state.get("messages", [])):
        is_user = msg["role"] == "user"
        with st.container():
            col1, col2 = st.columns([1, 11] if not is_user else [11, 1])
            avatar_col, content_col = (col1, col2) if not is_user else (col2, col1)
            with avatar_col:
                if not is_user:
                    logo_b64 = get_image_base64(LOGO_PATH)
                    st.markdown(
                        f'<img src="data:image/png;base64,{logo_b64}" class="avatar-mti" />' if logo_b64 else
                        '<div class="avatar-mti" style="background:#232942;"></div>',
                        unsafe_allow_html=True)
                else:
                    initials = "".join(part[0] for part in st.session_state.user_full_name.split()[:2]).upper()
                    st.markdown(f'<div class="avatar-user">{initials}</div>', unsafe_allow_html=True)
            with content_col:
                content_html = process_response_text(msg["content"]) if not is_user else msg["content"]
                st.markdown(
                    f"<div class='message-container {'user-message' if is_user else 'bot-message'}'>"
                    f"<div class='message'>{content_html}<span style='float:right;font-size:0.93em;color:#6CA2FF7a;'>{readable_time(msg['timestamp'])}</span></div></div>",
                    unsafe_allow_html=True
                )
                if not is_user and i == len(st.session_state['messages'])-1:
                    c1, c2 = st.columns([0.1,0.1])
                    with c1:
                        if st.button("👍", key=f"like_{i}"):
                            st.success("Obrigado pelo feedback!", icon="✅")
                    with c2:
                        if st.button("👎", key=f"dislike_{i}"):
                            st.warning("Sua avaliação negativa será considerada.", icon="⚠️")
    st.markdown("</div>", unsafe_allow_html=True)
    if st.session_state.get("typing", False):
        st.markdown("""
        <div class="ai-loader">
            <div class="ai-loader-dot"></div>
            <div class="ai-loader-dot"></div>
            <div class="ai-loader-dot"></div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("""<script>
        const chatArea = document.getElementById("chat-area");
        if (chatArea) { chatArea.scrollTop = chatArea.scrollHeight; }
    </script>""", unsafe_allow_html=True)

def process_prompt(prompt):
    st.session_state.typing = True
    if prompt.startswith("/ajuda"):
        st.session_state.messages.append({
            "role": "assistant",
            "content":
            "**Comandos Rápidos:**<br>"
            "- <b>/limpar</b>: Limpa todo o histórico do chat<br>"
            "- <b>/ajuda</b>: Exibe estes comandos<br>"
            "- <b>/foco</b>: Alterna modo de foco (tela cheia)",
            "timestamp": datetime.datetime.now().isoformat()
        })
        st.session_state.typing = False
        return False
    if prompt.startswith("/limpar"):
        st.session_state.messages = []
        st.success("Histórico limpo!", icon="🧹")
        st.session_state.typing = False
        return False
    if prompt.startswith("/foco"):
        st.session_state.foco = not st.session_state.get("foco", False)
        st.info("Modo foco ativado!" if st.session_state.foco else "Modo foco desativado!", icon="💡")
        st.session_state.typing = False
        return False
    user_msg = {"role": "user", "content": prompt, "timestamp": datetime.datetime.now().isoformat()}
    st.session_state.messages.append(user_msg)
    add_message_to_history(st.session_state.get("session_id", ""), user_msg)
    return True

def run_ai_response():
    if not st.session_state.messages:
        return
    last_user_input = st.session_state.messages[-1]["content"]
    selected_vs_key = VECTORSTORE_MAP.get(st.session_state.get("selected_vectorstore_label"), "Geral")
    with st.spinner("O Analista Estratégico está processando sua pergunta..."):
        try:
            stream = (get_response_stream(last_user_input, st.session_state.get("session_id", ""))
                      if selected_vs_key == "Geral" else
                      get_response_stream_single_vectorstore(last_user_input, st.session_state.get("session_id", ""), selected_vs_key))
            response_stream = "".join(chunk for chunk in stream if chunk)
        except Exception as e:
            response_stream = f"Desculpe, ocorreu um erro: {e}"
    assistant_msg = {"role": "assistant", "content": response_stream, "timestamp": datetime.datetime.now().isoformat()}
    st.session_state.messages.append(assistant_msg)
    save_user_history(st.session_state.username, st.session_state.messages)
    st.session_state.typing = False

def main():
    st.markdown(load_global_styles(THEME), unsafe_allow_html=True)
    if "authenticated" not in st.session_state: st.session_state.authenticated = False
    if not st.session_state.authenticated:
        login_screen()
        return
    for key in ["messages", "session_id"]:
        if key not in st.session_state:
            st.session_state[key] = [] if key == "messages" else str(uuid.uuid4())
    if "foco" in st.session_state and st.session_state.foco:
        st.markdown("""
        <style>
        [data-testid="stSidebar"], header, #MainMenu, footer {display:none!important;}
        .chat-area-wrapper {max-width: 1100px;margin:auto;}
        </style>""", unsafe_allow_html=True)
    render_sidebar()
    display_chat_interface()
    if "processing_prompt" in st.session_state and st.session_state.processing_prompt:
        prompt_to_process = st.session_state.processing_prompt
        st.session_state.processing_prompt = None
        should_run_ai = process_prompt(prompt_to_process)
        if should_run_ai:
            run_ai_response()
        st.rerun()
    if prompt := st.chat_input("Faça sua pergunta ao Assistente MTI... (ou digite /ajuda)"):
        should_run_ai = process_prompt(prompt)
        if should_run_ai:
            run_ai_response()
        st.rerun()

if __name__ == "__main__":
    main()