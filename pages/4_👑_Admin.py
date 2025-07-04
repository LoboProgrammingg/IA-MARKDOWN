import streamlit as st
import json
import os
import base64

# THEME e UNIDADES_MTI (mantidos conforme o original)
THEME = {
    'PRIMARY': "#00529B",
    'SECONDARY': "#0078D4",
    'ACCENT': "#00A9E0",
    'ACCENT_LIGHT': "#71C5E8",
    'BACKGROUND': "#0A192F",
    'BACKGROUND_ALT': "#102A4C",
    'CARD_BG': "#1A2B44",
    'INPUT_BG': "#22304d",
    'BORDER_LIGHT': "#4A5568",
    'BORDER_DARK': "#2D3748",
    'TEXT_PRIMARY': "#FFFFFF",
    'TEXT_SECONDARY': "#E0E0E0",
    'TEXT_TERTIARY': "#A0AEC0",
    'TEXT_ACCENT': "#00A9E0",
    'LIGHT_GRAY': "#CBD5E0",
    'SUCCESS': "#38A169",
    'ERROR': "#E53E3E",
    'WARNING': "#DD6B20",
    'ICON_COLOR': "#A0AEC0",
    'SECTION_TITLE_TEXT': "#00A9E0",
}

# Adapte os caminhos conforme necessário.
# Esta estrutura assume que este script (ex: 4_👑_Admin.py) está numa pasta 'pages'
# e 'user.json' e a pasta 'documentation' estão no diretório pai.
try:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
except NameError: # __file__ não é definido em alguns contextos (ex: Streamlit Cloud com entrada direta de script)
    BASE_DIR = os.getcwd() # Use o diretório atual como fallback

USERS_FILE = os.path.join(BASE_DIR, "user.json")
LOGO_PATH = os.path.join(BASE_DIR, "documentation", "mti.png")


UNIDADES_MTI = {
    "GADP": "GABINETE DO DIRETOR-PRESIDENTE",
    "UGGOV": "UGGOV (UNIDADE DE GESTÃO DE APOIO À GOVERNANÇA)",
    "UGPRO": "UGPRO (UNIDADE DE GESTÃO DE PROJETOS)",
    "OUVIDORIA": "OUVIDORIA (OUVIDORIA E TRANSPARÊNCIA)",
    "UNIJUR": "UNIJUR (UNIDADE DE ASSESSORIA JURÍDICA)",
    "ASSCOM": "ASSCOM (UNIDADE DE ASSESSORIA DE COMUNICAÇÃO E MARKETING)",
    "UNISECI": "UNISECI (UNIDADE SETORIAL DE CONTROLE INTERNO)",
    "UNICRS": "UNICRS (UNIDADE DE GESTÃO DE CONFORMIDADE, RISCOS E SEGURANÇA DA INFORMAÇÃO)",
    "DAFI": "GABINETE DA DIRETORIA ADMINISTRATIVA",
    "UGOFF": "UGOFF (UNIDADE DE GESTÃO ORÇAMENTÁRIA, FINANCEIRA E FATURAMENTO)",
    "UGCOF": "UGCOF (UNIDADE DE GESTÃO CONTÁBIL E FISCAL)",
    "UGADM": "UGADM (UNIDADE DE GESTÃO ADMINISTRATIVA)",
    "UGPES": "UGPES (UNIDADE DE GESTÃO DE PESSOAS)",
    "UGACO": "UGACO (UNIDADE DE GESTÃO DE AQUISIÇÕES E CONTRATOS)",
    "DIRC_GAB": "DIRC (GABINETE DA DIRETORIA DE RELACIONAMENTO COM CLIENTE)",
    "UGVEN": "UGVEN (UNIDADE DE GESTÃO DE VENDAS)",
    "UGEPV": "UGEPV (UNIDADE DE GESTÃO DE PÓS-VENDA)",
    "UGENP": "UGENP (UNIDADE DE GESTÃO DE NOVOS NEGÓCIOS E PARCERIAS)",
    "DTIC_GAB": "DTIC (GABINETE DA DIRETORIA DE TECNOLOGIA DA INFORMAÇÃO E COMUNICAÇÃO)",
    "UGSTI": "UGSTI (UNIDADE DE GESTÃO DE SERVIÇOS DE TECNOLOGIA DA INFORMAÇÃO E COMUNICAÇÃO)",
    "UGITI": "UGITI (UNIDADE DE GESTÃO DE INFRAESTRUTURA DE TECNOLOGIA DA INFORMAÇÃO E COMUNICAÇÃO)",
    "UGSDG": "UGSDG (UNIDADE DE GESTÃO DE SOLUÇÕES DIGITAIS DE GOVERNO)",
    "UGGDC": "UGGDC (UNIDADE DE GESTÃO DE GOVERNANÇA DE DADOS E DEFESA CIBERNÉTICA)",
    "UGGDI": "UGGDI (UNIDADE DE GESTÃO DE GOVERNO DIGITAL)",
    "UGARQ": "UGARQ (UNIDADE DE GESTÃO DE ARQUITETURA TECNOLÓGICA)",
    "N/A": "Não Aplicável / Outra"
}

