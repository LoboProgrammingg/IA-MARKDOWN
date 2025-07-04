import streamlit as st
import os
import base64
import pandas as pd
import matplotlib.pyplot as plt 
# numpy é importado em grafico_diretoria.py se necessário

# Importar a função de gráfico do novo local
try:
    # Assumindo que 'dashboards' é uma pasta na raiz do projeto
    from dashboards.grafico_diretoria import gerar_grafico_unidades_por_diretoria 
except ImportError as e:
    st.error(f"Erro ao importar 'gerar_grafico_unidades_por_diretoria': {e}. Verifique se 'dashboards/grafico_diretoria.py' existe.")
    def gerar_grafico_unidades_por_diretoria(*args, **kwargs): # Fallback
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "Erro: Função do gráfico não encontrada.\nVerifique 'dashboards/grafico_diretoria.py'.", ha='center', va='center', color='red', fontsize=12)
        fig.patch.set_facecolor(THEME.get('CHART_BACKGROUND', '#0A192F'))
        ax.set_facecolor(THEME.get('CHART_AXES_FACE', '#102A4C'))
        return fig

# MTI Theme Colors - Enhanced for a "Perfect" Layout
THEME = {
    'PRIMARY': "#00529B",          # MTI Blue (Deep) - For primary actions, borders
    'SECONDARY': "#0078D4",       # MTI Blue (Medium) - For secondary elements, accents
    'ACCENT': "#00A9E0",           # MTI Cyan/Light Blue - For highlights, active states
    'ACCENT_LIGHT': "#71C5E8",     # Lighter Accent - For hover effects, subtle details
    'BACKGROUND': "#071426",       # Even Darker Blue/Slate - Main app background for depth
    'BACKGROUND_ALT': "#0A1E3C",   # Slightly Lighter BG - For cards or layered elements
    'CARD_BG': "#102A4C",            # Dark Blue/Slate for cards - Slightly more contrast
    'INPUT_BG': "#1A3B5C",           # Darker, richer blue for inputs
    'BORDER_LIGHT': "#2A4A6C",       # More visible, but still dark, border
    'BORDER_DARK': "#0A1E3C",        # For subtle definition
    'TEXT_PRIMARY': "#FFFFFF",       # White text - Main text
    'TEXT_SECONDARY': "#E0E6F1",     # Off-white - Secondary text, slightly brighter
    'TEXT_TERTIARY': "#A0AEC0",      # Gray - For less emphasis, placeholders
    'TEXT_ACCENT': "#00A9E0",        # Cyan text for highlights
    'LIGHT_GRAY': "#B0C4DE",         # Lighter Gray for subtle text (LightSteelBlue)
    'SUCCESS': "#28A745",            # Bootstrap Green
    'ERROR': "#DC3545",              # Bootstrap Red
    'WARNING': "#FFC107",            # Bootstrap Yellow/Orange
    'INFO': "#17A2B8",               # Bootstrap Info Blue/Teal
    'ICON_COLOR': "#A0AEC0",
    'SECTION_TITLE_TEXT': "#00A9E0", 
    'CHART_BACKGROUND': "#071426",   # Match app background
    'CHART_AXES_FACE': "#102A4C",    # Match card background for plot area
    'SHADOW_COLOR': "rgba(0, 120, 212, 0.2)", # MTI Blue based shadow
}

# Paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR) 
LOGO_PATH = os.path.join(PROJECT_ROOT, "documentation", "mti.png")
INICIATIVAS_CSV_PATH = os.path.join(PROJECT_ROOT, "data", "iniciativas.csv") 

# Unidades MTI (para exibir nomes completos se necessário)
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
    if not os.path.exists(path): 
        print(f"ALERTA (Dashboards Page): Imagem da logo não encontrada em {path}")
        return ""
    with open(path, "rb") as img_file: return base64.b64encode(img_file.read()).decode("utf-8")

@st.cache_data 
def load_iniciativas_data(file_path):
    try:
        try: df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError: df = pd.read_csv(file_path, encoding='latin1')

        required_cols = ['DIR', 'CONSOLIDADO UNIDADE', 'Nº INICIATIVAS']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            st.error(f"Colunas ausentes no arquivo CSV ('{file_path}'): {', '.join(missing_cols)}.")
            return pd.DataFrame()
        
        df['Nº INICIATIVAS'] = pd.to_numeric(df['Nº INICIATIVAS'], errors='coerce').fillna(0).astype(int)
        df['DIR'] = df['DIR'].astype(str).str.strip().fillna("N/A")
        df['CONSOLIDADO UNIDADE'] = df['CONSOLIDADO UNIDADE'].astype(str).str.strip().fillna("N/A")
        return df
    except FileNotFoundError:
        st.error(f"Arquivo de dados '{file_path}' não encontrado. Certifique-se que ele existe em 'data/iniciativas.csv'.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao carregar ou processar o arquivo de dados '{file_path}': {e}")
        return pd.DataFrame()

