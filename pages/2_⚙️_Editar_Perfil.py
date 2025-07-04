import streamlit as st
import os
import json
import base64
from io import BytesIO
from PIL import Image

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Editar Perfil", layout="wide")

# --- CSS ELEGANTE ---
st.markdown("""
<style>
body, .stApp { background: #0a1a2f !important; }
h1, h2, h3, h4 { font-family: Montserrat, sans-serif; color: #00A9E0; }
.stTextInput>label, .stFileUploader>label, .stSelectbox>label { color: #b0cfff !important; font-weight: 600;}
.stButton>button, div[data-testid="stFormSubmitButton"]>button, .stDownloadButton>button {
    background: linear-gradient(90deg,#00A9E0,#71C5E8)!important;
    color: #fff; border-radius:.9rem; font-weight:700; margin-top:1.2rem;
    box-shadow: 0 3px 16px #0086c850;
    letter-spacing: .5px;
    border: none;
    transition: 0.2s;
    width: 100%; /* Garante que botões como o de download usem a largura total se use_container_width=True */
}
.stButton>button:active, div[data-testid="stFormSubmitButton"]>button:active, .stDownloadButton>button:active { transform: scale(.97);}
.perfil-card {
    background: linear-gradient(135deg, #0a223f 60%, #193f68 100%);
    border-radius: 2.2rem; box-shadow: 0 12px 62px #0005;
    padding: 2.8rem 2.6rem 2.5rem 2.6rem; margin-bottom: 2.5rem;
    border: 2px solid #00a9e0; max-width: 580px;
    margin-left:auto; margin-right:auto; min-width:340px;
}
.avatar-box {
    display: flex; flex-direction: column; align-items: center; gap: 1rem;
    margin-bottom: 1.6rem;
}
.avatar-glow {
    width: 158px; height: 158px; border-radius: 50%; overflow: hidden;
    border: 8px solid #00A9E0; background: #0A192F; margin-bottom: .9rem;
    box-shadow: 0 0 0 16px #00a9e038, 0 0 64px #00a9e0bb;
    display: flex; align-items: center; justify-content: center;
    position: relative;
    transition: box-shadow 0.2s;
}
.avatar-glow:hover { box-shadow: 0 0 0 18px #00a9e070, 0 0 70px #00a9e0cc; }
.avatar-glow img { width: 100%; height: 100%; object-fit: cover; }
.avatar-initials { font-size: 4.2rem; color: #fff; font-weight: 900; letter-spacing: 2px;}
.avatar-actions {
    display: flex; flex-direction: column; align-items: center; gap: 0.8rem;
    margin-top: .35rem; width: 100%; max-width: 280px;
}
.unid-badge {
    background:linear-gradient(90deg,#1a4e5a 70%,#00529B 100%);
    padding:.55rem 1.5rem; border-radius: 1.3rem; color:#fff; font-weight:700;
    font-size:1.14rem; margin-bottom:.7rem; display:inline-block;
    letter-spacing: .6px; border:1.6px solid #00A9E0;
    box-shadow: 0 2px 12px #0086c820;
}
.perfil-fields .stTextInput, .perfil-fields .stTextArea, .perfil-fields .stSelectbox { margin-bottom: 1.25rem; }
.perfil-fields label { font-size: 1.14rem; }
.stAlert { border-radius: 1.1rem; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0b263d 60%, #0a1a2f 100%)!important;
    color: #B0C0D0!important;
    border-right: 2px solid #00A9E0;
    box-shadow: 7px 0 32px #00a9e04d;
}
.sidebar-profile {
    text-align: center;
    padding: 2.3rem 1rem 2.2rem 1rem;
    background: linear-gradient(120deg, #00529B 60%, #10284e 100%);
    border-bottom: 2.5px solid #00A9E0;
    margin-bottom: 2.7rem;
    border-radius: 0 0 1.5rem 1.5rem;
}
.sidebar-avatar {
    width: 80px; height: 80px; border-radius: 50%; overflow: hidden;
    border: 3px solid #00A9E0; background: #0A192F;
    box-shadow: 0 0 0 8px #00a9e048;
    margin: 0 auto 1.1rem auto;
    display: flex; align-items: center; justify-content: center;
}
.sidebar-avatar img { width: 100%; height: 100%; object-fit: cover;}
.sidebar-avatar-initials { font-size: 2.3rem; color: #fff; font-weight: 800;}
.sidebar-username { font-size: 1.23rem; font-weight: 700; color: #fff; margin-bottom: .2rem;}
.sidebar-email { font-size: 0.98rem; color: #B0C0D0; margin-bottom:.5rem;}
.sidebar-unidade { font-size: 0.86rem; color: #71C5E8; }
.sidebar-footer {
    font-size: 0.92rem; color: #B0C0D0; text-align: center; margin-top:3rem; padding: .8rem 0;
    border-top: 1px solid #00A9E0;
}
/* Seletores para links da sidebar (podem precisar de ajuste com versões do Streamlit) */
.st-emotion-cache-1px2117.e1gf0u8t0 a, .css-1oe5k79.e1fqkh3o9 a {
    color: #B0C0D0;
    font-size: 1.07rem;
    font-weight: 500;
    padding: 0.7rem 1.2rem;
    margin-bottom: 0.6rem;
    border-radius: 0.9rem;
    transition: background-color 0.18s, color 0.15s, transform 0.17s;
    display: flex; align-items: center; gap: 0.8rem;
}
.st-emotion-cache-1px2117.e1gf0u8t0 a:hover, .css-1oe5k79.e1fqkh3o9 a:hover {
    background-color: #00A9E0;
    color: #fff;
    transform: translateX(7px) scale(1.03);
}
.st-emotion-cache-1px2117.e1gf0u8t0 a[data-active="true"], .css-1oe5k79.e1fqkh3o9 a[aria-current="page"] {
    background: #00529B !important;
    color: #fff !important;
    font-weight: 700;
    border-left: 4px solid #71C5E8;
}
@media (max-width: 900px) {
    .perfil-card { padding: 1.2rem .4rem; max-width: 99vw;}
    .avatar-glow { width:110px; height:110px;}
}
.edit-tip {
    background: #003b5b;
    color: #fff;
    border-radius: .8rem;
    padding: .8rem 1.1rem;
    font-size: 1.10rem;
    margin-bottom: 1.3rem;
    display: flex;
    align-items: center;
    gap: .7rem;
    box-shadow: 0 4px 18px #00a9e044;
    border-left: 6px solid #00A9E0;
}
.edit-tip .emoji-pencil {
    font-size: 1.2rem;
    margin-right: .2rem;
}
.avatar-actions .stFileUploader {
    width: 100%;
}
.avatar-actions .stButton>button { /* Estilo específico para o botão Remover Foto */
    background: #182d4e !important;
    color: #71C5E8 !important;
    margin-top: 0.5rem !important; /* Ajuste de margem se necessário */
}
.avatar-actions .stButton>button:hover {
    background: #00A9E0 !important;
    color: #fff !important;
}
.data-management-section {
    max-width: 580px; /* Mesmo max-width do perfil-card para consistência */
    margin: 2rem auto; /* Centraliza e adiciona margem superior/inferior */
    padding: 0 1rem; /* Padding lateral */
    /* background: linear-gradient(135deg, #0a223f 60%, #193f68 100%); /* Opcional: mesmo fundo do card */
    /* border-radius: 2.2rem; */ /* Opcional */
    /* box-shadow: 0 12px 62px #0005; */ /* Opcional */
    /* border: 2px solid #00a9e0; */ /* Opcional */
    /* padding: 1.5rem; */ /* Opcional: se usar fundo/borda */
}
.data-management-section h3 { /* Título da seção */
    text-align:center; 
    margin-bottom:1.2rem;
    color: #00A9E0;
}
.data-management-section p { /* Texto de ajuda/descrição */
    text-align: center;
    font-size: 0.95rem;
    color: #b0cfff;
    margin-top: 0.5rem;
}
.data-management-section .stDownloadButton>button {
    margin-top: 0.5rem !important; /* Ajusta a margem superior do botão de download */
}
</style>
<link href="https://fonts.googleapis.com/css?family=Montserrat:700,900,400&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# --- DADOS / UTILITÁRIOS ---
# Assume que este script está em uma pasta 'pages' e 'user.json' está na raiz do projeto
CURRENT_SCRIPT_PATH = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_SCRIPT_PATH, ".."))
USERS_PATH = os.path.join(PROJECT_ROOT, "user.json")

def load_users():
    """Carrega os dados dos usuários do arquivo JSON."""
    if not os.path.exists(USERS_PATH):
        with open(USERS_PATH, "w", encoding="utf-8") as f:
            json.dump({}, f) # Cria um JSON vazio se o arquivo não existir
        return {}
    try:
        with open(USERS_PATH, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        st.error("Erro ao carregar dados dos usuários. O arquivo user.json pode estar corrompido.")
        return {} # Retorna um dict vazio em caso de erro de decodificação

def save_user(username_to_save, data_to_save):
    """Salva os dados de um usuário específico no arquivo JSON."""
    users_data = load_users()
    if username_to_save not in users_data:
        users_data[username_to_save] = {} # Cria a entrada do usuário se não existir
    users_data[username_to_save].update(data_to_save)
    try:
        with open(USERS_PATH, "w", encoding="utf-8") as f:
            json.dump(users_data, f, ensure_ascii=False, indent=4)
    except IOError as e:
        st.error(f"Erro ao salvar dados do usuário: {e}")


def process_image(uploaded_file):
    """Processa uma imagem carregada para base64."""
    if not uploaded_file:
        return None
    try:
        img = Image.open(uploaded_file).convert("RGB")
        img.thumbnail((320, 320)) # Redimensiona mantendo a proporção
        buf = BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
    except Exception as e:
        st.error(f"Erro ao processar imagem: {e}")
        return None

def initials(name_str):
    """Gera iniciais a partir de um nome completo."""
    parts = (name_str or "").strip().split()
    if not parts:
        return "U" # Usuário Desconhecido
    return (parts[0][0] + (parts[1][0] if len(parts) > 1 else '')).upper()

def ensure_user_in_json(username_to_check):
    """Garante que um usuário exista no JSON, adicionando-o com valores padrão se necessário."""
    users_data = load_users()
    if username_to_check not in users_data:
        users_data[username_to_check] = {
            "nome_completo": "Novo Usuário", # Valor padrão
            "unidade": "Não definida",      # Valor padrão
            "profile_image": None,
            "assistant_tone": "Neutro",     # Valor padrão para nova preferência
            "assistant_detail_level": "Equilibrado" # Valor padrão para nova preferência
        }
        # Salva apenas se um novo usuário foi de fato adicionado
        try:
            with open(USERS_PATH, "w", encoding="utf-8") as f:
                json.dump(users_data, f, ensure_ascii=False, indent=4)
        except IOError as e:
            st.error(f"Erro ao inicializar usuário no JSON: {e}")


# --- AUTENTICAÇÃO ---
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("🔒 Faça login para acessar esta página.")
    if st.button("Ir para o login", key="login_redirect_btn"):
        st.switch_page("ChatBot.py") # Ajuste se o nome do seu script principal for diferente
    st.stop()

username = st.session_state.get("username")
if not username: # Segurança adicional
    st.error("⚠️ Nome de usuário não encontrado na sessão. Por favor, faça login novamente.")
    if st.button("Retornar ao Login", key="username_missing_login_btn"):
        st.switch_page("ChatBot.py") # Ajuste conforme necessário
    st.stop()

ensure_user_in_json(username) # Garante que o usuário exista no JSON
users = load_users()
user = users.get(username, {}) # Carrega dados do usuário atual

# Garantir que usuários existentes tenham os novos campos com valores padrão se ausentes
user.setdefault("assistant_tone", "Neutro")
user.setdefault("assistant_detail_level", "Equilibrado")

# Inicializa st.session_state para a imagem de perfil se não existir
if "pfp_b64" not in st.session_state:
    st.session_state.pfp_b64 = user.get("profile_image")
# O nome do input (st.session_state.nome_input_key) será gerenciado pelo próprio st.text_input
# e inicializado em perfil_form. As preferências (selectbox) também.

# --- SIDEBAR COMPLETA ---
with st.sidebar:
    st.markdown('<div class="sidebar-profile">', unsafe_allow_html=True)
    
    # O nome na sidebar tenta pegar o valor mais recente do campo de edição,
    # senão o nome salvo.
    if "nome_input_key" in st.session_state and st.session_state.nome_input_key.strip():
        sidebar_nome = st.session_state.nome_input_key
    else:
        sidebar_nome = user.get("nome_completo", "Usuário")

    sidebar_img = st.session_state.get("pfp_b64", user.get("profile_image"))

    if sidebar_img:
        st.markdown(f'<div class="sidebar-avatar"><img src="data:image/png;base64,{sidebar_img}"></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="sidebar-avatar"><span class="sidebar-avatar-initials">{initials(sidebar_nome)}</span></div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="sidebar-username">{sidebar_nome}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-email">{username}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-unidade">Unidade: {user.get("unidade","Não definida")}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Links de Navegação (ajuste os caminhos se necessário)
    # Assume que ChatBot.py está na raiz do projeto.
    st.page_link("ChatBot.py", label="Chat Assistente", icon="💬")
    # Assume que este script é 'pages/2_⚙️_Editar_Perfil.py' (o nome do arquivo atual)
    st.page_link("pages/2_⚙️_Editar_Perfil.py", label="Editar Perfil", icon="🛠️")


    st.markdown('<div class="sidebar-footer">MTI Assistente v1.0<br>© 2024 Sua Empresa</div>', unsafe_allow_html=True)


# --- COMPONENTE AVATAR ---
def avatar_section():
    st.markdown('<div class="avatar-box">', unsafe_allow_html=True)

    # As iniciais usam o valor do campo de nome (st.session_state.nome_input_key) se disponível,
    # caso contrário, o nome salvo do usuário.
    if "nome_input_key" in st.session_state and st.session_state.nome_input_key.strip():
        nome_para_iniciais = st.session_state.nome_input_key
    else:
        nome_para_iniciais = user.get("nome_completo", "Usuário")
    
    if st.session_state.pfp_b64:
        st.markdown(f'<div class="avatar-glow"><img src="data:image/png;base64,{st.session_state.pfp_b64}"></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="avatar-glow"><span class="avatar-initials">{initials(nome_para_iniciais)}</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="avatar-actions">', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Alterar foto de perfil:",
        type=["png", "jpg", "jpeg"],
        key=f"uploader_{username}_{st.session_state.get('upload_key_suffix', 0)}", # Chave dinâmica
        label_visibility="collapsed",
        help="Faça upload de uma nova foto para seu perfil. Tamanho máximo recomendado: 2MB."
    )

    if uploaded_file:
        new_b64img = process_image(uploaded_file)
        if new_b64img is not None and new_b64img != st.session_state.pfp_b64:
            st.session_state.pfp_b64 = new_b64img
            st.rerun() # Re-renderizar para mostrar a nova imagem e atualizar a sidebar

    if st.session_state.pfp_b64:
        if st.button("🗑️ Remover Foto", key="remover_foto_btn_v2", help="Remover foto atual", use_container_width=True):
            st.session_state.pfp_b64 = None
            st.session_state.upload_key_suffix = st.session_state.get('upload_key_suffix', 0) + 1
            st.rerun()

    st.markdown('</div></div>', unsafe_allow_html=True) # Fechar avatar-actions e avatar-box

# --- COMPONENTE FORMULÁRIO PERFIL ---
def perfil_form():
    st.markdown(
        """
        <div class="edit-tip">
            <span class="emoji-pencil">✏️</span>
            <b>Edite suas informações pessoais e preferências abaixo e clique em "Salvar alterações".</b>
        </div>
        """, unsafe_allow_html=True
    )
    st.markdown('<div class="perfil-fields">', unsafe_allow_html=True)

    with st.form("editar_perfil_form_final"): # Chave do formulário atualizada
        
        # Campo Nome Completo
        # O valor inicial é o que está em session_state (se já digitado) ou o valor salvo.
        valor_inicial_nome = st.session_state.get("nome_input_key", user.get("nome_completo", ""))
        # O widget st.text_input com uma 'key' atualiza st.session_state[key] automaticamente.
        # NENHUM CALLBACK on_change é usado aqui.
        st.text_input(
            "Nome completo",
            value=valor_inicial_nome,
            key="nome_input_key", # Essencial para acessar o valor via st.session_state
            help="Seu nome completo como aparecerá no perfil."
        )
        
        st.markdown(f'<div class="unid-badge">Unidade: {user.get("unidade","Não definida")}</div>', unsafe_allow_html=True)
        st.text_input("Email (Login)", value=username, disabled=True, help="Seu email de login não pode ser alterado.")

        st.markdown("<hr style='border-color:#00A9E060; margin-top:1.5rem; margin-bottom:1rem;'>", unsafe_allow_html=True)
        st.markdown('<h4 style="color: #00A9E0; margin-bottom: 0.8rem;">Preferências do Assistente</h4>', unsafe_allow_html=True)

        # Preferência: Tom de Resposta
        tone_options = ["Neutro", "Amigável e Informal", "Profissional e Direto"]
        current_tone = user.get("assistant_tone", "Neutro") # Valor salvo para inicialização
        # O st.selectbox manterá seu estado. O valor selecionado será 'assistant_tone_selected_val' no submit.
        assistant_tone_selected_val = st.selectbox(
            "Tom de Resposta Preferido:",
            options=tone_options,
            index=tone_options.index(current_tone) if current_tone in tone_options else 0,
            key="assistant_tone_sb", # Chave para o estado do selectbox
            help="Escolha como você prefere que o assistente se comunique."
        )

        # Preferência: Nível de Detalhe
        detail_options = ["Conciso", "Equilibrado", "Detalhado"]
        current_detail = user.get("assistant_detail_level", "Equilibrado") # Valor salvo
        assistant_detail_level_selected_val = st.selectbox(
            "Nível de Detalhe nas Respostas:",
            options=detail_options,
            index=detail_options.index(current_detail) if current_detail in detail_options else 0,
            key="assistant_detail_sb", # Chave para o estado do selectbox
            help="Defina o quão detalhadas devem ser as respostas do assistente."
        )
        
        with st.expander("Alterar senha (Em Desenvolvimento)"):
            st.warning("No momento, a alteração de senha não está disponível através desta interface.", icon="🔒")
            st.text_input("Nova senha", type="password", disabled=True, key="new_pass_disabled")
            st.text_input("Confirmar nova senha", type="password", disabled=True, key="confirm_pass_disabled")
        
        submitted = st.form_submit_button("💾 Salvar alterações")
        
        if submitted:
            img_to_save = st.session_state.get("pfp_b64")
            # Pega o nome do st.session_state usando a chave do input
            nome_para_salvar = st.session_state.get("nome_input_key", user.get("nome_completo", ""))
            
            # Os valores dos selectboxes são lidos diretamente das variáveis que os receberam
            # no momento em que o formulário foi renderizado para este submit.
            dados_para_salvar = {
                "nome_completo": nome_para_salvar,
                "profile_image": img_to_save,
                "assistant_tone": assistant_tone_selected_val, # Valor do selectbox
                "assistant_detail_level": assistant_detail_level_selected_val # Valor do selectbox
            }
            save_user(username, dados_para_salvar)
            
            # Atualizar o dict 'user' em memória para reflexo imediato antes do rerun
            user.update(dados_para_salvar)
            
            st.success("🎉 Perfil atualizado com sucesso!", icon="✅")
            st.balloons()
            st.rerun() # Garante que toda a página (incluindo sidebar) reflita os dados salvos

    st.markdown('</div>', unsafe_allow_html=True)

# --- COMPONENTE GERENCIAMENTO DE DADOS ---
def export_data_section():
    st.markdown('<div class="data-management-section">', unsafe_allow_html=True)
    st.markdown('<h3>Gerenciamento de Dados</h3>', unsafe_allow_html=True)
    
    user_data_to_export = {
        "email_login": username,
        "nome_completo": user.get("nome_completo"),
        "unidade": user.get("unidade"),
        "preferencias_assistente": {
            "tom_resposta": user.get("assistant_tone"),
            "nivel_detalhe": user.get("assistant_detail_level")
        },
        "imagem_perfil_definida": bool(user.get("profile_image"))
        # Para incluir a imagem em base64 no JSON (pode tornar o arquivo grande):
        # "profile_image_base64": user.get("profile_image")
    }
    try:
        user_data_json = json.dumps(user_data_to_export, indent=4, ensure_ascii=False)
        file_name = f"{username}_dados_perfil.json"

        st.download_button(
            label="📥 Exportar Meus Dados (JSON)",
            data=user_data_json,
            file_name=file_name,
            mime="application/json",
            use_container_width=True,
            help="Faça o download das suas informações de perfil e preferências em formato JSON."
        )
        st.markdown("<p>Esta ação permite que você baixe uma cópia dos seus dados armazenados.</p>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Ocorreu um erro ao preparar os dados para exportação: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

# --- ORGANIZAÇÃO FINAL DA PÁGINA ---
st.markdown('<h1 style="text-align:center; margin-bottom:2.0rem;">Meu Perfil</h1>', unsafe_allow_html=True)

st.markdown('<div class="perfil-card">', unsafe_allow_html=True)
avatar_section()  # Renderiza a seção do avatar
perfil_form()     # Renderiza o formulário de perfil (agora corrigido)
st.markdown('</div>', unsafe_allow_html=True) # Fecha perfil-card

export_data_section() # Nova seção para gerenciamento de dados

