import streamlit as st
import os
import base64

# === THEME ===
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

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

def get_image_base64(path):
    if not os.path.exists(path): 
        return ""
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def sidebar_profile():
    user = st.session_state.get("user_full_name", "Usuário")
    unidade = st.session_state.get("user_unidade", "Unidade não definida")
    # Busca a foto de perfil: se não houver, mostra as iniciais
    user_img = st.session_state.get("user_profile_image")  # Espera-se base64 aqui
    initials = "".join([w[0] for w in user.split()[:2]]).upper()
    st.markdown('<div class="sidebar-profile">', unsafe_allow_html=True)
    if user_img:
        st.markdown(f'<div class="sidebar-avatar"><img src="data:image/png;base64,{user_img}"></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="sidebar-avatar"><span class="sidebar-avatar-initials">{initials}</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-username">{user}</div>', unsafe_allow_html=True)
    if st.session_state.get("authenticated", False):
        st.markdown(f'<div class="sidebar-email">{st.session_state.get("username","")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sidebar-unidade">Unidade: {unidade}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="sidebar-email">Visitante</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sidebar-unidade">Acesse para mais recursos</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def instructions_page():
    st.set_page_config(page_title="Instruções - MTI Assistente", layout="wide", page_icon="📖")
    # === CSS MODERNO ===
    st.markdown(f"""
    <style>
    body, .stApp {{
        background-color: {THEME['BACKGROUND']};
        color: {THEME['TEXT_SECONDARY']};
        font-family: 'Montserrat', 'Segoe UI', system-ui, -apple-system, sans-serif;
    }}
    .main .block-container {{
        padding: 0; max-width: 1200px;
    }}
    /* SIDEBAR ESTILO PERFEITO */
    [data-testid="stSidebar"] {{
        background: linear-gradient(185deg,#0b263d 60%, #0a1a2f 100%)!important;
        color: {THEME['LIGHT_GRAY']};
        border-right: 2px solid {THEME['ACCENT_LIGHT']};
        box-shadow: 7px 0 32px #00a9e04d;
        min-width: 310px !important;
        max-width: 360px !important;
    }}
    .sidebar-profile {{
        text-align: center;
        padding: 2.3rem 1rem 2.2rem 1rem;
        background: linear-gradient(120deg, #00529B 60%, #10284e 100%);
        border-bottom: 2.5px solid {THEME['ACCENT']};
        margin-bottom: 2.7rem;
        border-radius: 0 0 1.5rem 1.5rem;
    }}
    .sidebar-avatar {{
        width: 82px; height: 82px; border-radius: 50%; overflow: hidden;
        border: 3px solid {THEME['ACCENT']}; background: {THEME['BACKGROUND']};
        box-shadow: 0 0 0 8px {THEME['ACCENT_LIGHT']}36;
        margin: 0 auto 1.1rem auto;
        display: flex; align-items: center; justify-content: center;
    }}
    .sidebar-avatar img {{ width: 100%; height: 100%; object-fit: cover; }}
    .sidebar-avatar-initials {{ font-size: 2.6rem; color: #fff; font-weight: 800; }}
    .sidebar-username {{ font-size: 1.21rem; font-weight: 700; color: #fff; margin-bottom: .2rem; }}
    .sidebar-email {{ font-size: 0.97rem; color: {THEME['LIGHT_GRAY']}; margin-bottom:0.2rem; }}
    .sidebar-unidade {{ font-size: 0.91rem; color: {THEME['ACCENT_LIGHT']}; margin-bottom:0.6rem; }}
    .sidebar-footer {{
        font-size: 0.97rem; color: {THEME['LIGHT_GRAY']}; text-align: center; margin-top:2.2rem; padding: .7rem 0;
        border-top: 1px solid {THEME['ACCENT']};
    }}
    /* Sidebar links */
    .st-emotion-cache-1px2117.e1gf0u8t0 a {{
        color: {THEME['LIGHT_GRAY']}; font-size: 1.09rem; font-weight: 500;
        padding: 0.7rem 1.2rem; margin-bottom: 0.5rem; border-radius: .9rem;
        transition: background 0.16s, color 0.13s, transform 0.17s;
        display: flex; align-items: center; gap: 0.8rem;
    }}
    .st-emotion-cache-1px2117.e1gf0u8t0 a:hover {{
        background-color: {THEME['ACCENT']};
        color: #fff;
        transform: translateX(7px) scale(1.03);
    }}
    .st-emotion-cache-1px2117.e1gf0u8t0 a[data-st-page="true"] {{
        background: {THEME['PRIMARY']} !important;
        color: #fff !important;
        font-weight: 700;
        border-left: 4px solid {THEME['ACCENT_LIGHT']};
    }}
    /* LOGO */
    .sidebar-logo-container {{ text-align: center; margin-bottom: 2rem; }}
    .sidebar-logo-container img {{
        max-width: 140px; border-radius: 14px;
        box-shadow: 0 4px 18px #00a9e038;
        margin-top:0.7rem; margin-bottom:0.7rem;
        transition: transform .22s;
    }}
    .sidebar-logo-container img:hover {{ transform:scale(1.07); }}
    /* Content Card */
    .instructions-content-wrapper {{
        background-color: {THEME['CARD_BG']};
        padding: 2.7rem 2.7rem 3rem 2.7rem; 
        border-radius: 2.4rem; 
        border: 2px solid {THEME['ACCENT']};
        box-shadow: 0 15px 40px -12px {THEME['PRIMARY']}33;
        margin-bottom: 2rem;
        margin-top:2rem;
    }}
    .instructions-header h1 {{
        color: {THEME['TEXT_PRIMARY']}; font-size: 2.5rem; font-weight: 900;
        margin-bottom: 0.7rem; text-align: center; letter-spacing: -1px;
        text-shadow: 0 2px 8px {THEME['BACKGROUND_ALT']};
    }}
    .instructions-header .subtitle {{
        color: {THEME['LIGHT_GRAY']}; font-size: 1.25rem; text-align: center;
        margin-bottom: 2.3rem; line-height: 1.65;
        max-width: 800px; margin-left: auto; margin-right: auto;
    }}
    .emoji-title {{ margin-right: 0.8rem; font-size: 1.1em; vertical-align: middle; }}
    .section-divider-major, .section-divider {{
        border: 0; height: 2px;
        background-image: linear-gradient(to right, transparent, {THEME['ACCENT']}77, transparent);
        margin: 2.5rem auto 2.5rem auto; width: 85%;
    }}
    /* Accordions */
    [data-testid="stExpander"] > div {{
        background: {THEME['BACKGROUND_ALT']};
        border-radius: 1.3rem;
        border: 2px solid {THEME['ACCENT']};
        box-shadow: 0 3px 14px #00a9e02d;
        margin-bottom:1.3rem;
    }}
    [data-testid="stExpander"] label {{
        color: {THEME['ACCENT']}; 
        font-weight: 800; font-size: 1.19rem; letter-spacing: 0.5px;
    }}
    [data-testid="stExpander"] svg {{
        color: {THEME['ACCENT']};
    }}
    /* Table */
    .styled-table {{
        width: 100%; border-collapse:separate; border-spacing:0;
        margin-top: 1rem; margin-bottom: 1.5rem;
        font-size: 1rem; 
        box-shadow: 0 5px 12px #00a9e055;
        border-radius: 14px; overflow: hidden; 
    }}
    .styled-table th, .styled-table td {{
        border-bottom: 1px solid {THEME['BORDER_DARK']};
        padding: 1.1rem 1.1rem; text-align: left; 
    }}
    .styled-table th {{
        background-color: {THEME['PRIMARY']}; color: {THEME['TEXT_PRIMARY']};
        font-weight: 700; font-size: 1.05rem;
        border-top: 1px solid {THEME['BORDER_DARK']}; 
    }}
    .styled-table td strong {{ color: {THEME['ACCENT']}; }}
    .styled-table tbody tr:nth-child(even) {{ background-color: {THEME['BACKGROUND_ALT']}55; }} 
    .styled-table tbody tr:hover {{ background-color: {THEME['INPUT_BG']}77; transition: background-color 0.2s; }}
    /* Listas e dicas */
    .styled-list {{ list-style: none; padding-left: 0; margin-bottom: 1.2rem; }}
    .styled-list li {{
        padding: 0.5rem 0 0.5rem 2.2em; position: relative; margin-bottom: 0.7rem;
        color: {THEME['TEXT_SECONDARY']};
        transition: background-color 0.2s, transform 0.2s; border-radius: 6px;
    }}
    .styled-list li:hover {{ background-color: {THEME['INPUT_BG']}33; transform: translateX(5px); }}
    .styled-list li::before {{ content: '❖'; color: {THEME['ACCENT']}; position: absolute; left: 0.5em; top: 0.5em; font-size: 1.2em; }}
    .styled-list.check-list li::before {{ content: '✔️'; color: {THEME['SUCCESS']}; }}
    .styled-list.example-queries li::before {{ content: '💬'; color: {THEME['ACCENT_LIGHT']}; }}
    .styled-list.tips-list li::before {{ content: '💡'; color: {THEME['TEXT_ACCENT']}; }}
    .example-block {{
        background-color: {THEME['BACKGROUND_ALT']};
        border: 1px solid {THEME['BORDER_DARK']};
        border-left: 5px solid {THEME['ACCENT']};
        padding: 1.1rem 1.6rem; margin-top: 1rem; margin-bottom: 1.2rem;
        border-radius: 10px;
        box-shadow: 0 3px 8px #00a9e026;
    }}
    .example-label {{ font-size: 0.99em; color: {THEME['TEXT_TERTIARY']}; margin-bottom: 0.3rem; font-weight: 500; }}
    .example-label.bad {{ color: {THEME['ERROR']}; }}
    .example-label.good {{ color: {THEME['SUCCESS']}; }}
    blockquote {{
        margin: 0.5rem 0 0.5rem 0; padding: 0.8rem 1.1rem;
        border-radius: 8px; font-style: italic; color: {THEME['LIGHT_GRAY']};
        font-family: 'Courier New', Courier, monospace; font-size: 0.97em;
    }}
    blockquote.bad-example {{ background-color: {THEME['ERROR']}1A; border-left: 4px solid {THEME['ERROR']}; }}
    blockquote.good-example {{ background-color: {THEME['SUCCESS']}1A; border-left: 4px solid {THEME['SUCCESS']}; }}
    .final-greeting {{ font-weight: 700; color: {THEME['TEXT_PRIMARY']}; margin-top: 1.7rem; text-align:center; font-size: 1.13em; }}
    @media (max-width: 1050px) {{
        .instructions-content-wrapper {{ padding: 1.3rem 0.7rem; }}
    }}
    </style>
    <link href="https://fonts.googleapis.com/css?family=Montserrat:700,900,400&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

    # === SIDEBAR (APROVEITA O PERFIL MODERNO) ===
    with st.sidebar:
        st.markdown('</div>', unsafe_allow_html=True)
        sidebar_profile()
        st.page_link("ChatBot.py", label="Chat Assistente", icon="💬")
        st.page_link("pages/2_⚙️_Editar_Perfil.py", label="Editar Perfil", icon="🛠️")
        st.markdown('<div class="sidebar-footer">MTI Assistente v1.0<br>© 2024 Sua Empresa</div>', unsafe_allow_html=True)

    # === MAIN CONTENT ===
    st.markdown('<div class="instructions-content-wrapper">', unsafe_allow_html=True)
    st.markdown("""
    <div class="instructions-header">
        <h1><span class="emoji-title">👋</span> Bem-vindo ao MTI Assistente Estratégico</h1>
        <p class="subtitle">
            Seu canal inteligente para informações estratégicas da MTI.<br>
            <span style="font-size:1.07em;color:#71C5E8;">Acesse documentos, indicadores e práticas de gestão de forma rápida, interativa e segura.</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<hr class="section-divider-major">', unsafe_allow_html=True)

    # --- ACCORDIONS INTERATIVOS ---
    with st.expander("📚 Documentos e Temas Disponíveis", expanded=True):
        st.markdown("""
        <p>O assistente tem acesso a uma vasta gama de informações. Consulte a tabela:</p>
        <div class="table-responsive">
            <table class="styled-table">
                <thead>
                    <tr>
                        <th>Tema/Documento</th>
                        <th>Descrição Concisa</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td><strong>Estatuto Social</strong></td><td>Princípios e estrutura fundamental da MTI.</td></tr>
                    <tr><td><strong>Regimento Interno</strong></td><td>Normas de organização e funcionamento interno.</td></tr>
                    <tr><td><strong>Cadeia de Valor</strong></td><td>Processos chave para a geração de valor.</td></tr>
                    <tr><td><strong>Padronização</strong></td><td>Procedimentos para uniformizar atividades.</td></tr>
                    <tr><td><strong>Políticas e Normas</strong></td><td>Diretrizes institucionais para conduta e processos.</td></tr>
                    <tr><td><strong>PPA</strong></td><td>Planejamento estratégico de médio prazo.</td></tr>
                    <tr><td><strong>PTA</strong></td><td>Desdobramento operacional das estratégias anuais.</td></tr>
                    <tr><td><strong>Estratégia</strong></td><td>Objetivos, metas e planos de ação estratégicos.</td></tr>
                    <tr><td><strong>Indicadores</strong></td><td>Métricas de desempenho e acompanhamento de resultados.</td></tr>
                    <tr><td><strong>Riscos</strong></td><td>Identificação e gestão de riscos estratégicos.</td></tr>
                    <tr><td><strong>Avaliação da Gestão</strong></td><td>IMGG e iESGo para melhoria contínua.</td></tr>
                    <tr><td><strong>Práticas de Gestão</strong></td><td>Modelos e exemplos de excelência em gestão.</td></tr>
                </tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📝 Como Formular Suas Perguntas Eficazmente", expanded=False):
        st.markdown("""
        <ol class="styled-list interactive-list">
            <li>
                <h3>1. Clareza e Especificidade</h3>
                <p>Formule perguntas diretas e detalhadas. Quanto mais específico você for, melhor será a resposta.</p>
                <div class="example-block">
                    <p class="example-label bad">❌ Exemplo a evitar:</p>
                    <blockquote class="bad-example">"Me fale sobre indicadores."</blockquote>
                    <p class="example-label good">✔️ Exemplo ideal:</p>
                    <blockquote class="good-example">"Quais são os principais indicadores de desempenho da unidade de Recursos Humanos para o último trimestre?"</blockquote>
                </div>
            </li>
            <li>
                <h3>2. Contextualize com a Unidade</h3>
                <p>Sempre que aplicável, mencione a <strong>unidade organizacional</strong> (departamento, setor, diretoria) referente à sua consulta. Isso ajuda a IA a focar nos dados corretos.</p>
                <div class="example-block">
                    <p class="example-label">Exemplo:</p>
                    <blockquote>"Quais são os riscos estratégicos mapeados para a unidade de Tecnologia da Informação relacionados à segurança de dados?"</blockquote>
                </div>
            </li>
            <li><h3>3. Um Tema por Pergunta</h3><p>Para melhores resultados, concentre-se em um único tema ou questão por vez. Se tiver múltiplas dúvidas, envie-as separadamente.</p></li>
            <li>
                <h3>4. Detalhes Adicionais São Bem-vindos</h3>
                <p>Se sua pergunta se refere a um período específico, projeto, ou documento particular, inclua essa informação.</p>
                <div class="example-block">
                    <p class="example-label">Exemplo:</p>
                    <blockquote>"Gostaria do sumário executivo do relatório de avaliação da gestão (IMGG) da unidade de Compras referente ao ano de 2024."</blockquote>
                </div>
            </li>
            <li><h3>5. Linguagem Natural e Objetiva</h3><p>Use uma linguagem clara e comum. Evite excesso de jargões técnicos ou siglas se houver alternativas mais simples.</p></li>
            <li><h3>6. Utilize o Filtro de Foco</h3><p>Na barra lateral do chat, você pode selecionar um "Foco da Informação". Escolher o tema mais relevante para sua pergunta pode refinar a busca do assistente.</p></li>
        </ol>
        """, unsafe_allow_html=True)

    # GRID INTERATIVO (Boas práticas e exemplos lado a lado)
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("⭐ Boas Práticas de Uso", expanded=True):
            st.markdown("""
                <ul class="styled-list check-list">
                    <li>Revise sua pergunta para clareza antes de enviar.</li>
                    <li>Jamais compartilhe informações pessoais sensíveis, senhas ou dados confidenciais.</li>
                    <li>Se a resposta não for clara, reformule sua pergunta ou peça por mais detalhes.</li>
                    <li>Lembre-se que suas interações podem ser usadas para aprimorar o sistema e para fins de segurança.</li>
                    <li>Suas sugestões são valiosas! Utilize o canal de contato para feedback.</li>
                </ul>
            """, unsafe_allow_html=True)
    with col2:
        with st.expander("💬 Exemplos de Perguntas Bem Formuladas", expanded=True):
            st.markdown("""
                <ul class="styled-list example-queries">
                    <li>"Quais são as políticas de contratação e desenvolvimento de talentos vigentes para a unidade de Gestão de Pessoas (UGPES)?"</li>
                    <li>"Apresente um resumo dos indicadores de desempenho financeiro da Diretoria Administrativa (DAFI) para o exercício de 2023."</li>
                    <li>"Existe algum risco estratégico de alta criticidade identificado para a área de Tecnologia da Informação e Comunicação (DTIC) no plano atual?"</li>
                    <li>"Como está o progresso das metas estabelecidas no PTA da unidade de Compras (UGACO) para o corrente ano?"</li>
                </ul>
            """, unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    with st.expander("💡 Dicas Extras para Maximizar o Uso", expanded=False):
        st.markdown("""
            <ul class="styled-list tips-list">
                <li>Perguntas diretas e sem ambiguidades tendem a gerar respostas mais rápidas e precisas.</li>
                <li>Utilize o histórico de conversas (se disponível na sua interface) para revisitar informações anteriores.</li>
                <li>Não hesite em experimentar diferentes formulações para a mesma dúvida se a primeira tentativa não for ideal.</li>
                <li>Para informações muito específicas ou que exijam análise humana complexa, consulte também os especialistas da área.</li>
            </ul>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="section-divider-major">', unsafe_allow_html=True)

    with st.expander("🤝 Suporte e Contato", expanded=False):
        st.markdown("""
            <p>Para auxílio técnico, dúvidas sobre o uso do assistente ou sugestões de melhoria, por favor, entre em contato com a <strong>UGGOV (Unidade de Gestão de Apoio à Governança)</strong>.</p>
            <p class="final-greeting">Aproveite ao máximo o MTI Assistente Estratégico!</p>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    if 'authenticated' not in st.session_state: 
        st.session_state.authenticated = True 
    if 'user_full_name' not in st.session_state:
        st.session_state.user_full_name = "Usuário Teste" 
    if 'username' not in st.session_state:
        st.session_state.username = "usuario@empresa.com"
    if 'user_unidade' not in st.session_state:
        st.session_state.user_unidade = "Unidade Exemplo"
    if 'user_profile_image' not in st.session_state:
        st.session_state.user_profile_image = ""
    instructions_page()