# --- Main Dashboards Page Function ---
def dashboards_page():
    st.set_page_config(page_title="Dashboards - MTI Assistente", layout="wide", page_icon="📊")

    if "dash_filter_diretoria" not in st.session_state: 
        st.session_state.dash_filter_diretoria = "Todas as Diretorias" 

    st.markdown(f"""
    <style>
        /* Base styles */
        body, .stApp {{ 
            background-color: {THEME['BACKGROUND']}; 
            color: {THEME['TEXT_SECONDARY']}; 
            font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif; 
        }}
        .main .block-container {{ padding: 2.5rem 3.5rem; max-width: 1800px; margin: 0 auto; }} /* Wider for dashboards */
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] > div:first-child {{
            background-color: {THEME['BACKGROUND_ALT']}; /* Slightly different sidebar bg */
            padding: 2rem 1.5rem;
            border-right: 1px solid {THEME['BORDER_DARK']};
        }}
        .sidebar-logo-container {{ text-align: center; margin-bottom: 2.5rem; }}
        .sidebar-logo-container img {{
            max-width: 150px; /* Larger sidebar logo */
            border-radius: 12px;
            box-shadow: 0 6px 18px rgba(0,0,0,0.25);
            transition: transform 0.3s ease-in-out, filter 0.3s ease;
            filter: brightness(1);
        }}
        .sidebar-logo-container img:hover {{ transform: scale(1.08); filter: brightness(1.1); }}

        .dashboard-sidebar-user-card {{ 
            padding: 1.3rem 1.1rem; background-color: {THEME['CARD_BG']};
            border-radius: 16px; margin-bottom: 2rem;
            border: 1px solid {THEME['BORDER_LIGHT']}; text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}
        .dashboard-sidebar-user-card .user-name {{
            color: {THEME['TEXT_PRIMARY']}; font-weight: 600; font-size: 1.15rem; margin-bottom: 0.4rem;
        }}
        .dashboard-sidebar-user-card .user-role {{ 
            color: {THEME['ACCENT_LIGHT']}; font-size: 0.95rem; font-weight: 500;
        }}
        .dashboard-sidebar-button button {{
            background-image: linear-gradient(120deg, {THEME['PRIMARY']} 0%, {THEME['SECONDARY']} 100%) !important;
            color: {THEME['TEXT_PRIMARY']} !important; font-weight: 600 !important;
            border-radius: 12px !important; padding: 0.9rem 0 !important;
            transition: all 0.3s ease !important; width: 100%; 
            box-shadow: 0 4px 10px {THEME['PRIMARY']}55;
            letter-spacing: 0.5px;
        }}
        .dashboard-sidebar-button button:hover {{
             background-image: linear-gradient(120deg, {THEME['SECONDARY']} 0%, {THEME['ACCENT']} 100%) !important;
             transform: translateY(-3px) scale(1.02); box-shadow: 0 6px 15px {THEME['SECONDARY']}77;
        }}

        /* Dashboard Page Specific Content Styling */
        .dashboard-header {{ margin-bottom: 3rem; }}
        .dashboard-header h1 {{
            color: {THEME['TEXT_PRIMARY']}; font-size: 3rem; font-weight: 700;
            margin-bottom: 0.6rem; letter-spacing: -1.2px;
            text-shadow: 0 3px 6px {THEME['BACKGROUND_ALT']};
        }}
        .dashboard-header .subtitle {{
            color: {THEME['LIGHT_GRAY']}; font-size: 1.2rem;
            line-height: 1.65; max-width: 900px;
        }}
        
        /* Styling for st.tabs */
        div[data-baseweb="tab-list"] {{
            background-color: {THEME['BACKGROUND_ALT']}; border-radius: 14px; /* More rounded */
            padding: 0.6rem; margin-bottom: 3rem; 
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            border: 1px solid {THEME['BORDER_DARK']};
        }}
        button[data-baseweb="tab"] {{
            background-color: transparent !important; color: {THEME['TEXT_TERTIARY']} !important;
            font-family: 'Inter', 'Segoe UI', sans-serif; font-weight: 600; /* Bolder tab text */
            font-size: 1.15rem; 
            border-radius: 10px !important; 
            padding: 1rem 2rem !important; 
            margin: 0 0.5rem;
            transition: all 0.3s ease-in-out;
            border: none !important; /* Remove default borders */
        }}
        button[data-baseweb="tab"]:hover {{
            background-color: {THEME['INPUT_BG']}99 !important;
            color: {THEME['TEXT_PRIMARY']} !important;
        }}
        button[data-baseweb="tab"][aria-selected="true"] {{
            background-image: linear-gradient(120deg, {THEME['ACCENT']} 0%, {THEME['SECONDARY']} 100%) !important;
            color: {THEME['TEXT_PRIMARY']} !important;
            box-shadow: 0 5px 12px {THEME['ACCENT']}77;
        }}
        .dashboard-content-card h3 {{
             color: {THEME['ACCENT_LIGHT']}; font-size: 2rem; font-weight: 600;
            margin-bottom: 2.5rem; 
            border-bottom: 1.5px solid {THEME['BORDER_LIGHT']}88;
            padding-bottom: 1rem;
            letter-spacing: -0.3px;
        }}
        .stSelectbox > label {{ 
            color: {THEME['LIGHT_GRAY']} !important; font-weight: 500 !important; 
            font-size: 1.15rem !important; margin-bottom: 0.6rem !important;
        }}
         .stSelectbox > div > div {{ /* The selectbox itself */
            background-color: {THEME['INPUT_BG']} !important;
            border: 1.5px solid {THEME['BORDER_LIGHT']} !important;
            border-radius: 10px !important;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
        }}
        .stSelectbox > div > div:hover {{ border-color: {THEME['ACCENT']} !important; }}

        .filter-info-text {{
            color: {THEME['ACCENT']}; font-style: normal; font-weight: 500;
            font-size: 1.05rem; margin-top: 0.8rem; margin-bottom: 2.5rem; 
            padding: 0.8rem 1.2rem; background-color: {THEME['BACKGROUND_ALT']}; 
            border-radius: 10px; border-left: 5px solid {THEME['ACCENT']};
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        /* KPI Card Styling */
        .kpi-card-container {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem; margin-bottom: 2rem; }}
        .kpi-card {{
            background-color: {THEME['BACKGROUND_ALT']};
            padding: 1.8rem;
            border-radius: 16px;
            border: 1px solid {THEME['BORDER_LIGHT']};
            box-shadow: 0 6px 15px -5px rgba(0,0,0,0.2);
            text-align: center;
            transition: transform 0.25s ease, box-shadow 0.25s ease;
        }}
        .kpi-card:hover {{ transform: translateY(-5px); box-shadow: 0 10px 20px -5px {THEME['ACCENT']}44; }}
        .kpi-card .stMetric {{ border-bottom: none !important; padding-bottom: 0 !important; }} /* Remove default Streamlit metric border */
        .kpi-card .stMetric > label {{ /* Metric Label */
            color: {THEME['TEXT_TERTIARY']} !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            margin-bottom: 0.5rem !important;
        }}
        .kpi-card .stMetric > div:nth-of-type(2) > div {{ /* Metric Value */
            color: {THEME['TEXT_PRIMARY']} !important;
            font-size: 2.8rem !important;
            font-weight: 700 !important;
            line-height: 1.1 !important;
        }}
        .kpi-card .stMetric > div:nth-of-type(3) > div {{ /* Metric Delta */
            font-size: 0.95rem !important;
            font-weight: 500 !important;
            padding: 0.2rem 0.5rem;
            border-radius: 6px;
            margin-top: 0.6rem;
        }}
        /* Positive delta */
        .kpi-card .stMetric > div:nth-of-type(3) > div[data-delta-direction="positive"] {{
            color: {THEME['SUCCESS']} !important;
            background-color: {THEME['SUCCESS']}22;
        }}
        /* Negative delta */
        .kpi-card .stMetric > div:nth-of-type(3) > div[data-delta-direction="negative"] {{
            color: {THEME['ERROR']} !important;
            background-color: {THEME['ERROR']}22;
        }}


    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown('<div class="sidebar-logo-container">', unsafe_allow_html=True)
        logo_b64_sidebar = get_image_base64(LOGO_PATH)
        if logo_b64_sidebar: st.image(f"data:image/png;base64,{logo_b64_sidebar}", width=140)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.session_state.get("authenticated", False):
            st.markdown(f"""<div class="dashboard-sidebar-user-card">
                <div class="user-name">{st.session_state.get("user_full_name", "Usuário")}</div>
                <div class="user-role">Status: Conectado</div>
            </div>""", unsafe_allow_html=True)
        else: 
            st.markdown(f"""<div class="dashboard-sidebar-user-card">
                <div class="user-name">Visitante</div>
                <div class="user-role">Visualizando Dashboards</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("<hr style='margin: 1.5rem 0; border-color: " + THEME['BORDER_LIGHT'] + "44;'>", unsafe_allow_html=True)
        st.markdown('<div class="dashboard-sidebar-button">', unsafe_allow_html=True)
        if st.button("⬅️ Voltar para o Chat", use_container_width=True, key="dashboard_back_to_chat_v3"):
            st.switch_page("ChatBot.py") 
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div class='dashboard-header'><h1>📊 Painel de Dashboards</h1><p class='subtitle'>Visualize dados e insights estratégicos da MTI.</p></div>", unsafe_allow_html=True)
    
    df_iniciativas_completo = load_iniciativas_data(INICIATIVAS_CSV_PATH)

    tab_iniciativas, tab_indicadores = st.tabs(["📊  Iniciativas Estratégicas", "📈  Indicadores de Desempenho"])

    with tab_iniciativas:
        st.markdown('<div class="dashboard-content-card">', unsafe_allow_html=True)
        st.markdown("<h3>Iniciativas por Unidade (Filtrado por Diretoria)</h3>", unsafe_allow_html=True)
        
        if df_iniciativas_completo.empty:
            st.warning("Não foi possível carregar os dados das iniciativas. Verifique o arquivo 'data/iniciativas.csv'.")
        else:
            if 'DIR' in df_iniciativas_completo.columns:
                diretorias_disponiveis = ["Todas as Diretorias"] + sorted(list(df_iniciativas_completo['DIR'].unique()))
            else:
                st.error("Coluna 'DIR' (Diretoria) não encontrada nos dados. Não é possível criar o filtro.")
                diretorias_disponiveis = ["Todas as Diretorias"] 

            try:
                current_filter_index_dir = diretorias_disponiveis.index(st.session_state.dash_filter_diretoria)
            except ValueError: 
                current_filter_index_dir = 0 
                st.session_state.dash_filter_diretoria = diretorias_disponiveis[0]

            diretoria_selecionada_filtro = st.selectbox(
                "Selecione a Diretoria para visualizar o detalhamento por Unidade:",
                options=diretorias_disponiveis,
                index=current_filter_index_dir,
                key="dash_filter_diretoria_selectbox_v3" 
            )
            st.session_state.dash_filter_diretoria = diretoria_selecionada_filtro
            
            if st.session_state.dash_filter_diretoria != "Todas as Diretorias":
                st.markdown(f"<div class='filter-info-text'>Exibindo unidades da Diretoria: <strong>{st.session_state.dash_filter_diretoria}</strong></div>", unsafe_allow_html=True)
                
                if 'DIR' in df_iniciativas_completo.columns and \
                   'CONSOLIDADO UNIDADE' in df_iniciativas_completo.columns and \
                   'Nº INICIATIVAS' in df_iniciativas_completo.columns:
                    
                    fig_iniciativas = gerar_grafico_unidades_por_diretoria(
                        df_iniciativas_completo, 
                        diretoria_selecionada=st.session_state.dash_filter_diretoria,
                        coluna_diretoria_principal="DIR", 
                        coluna_unidade="CONSOLIDADO UNIDADE",
                        coluna_iniciativas="Nº INICIATIVAS",
                        theme_colors=THEME 
                    )
                    st.pyplot(fig_iniciativas, use_container_width=True)
                else:
                    st.error("Não foi possível gerar o gráfico. Verifique se as colunas 'DIR', 'CONSOLIDADO UNIDADE' e 'Nº INICIATIVAS' existem no seu arquivo CSV.")
            else:
                st.info("ℹ️ Selecione uma Diretoria específica para visualizar o detalhamento de iniciativas por unidade e o total da diretoria.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_indicadores:
        st.markdown('<div class="dashboard-content-card">', unsafe_allow_html=True)
        st.markdown("<h3>Acompanhamento de Indicadores Chave</h3>", unsafe_allow_html=True)
        
        # KPI Cards Example
        kpi_cols = st.columns(3)
        with kpi_cols[0]:
            st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
            st.metric(label="Projetos Concluídos (Ano)", value="128", delta="12%")
            st.markdown('</div>', unsafe_allow_html=True)
        with kpi_cols[1]:
            st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
            st.metric(label="Satisfação do Cliente (CSAT)", value="4.7/5", delta="0.2")
            st.markdown('</div>', unsafe_allow_html=True)
        with kpi_cols[2]:
            st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
            st.metric(label="Eficiência Operacional", value="93%", delta="-1.5%")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.info("🚧 Mais gráficos e visualizações de indicadores serão adicionados aqui em breve. 🚧")
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    if 'authenticated' not in st.session_state: 
        st.session_state.authenticated = True 
    if 'user_full_name' not in st.session_state:
        st.session_state.user_full_name = "Usuário Teste" 
    if 'dash_filter_diretoria' not in st.session_state: 
        st.session_state.dash_filter_diretoria = "Todas as Diretorias"
    
    dashboards_page()