def get_image_base64(path):
    """Converte uma imagem para base64."""
    if not os.path.exists(path): return ""
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except Exception as e:
        # st.error(f"Erro ao carregar imagem {path}: {e}") # Descomente para depuração
        return ""


def load_users_admin():
    """Carrega os dados dos usuários do arquivo JSON."""
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f) # Cria um JSON vazio se o arquivo não existir
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        # st.error(f"Erro ao carregar user.json: {e}. Criando um novo.") # Descomente para depuração
        return {} # Retorna dicionário vazio em caso de erro

def save_users_admin(users_data):
    """Salva os dados dos usuários no arquivo JSON."""
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"Erro ao salvar user.json: {e}")


def initials(name):
    """Gera iniciais a partir de um nome completo."""
    if not name or not isinstance(name, str): return "A" # Retorno padrão
    parts = name.strip().split()
    if not parts: return "A"
    return (parts[0][0] + (parts[1][0] if len(parts) > 1 else "")).upper()

def sidebar_profile():
    """Exibe o perfil do usuário na barra lateral."""
    user = st.session_state.get("user_full_name", "Administrador")
    unidade_key = st.session_state.get("user_unidade", "N/A")
    unidade_nome_completo = UNIDADES_MTI.get(unidade_key, "Unidade não definida")
    user_img_b64 = st.session_state.get("user_profile_image") # Imagem de perfil em base64
    initials_val = initials(user)
    
    st.markdown('<div class="sidebar-profile">', unsafe_allow_html=True)
    if user_img_b64:
        st.markdown(f'<div class="sidebar-avatar"><img src="data:image/png;base64,{user_img_b64}"></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="sidebar-avatar"><span class="sidebar-avatar-initials">{initials_val}</span></div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="sidebar-username">{user}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-email">{st.session_state.get("username","")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-unidade" title="{unidade_nome_completo}">Unidade: {unidade_key}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def admin_css():
    """Aplica o CSS customizado para a página de administração."""
    st.markdown(f"""
    <style>
    body, .stApp {{
        background: {THEME['BACKGROUND']};
        color: {THEME['TEXT_SECONDARY']};
    }}
    .main .block-container {{
        padding: 1rem 1.5rem; /* Padding geral do container principal */
        max-width: 1300px; 
    }}
    [data-testid="stSidebar"] {{
        background: linear-gradient(185deg,#0b263d 60%, #0a1a2f 100%)!important;
        color: {THEME['LIGHT_GRAY']};
        border-right: 2px solid {THEME['ACCENT_LIGHT']};
        box-shadow: 7px 0 32px #00a9e04d;
        min-width: 300px !important; /* Ajustado */
        max-width: 350px !important; /* Ajustado */
    }}
    .sidebar-profile {{
        text-align: center;
        padding: 2rem 1rem 1.8rem 1rem; /* Ajustado */
        background: linear-gradient(120deg, {THEME['PRIMARY']} 60%, {THEME['BACKGROUND_ALT']} 100%);
        border-bottom: 2.5px solid {THEME['ACCENT']};
        margin-bottom: 2.5rem; /* Ajustado */
        border-radius: 0 0 1.3rem 1.3rem; /* Ajustado */
    }}
    .sidebar-avatar {{
        width: 78px; height: 78px; border-radius: 50%; overflow: hidden; /* Ajustado */
        border: 3px solid {THEME['ACCENT']}; background: {THEME['BACKGROUND']};
        box-shadow: 0 0 0 7px {THEME['ACCENT_LIGHT']}36; /* Ajustado */
        margin: 0 auto 1rem auto; /* Ajustado */
        display: flex; align-items: center; justify-content: center;
    }}
    .sidebar-avatar img {{ width: 100%; height: 100%; object-fit: cover; }}
    .sidebar-avatar-initials {{ font-size: 2.4rem; color: #fff; font-weight: 800; }} /* Ajustado */
    .sidebar-username {{ font-size: 1.15rem; font-weight: 700; color: #fff; margin-bottom: .15rem; }} /* Ajustado */
    .sidebar-email {{ font-size: 0.9rem; color: {THEME['LIGHT_GRAY']}; margin-bottom:0.15rem; }} /* Ajustado */
    .sidebar-unidade {{ font-size: 0.85rem; color: {THEME['ACCENT_LIGHT']}; margin-bottom:0.5rem; }} /* Ajustado */
    .sidebar-footer {{
        font-size: 0.9rem; color: {THEME['LIGHT_GRAY']}; text-align: center; margin-top:2rem; padding: .6rem 0; /* Ajustado */
        border-top: 1px solid {THEME['ACCENT']};
    }}
    .sidebar-logo-container {{ text-align: center; margin-bottom: 1.8rem; }} /* Ajustado */
    .sidebar-logo-container img {{
        max-width: 130px; border-radius: 12px; /* Ajustado */
        box-shadow: 0 4px 16px #00a9e038; /* Ajustado */
        margin-top:0.6rem; margin-bottom:0.6rem; /* Ajustado */
    }}

    /* Estilos para a "tabela" baseada em colunas */
    .user-row-header, .user-row {{
        display: flex; /* Essencial para que flex-grow funcione nas células */
        align-items: center;
        padding: 0.6rem 0.4rem; /* Padding vertical e horizontal */
        border-bottom: 1.5px solid {THEME['BORDER_DARK']};
        color: {THEME['LIGHT_GRAY']};
        min-height: 50px; /* Altura mínima para consistência */
    }}
    .user-row-header {{
        background: {THEME['PRIMARY']};
        color: #fff;
        font-weight: 700;
        font-size: 1.05rem; /* Ajustado */
        border-top-left-radius: 10px; /* Ajustado */
        border-top-right-radius: 10px; /* Ajustado */
        padding-top: 0.8rem; /* Mais padding no topo do header */
        padding-bottom: 0.8rem; /* Mais padding em baixo do header */
    }}
    .user-row {{ /* Estilo para as linhas de dados */
        background-color: {THEME['BACKGROUND_ALT']};
    }}
    .user-row:nth-child(even) {{ /* Linhas pares com cor de fundo ligeiramente diferente */
        background-color: {THEME['CARD_BG']};
    }}
    .user-row:last-child {{
        border-bottom: none;
        border-bottom-left-radius: 10px; /* Ajustado */
        border-bottom-right-radius: 10px; /* Ajustado */
    }}
    .user-row:hover {{
        background: {THEME['INPUT_BG']};
        box-shadow: inset 0 0 10px {THEME['ACCENT']}30; /* Efeito sutil no hover */
    }}
    .user-cell {{
        padding: 0.4rem 0.6rem; /* Padding interno da célula */
        word-break: break-word;
        display: flex; /* Para alinhar verticalmente o conteúdo da célula */
        align-items: center; /* Alinhamento vertical */
    }}
    .user-cell.actions {{ /* Célula de ações específica */
        justify-content: center; /* Centraliza os botões de ação */
    }}
    .admin-yes {{ color: {THEME['SUCCESS']}; font-weight:700; }}
    .admin-no {{ color: {THEME['ERROR']}; font-weight:700; }}
    
    .action-button-cell .stButton>button {{
        background: transparent !important;
        border: none !important;
        padding: 0.2rem !important; 
        font-size: 1.15rem !important; 
        min-width: auto !important;
        width: auto !important;
        margin: 0 0.15rem !important; 
        color: {THEME['ACCENT_LIGHT']} !important;
        line-height: 1; /* Para melhor alinhamento vertical do ícone */
    }}
    .action-button-cell .stButton>button:hover {{
        color: {THEME['ACCENT']} !important;
        transform: scale(1.1);
    }}
    .action-button-cell .stButton.delete-action>button {{ 
         color: {THEME['WARNING']} !important;
    }}
    .action-button-cell .stButton.delete-action>button:hover {{
         color: {THEME['ERROR']} !important;
    }}

    /* Botões Primários e de Deleção (gerais) */
    .stButton>button {{ /* Seletor genérico para botões Streamlit */
        border-radius: 8px !important;
        font-weight: 600 !important; /* Ajustado */
        font-size: 1rem !important; /* Ajustado */
        padding: 0.45rem 1.1rem !important; /* Ajustado */
        color: #fff !important;
        background: linear-gradient(95deg, {THEME['SECONDARY']}, {THEME['ACCENT']}) !important; /* Gradiente ajustado */
        transition: all .2s ease-in-out;
        border: none;
        box-shadow: 0 2px 5px #00000030;
    }}
    .stButton>button:hover {{
        box-shadow: 0 4px 12px {THEME['ACCENT_LIGHT']}50; /* Sombra no hover ajustada */
        transform: translateY(-1px);
    }}
    .stButton>button:disabled {{
        background: {THEME['BORDER_DARK']} !important;
        opacity: 0.7;
        cursor: not-allowed;
    }}
    
    /* Classe específica para botões de confirmação/submissão de formulário */
    .stButton[kind="formSubmit"]>button {{
         background: linear-gradient(95deg, {THEME['SUCCESS']}, {THEME['SECONDARY']}) !important;
    }}

    .stButton.delete-btn-class>button {{ /* Botão de deleção principal (ex: no diálogo) */
        background: linear-gradient(95deg, {THEME['ERROR']}, {THEME['WARNING']}) !important;
    }}
    .stButton.delete-btn-class>button:hover {{
         box-shadow: 0 4px 12px {THEME['WARNING']}50;
    }}

    [data-testid="stDialog"] {{
        background-color: {THEME['BACKGROUND_ALT']};
        border: 1px solid {THEME['ACCENT']};
        border-radius: 10px; /* Ajustado */
        box-shadow: 0 8px 30px #00000050;
    }}
    [data-testid="stDialog"] h1 {{ /* Título do diálogo */
        color: {THEME['ACCENT_LIGHT']};
        font-size: 1.4rem; /* Ajustado */
        border-bottom: 1px solid {THEME['BORDER_DARK']};
        padding-bottom: 0.8rem;
        margin-bottom: 1rem;
    }}
    .pagination-container {{
        text-align: center;
        margin-top: 0.8rem; /* Ajustado */
        color: {THEME['LIGHT_GRAY']};
        font-size: 0.95rem; /* Ajustado */
    }}
    </style>
    """, unsafe_allow_html=True)

def admin_page():
    """Função principal para renderizar a página de administração."""
    st.set_page_config(page_title="Admin - MTI Assistente", layout="wide", page_icon="👑")
    admin_css()

    # Inicialização de chaves de estado da sessão para diálogos e paginação
    if 'editing_user_key' not in st.session_state:
        st.session_state.editing_user_key = None
    if 'deleting_user_key' not in st.session_state:
        st.session_state.deleting_user_key = None
    if 'admin_page_num' not in st.session_state:
        st.session_state.admin_page_num = 1


    # --- Barra Lateral ---
    with st.sidebar:
        st.markdown('<div class="sidebar-logo-container">', unsafe_allow_html=True)
        logo_b64_sidebar = get_image_base64(LOGO_PATH)
        if logo_b64_sidebar:
            st.image(f"data:image/png;base64,{logo_b64_sidebar}", width=130)
        else:
            # Fallback se o logo não carregar
            st.markdown(f"<h3 style='color:{THEME['ACCENT_LIGHT']}; text-align:center;'>MTI Assistente</h3>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        sidebar_profile()
        # Adapte os nomes dos arquivos de página se forem diferentes
        st.page_link("ChatBot.py", label="Chat Assistente") 
        st.page_link("pages/2_⚙️_Editar_Perfil.py", label="Editar Perfil", icon="🛠️") 
        st.markdown('<div class="sidebar-footer">MTI Assistente v1.2<br>© 2024 MTI</div>', unsafe_allow_html=True)

    # --- Título Principal da Página ---
    st.markdown(f"""
    <div style="margin-top:1.2rem; margin-bottom:1.8rem;">
        <h1 style="text-align:center; font-size:2.7rem; color:{THEME['TEXT_PRIMARY']}; font-weight:800; letter-spacing:-1.2px; text-shadow:0 2px 10px {THEME['PRIMARY']}50;">
            👑 Painel de Administração
        </h1>
        <p style="color:{THEME['TEXT_TERTIARY']}; font-size:1.1rem; text-align:center; margin-bottom:1.8rem;">
            Gestão de usuários, permissões e unidades do <b>MTI Assistente</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- Verificação de Autenticação e Permissão de Admin ---
    if not st.session_state.get("authenticated", False) or not st.session_state.get("is_admin", False):
        st.error("🔒 Acesso negado. Você precisa estar autenticado como administrador para visualizar esta página.")
        if st.button("Ir para Login", key="login_redirect_admin"): 
            st.switch_page("ChatBot.py") # Adapte para sua página de login
        return

    users = load_users_admin()
    if not isinstance(users, dict): # Tratamento de erro se o arquivo estiver corrompido
        st.error("⚠️ Arquivo de usuários (user.json) parece estar corrompido ou mal formatado. Carregando lista vazia.")
        users = {} 

    # --- Card: Adicionar Novo Usuário ---
    with st.container():
        st.markdown('<div class="admin-card">', unsafe_allow_html=True)
        st.markdown(f'<h2 style="color:{THEME["SECTION_TITLE_TEXT"]}; font-size:1.7rem; font-weight:700; margin-bottom:1.3rem; text-align:center;">➕ Adicionar Novo Usuário</h2>', unsafe_allow_html=True)
        
        with st.form("add_user_form", clear_on_submit=True):
            cols_add_1 = st.columns(2)
            with cols_add_1[0]:
                novo_user = st.text_input("👤 Login (email ou nome de usuário)", key="add_user_login_input", placeholder="ex: usuario@mti.gov.br")
            with cols_add_1[1]:
                novo_nome = st.text_input("📝 Nome Completo", key="add_user_nome_input", placeholder="Ex: João da Silva")
            
            cols_add_2 = st.columns([2,1,1])
            with cols_add_2[0]:
                novo_senha = st.text_input("🔑 Senha", type="password", key="add_user_senha_input", placeholder="Mínimo 8 caracteres")
            with cols_add_2[1]:
                novo_admin = st.checkbox("👑 Admin?", key="add_user_isadmin_input", help="Marcar se o usuário terá permissões de administrador.")
            with cols_add_2[2]:
                novo_unidade = st.selectbox("🏢 Unidade", list(UNIDADES_MTI.keys()), format_func=lambda x: f"{x} ({UNIDADES_MTI[x][:20]}...)", key="add_user_unidade_input")
            
            # Botão de submissão do formulário
            submitted_add = st.form_submit_button("💾 Cadastrar Usuário", use_container_width=True)
            if submitted_add:
                if not novo_user or not novo_nome or not novo_senha:
                    st.error("❗ Por favor, preencha todos os campos obrigatórios (Login, Nome, Senha)!")
                elif novo_user in users:
                    st.error(f"🚫 Login '{novo_user}' já está em uso. Escolha outro.")
                elif len(novo_senha) < 8:
                    st.error("🔒 A senha deve conter pelo menos 8 caracteres.")
                else:
                    users[novo_user] = {
                        "nome_completo": novo_nome,
                        "password": novo_senha, # Lembrete: Em produção, use HASHING de senhas!
                        "is_admin": novo_admin,
                        "unidade": novo_unidade,
                        "profile_image_b64": "" # Campo para imagem de perfil, inicializado vazio
                    }
                    save_users_admin(users)
                    st.success(f"✅ Usuário '{novo_nome}' adicionado com sucesso!")
                    st.toast(f"🎉 Usuário '{novo_nome}' cadastrado!", icon="👍")
                    st.rerun() # Recarrega a página para atualizar a lista

        st.markdown('</div>', unsafe_allow_html=True) # Fecha admin-card

    # --- Card: Filtros e Informações de Paginação ---
    st.markdown('<div class="admin-card" style="padding:1.3rem 1.8rem;">', unsafe_allow_html=True)
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        filtro_unidade = st.selectbox("🔍 Filtrar por Unidade:", ["Todas"] + list(UNIDADES_MTI.keys()), format_func=lambda x: "Todas as Unidades" if x=="Todas" else f"{x} ({UNIDADES_MTI[x][:25]}...)", key="admin_filter_unidade")
    with col_filter2:
        filtro_admin = st.selectbox("👤 Filtrar por Perfil:", ["Todos", "Apenas Admins", "Apenas Usuários"], key="admin_filter_admin")
    
    user_list = [
        (uname, udata) for uname, udata in users.items()
        if (filtro_unidade == "Todas" or udata.get("unidade") == filtro_unidade)
        and (filtro_admin == "Todos" or 
             (filtro_admin == "Apenas Admins" and udata.get("is_admin")) or 
             (filtro_admin == "Apenas Usuários" and not udata.get("is_admin")))
    ]
    
    per_page = 7 # Número de usuários por página
    total_pages = max(1, (len(user_list) + per_page - 1) // per_page)
    current_page_num = st.session_state.get('admin_page_num', 1)

    # Controles de Paginação
    pagination_cols_container = st.container()
    with pagination_cols_container:
        p_col1, p_col2, p_col3, p_col4 = st.columns([2,1,1,2]) # Ajustado para centralizar
        with p_col1:
            if st.button("⬅️ Anterior", use_container_width=True, disabled=(current_page_num <= 1), key="btn_prev_page"):
                st.session_state.admin_page_num = current_page_num - 1
                st.rerun()
        with p_col2:
            # Exibe a informação da página atual de forma mais centralizada
            st.markdown(f"<div style='text-align:center; margin-top:0.5rem; color:{THEME['TEXT_TERTIARY']};'>Página {current_page_num} de {total_pages}</div>", unsafe_allow_html=True)
        with p_col3:
             if st.button("Próxima ➡️", use_container_width=True, disabled=(current_page_num >= total_pages), key="btn_next_page"):
                st.session_state.admin_page_num = current_page_num + 1
                st.rerun()
        # with p_col4: # Espaçador

    st.markdown(f'<div class="pagination-container" style="margin-top:0.3rem;">Total de usuários filtrados: <b>{len(user_list)}</b></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True) # Fecha admin-card dos filtros


    # --- Card: Lista de Usuários ---
    st.markdown('<div class="admin-card" style="padding:1rem 1.3rem;">', unsafe_allow_html=True)
    st.markdown(f'<h3 style="color:{THEME["TEXT_ACCENT"]}; font-size:1.5rem; font-weight:600; margin-bottom:0.8rem;">👥 Usuários Cadastrados</h3>', unsafe_allow_html=True)

    # Definição das proporções das colunas para cabeçalho e linhas
    column_proportions = [3, 4, 2.5, 1.5, 2] 
    headers_text = ["Login", "Nome Completo", "Unidade", "Admin?", "Ações"]
    
    # Renderização do Cabeçalho da Lista
    header_html_cells = []
    for prop, text in zip(column_proportions, headers_text):
        align_style = "text-align:center;" if text in ["Admin?", "Ações"] else "text-align:left;"
        # Usar flex-grow para distribuir o espaço conforme as proporções
        header_html_cells.append(f'<div class="user-cell" style="flex-grow:{prop}; flex-basis:0; min-width:0; {align_style}">{text}</div>')
    st.markdown(f'<div class="user-row-header">{"".join(header_html_cells)}</div>', unsafe_allow_html=True)

    # Renderização dos Itens da Lista (usuários)
    start_index = (current_page_num - 1) * per_page
    end_index = start_index + per_page
    
    if not user_list[start_index:end_index]:
        st.info("ℹ️ Nenhum usuário encontrado com os filtros aplicados nesta página.")

    for uname, udata in user_list[start_index:end_index]:
        admin_status_html = f'<span class="admin-yes">Sim</span>' if udata.get("is_admin") else f'<span class="admin-no">Não</span>'
        unidade_sigla = udata.get('unidade', 'N/A')
        unidade_nome_completo_tooltip = UNIDADES_MTI.get(unidade_sigla, "Não especificada")
        
        # Envolver cada linha com a div .user-row para aplicar estilos de hover e borda
        st.markdown('<div class="user-row">', unsafe_allow_html=True)
        
        # Usar st.columns para criar as células da linha, respeitando as proporções
        data_cols = st.columns(column_proportions)
        
        with data_cols[0]: # Login
            st.markdown(f'<div class="user-cell">{uname}</div>', unsafe_allow_html=True)
        with data_cols[1]: # Nome Completo
            st.markdown(f'<div class="user-cell">{udata.get("nome_completo","")}</div>', unsafe_allow_html=True)
        with data_cols[2]: # Unidade
            st.markdown(f'<div class="user-cell" title="{unidade_nome_completo_tooltip}">{unidade_sigla}</div>', unsafe_allow_html=True)
        with data_cols[3]: # Admin?
            st.markdown(f'<div class="user-cell" style="text-align:center;">{admin_status_html}</div>', unsafe_allow_html=True)
        with data_cols[4]: # Ações
            # Wrapper para centralizar os botões e aplicar estilos de .action-button-cell
            st.markdown('<div class="user-cell actions action-button-cell">', unsafe_allow_html=True)
            
            action_buttons_cols = st.columns([1,1]) # Sub-colunas para os botões de ação
            with action_buttons_cols[0]:
                if st.button("✏️", key=f"edit_btn_{uname}", help=f"Editar usuário {uname}", use_container_width=True):
                    st.session_state.editing_user_key = uname
                    st.rerun() 
            with action_buttons_cols[1]:
                # Adiciona a classe CSS 'delete-action' para o botão de deletar
                st.markdown('<div class="stButton delete-action">', unsafe_allow_html=True)
                if st.button("🗑️", key=f"remove_btn_{uname}", help=f"Remover usuário {uname}", use_container_width=True):
                    st.session_state.deleting_user_key = uname
                    st.rerun() 
                st.markdown('</div>', unsafe_allow_html=True) # Fecha o wrapper do botão de deletar
            st.markdown('</div>', unsafe_allow_html=True) # Fecha .user-cell.actions.action-button-cell
        st.markdown('</div>', unsafe_allow_html=True) # Fecha .user-row

    st.markdown('</div>', unsafe_allow_html=True) # Fecha admin-card da lista

    # --- Diálogo de Edição ---
    if st.session_state.editing_user_key:
        uname_to_edit = st.session_state.editing_user_key
        udata_to_edit = users.get(uname_to_edit) # users é o dicionário carregado

        if udata_to_edit: # Garante que o usuário ainda existe
            current_unidade_key = udata_to_edit.get("unidade", "N/A")
            # Garante que a unidade exista no dict, ou usa a primeira como fallback seguro
            unidade_keys_list = list(UNIDADES_MTI.keys())
            default_unidade_idx = unidade_keys_list.index(current_unidade_key) if current_unidade_key in unidade_keys_list else 0
            
            @st.dialog(f"✏️ Editar Usuário: {uname_to_edit}", dismissible=True)
            def edit_user_dialog_content():
                st.markdown(f"**Editando:** {udata_to_edit.get('nome_completo', uname_to_edit)}")
                with st.form(key=f"edit_form_{uname_to_edit}"):
                    new_nome_edit = st.text_input("👤 Nome completo", value=udata_to_edit.get("nome_completo", ""), key=f"edit_input_nome_{uname_to_edit}")
                    new_unidade_edit = st.selectbox("🏢 Nova unidade", unidade_keys_list, index=default_unidade_idx, format_func=lambda x: f"{x} ({UNIDADES_MTI[x][:20]}...)", key=f"edit_select_unidade_{uname_to_edit}")
                    new_admin_edit = st.checkbox("👑 Administrador?", value=udata_to_edit.get("is_admin", False), key=f"edit_check_admin_{uname_to_edit}")
                    new_senha_edit = st.text_input("🔑 Nova senha (deixe em branco para não alterar)", type="password", key=f"edit_input_senha_{uname_to_edit}", placeholder="Mínimo 8 caracteres se preenchido")

                    # Botões dentro do formulário do diálogo
                    submit_col, cancel_col = st.columns(2)
                    with submit_col:
                        if st.form_submit_button("💾 Salvar Alterações", use_container_width=True):
                            if not new_nome_edit:
                                st.error("❗ Nome completo não pode ser vazio.")
                                return # Mantém o diálogo aberto

                            users[uname_to_edit]["nome_completo"] = new_nome_edit
                            users[uname_to_edit]["unidade"] = new_unidade_edit
                            users[uname_to_edit]["is_admin"] = new_admin_edit
                            if new_senha_edit: # Se uma nova senha foi fornecida
                                if len(new_senha_edit) < 8:
                                    st.error("🔒 Nova senha deve ter ao menos 8 caracteres.")
                                    return # Mantém o diálogo aberto
                                users[uname_to_edit]["password"] = new_senha_edit # Lembrete: HASHING!
                            
                            save_users_admin(users)
                            st.success(f"✅ Usuário '{new_nome_edit}' atualizado com sucesso!")
                            st.toast(f"💾 Alterações salvas para {new_nome_edit}!", icon="👍")
                            st.session_state.editing_user_key = None # Fecha o diálogo
                            st.rerun()
                    with cancel_col:
                        # O botão de cancelar não é um submit do form, apenas fecha o diálogo
                        if st.button("❌ Cancelar", key=f"cancel_edit_dialog_{uname_to_edit}", use_container_width=True):
                            st.session_state.editing_user_key = None
                            st.rerun()
            edit_user_dialog_content() # Chama a função que define o diálogo

    # --- Diálogo de Deleção ---
    if st.session_state.deleting_user_key:
        uname_to_delete = st.session_state.deleting_user_key
        user_to_delete_data = users.get(uname_to_delete)

        if user_to_delete_data: # Garante que o usuário ainda existe
            @st.dialog(f"🗑️ Confirmar Remoção", dismissible=True)
            def delete_user_dialog_content():
                st.warning(f"Tem certeza que deseja remover o usuário **{uname_to_delete}** ({user_to_delete_data.get('nome_completo', '')})?")
                st.markdown("Esta ação não poderá ser desfeita.")
                
                # Classe CSS delete-btn-class para o botão de confirmação de deleção
                st.markdown('<div class="stButton delete-btn-class">', unsafe_allow_html=True)
                confirm_delete = st.button(f"🗑️ Sim, remover {uname_to_delete}", key=f"confirm_delete_dialog_{uname_to_delete}", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

                if confirm_delete:
                    if uname_to_delete == st.session_state.get("username"):
                        st.error("🚫 Você não pode remover a si mesmo enquanto estiver logado.")
                    else:
                        deleted_name_display = user_to_delete_data.get("nome_completo", uname_to_delete)
                        del users[uname_to_delete]
                        save_users_admin(users)
                        st.success(f"✅ Usuário '{deleted_name_display}' removido com sucesso!")
                        st.toast(f"🗑️ Usuário '{deleted_name_display}' removido.", icon="👍")
                        st.session_state.deleting_user_key = None # Fecha o diálogo
                        st.rerun()
                
                if st.button("❌ Cancelar", key=f"cancel_delete_dialog_{uname_to_delete}", use_container_width=True):
                    st.session_state.deleting_user_key = None
                    st.rerun()
            delete_user_dialog_content()


# Bloco principal para execução e teste da página
if __name__ == "__main__":
    # Simulação do estado da sessão para fins de teste desta página isoladamente
    # Certifique-se de que os caminhos para USERS_FILE e LOGO_PATH estão corretos
    # ou que os arquivos existem nos locais esperados.

    # Inicializa o estado da sessão para teste
    if 'authenticated' not in st.session_state: 
        st.session_state.authenticated = True # Mude para False para testar o bloqueio de acesso
    if 'is_admin' not in st.session_state: 
        st.session_state.is_admin = True # Mude para False para testar o bloqueio de admin
    if 'username' not in st.session_state: 
        st.session_state.username = "admin.dev@mti.com" # Usuário de teste
    if 'user_full_name' not in st.session_state: 
        st.session_state.user_full_name = "Admin Desenvolvedor"
    if 'user_unidade' not in st.session_state: 
        st.session_state.user_unidade = "GADP" # Uma chave válida de UNIDADES_MTI
    if 'user_profile_image' not in st.session_state: 
        st.session_state.user_profile_image = "" # Pode ser uma string base64 de imagem para teste

    # Cria um arquivo user.json de exemplo se não existir para facilitar os testes
    if not os.path.exists(USERS_FILE):
        print(f"Arquivo {USERS_FILE} não encontrado. Criando um arquivo de exemplo para teste.")
        sample_users_data = {
            "admin.dev@mti.com": {"nome_completo": "Admin Desenvolvedor", "password": "securepassword123", "is_admin": True, "unidade": "GADP", "profile_image_b64": ""},
            "user.test1@mti.com": {"nome_completo": "Usuário de Teste Um", "password": "testpassword", "is_admin": False, "unidade": "UGPRO", "profile_image_b64": ""},
            "user.test2@mti.com": {"nome_completo": "Usuário de Teste Dois", "password": "anotherpassword", "is_admin": False, "unidade": "UGVEN", "profile_image_b64": ""},
            "maria.admin@mti.com": {"nome_completo": "Maria Administradora", "password": "adminpass", "is_admin": True, "unidade": "DAFI", "profile_image_b64": ""},
            "joao.user@mti.com": {"nome_completo": "João Usuário Padrão", "password": "userpass", "is_admin": False, "unidade": "UGEPV", "profile_image_b64": ""}
        }
        # Adiciona mais alguns usuários para testar a paginação
        for i in range(3, 15):
            sample_users_data[f"user.gen{i}@mti.com"] = {
                "nome_completo": f"Usuário Gerado {i}", 
                "password": f"pass{i}", 
                "is_admin": i % 3 == 0, # Alguns admins, outros não
                "unidade": list(UNIDADES_MTI.keys())[i % len(UNIDADES_MTI)], # Distribui unidades
                "profile_image_b64": ""
            }
        save_users_admin(sample_users_data)
    
    admin_page()