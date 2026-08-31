import streamlit as st

# 1. Configurazione della pagina
st.set_page_config(
    page_title="FantaIA Assistant",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Immagini per lo sfondo stadio e il martello dell'asta
URL_SFONDO_STADIO = "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?q=80&w=1920&auto=format&fit=crop"
URL_MARTELLO_ASTA = "https://cdn3d.iconscout.com/3d/premium/thumb/auction-gavel-4721151-3927976.png"

# 2. CSS Avanzato (Ricostruzione esatta dell'immagine concettuale)
custom_css = f"""
<style>
    /* Sfondo Stadio Scurito Elegante */
    .stApp {{
        background-image: linear-gradient(rgba(10, 17, 24, 0.88), rgba(10, 17, 24, 0.94)),
                          url("{URL_SFONDO_STADIO}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #f0f4f8;
    }}

    /* --- STILE PULSANTI DI NAVIGAZIONE (TABS) --- */
    /* Centra la barra dei pulsanti */
    div[data-baseweb="tab-list"] {{
        justify-content: center !important;
        gap: 12px !important;
        border-bottom: none !important;
        background-color: transparent !important;
        padding-top: 10px !important;
        padding-bottom: 5px !important;
    }}

    /* Rimuove le linee e gli indicatori predefiniti di Streamlit */
    div[data-baseweb="tab-highlight"], 
    div[data-baseweb="tab-border"] {{
        display: none !important;
    }}

    /* Singolo Pulsante Rettangolare (Stato Non Selezionato) */
    button[data-baseweb="tab"] {{
        background-color: rgba(20, 32, 44, 0.75) !important;
        border: 1.5px solid #3d5a45 !important;
        border-radius: 10px !important;
        padding: 8px 18px !important;
        transition: all 0.25s ease-in-out !important;
        margin: 0 !important;
    }}

    /* Testo e Icona dentro il Pulsante */
    button[data-baseweb="tab"] p {{
        color: #d1d5db !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin: 0 !important;
    }}

    /* Hover quando si passa sopra col mouse o si tocca */
    button[data-baseweb="tab"]:hover {{
        border-color: #52b788 !important;
        background-color: rgba(30, 46, 60, 0.85) !important;
    }}

    /* Pulsante SELEZIONATO (Contorno Verde Luminoso) */
    button[data-baseweb="tab"][aria-selected="true"] {{
        background-color: rgba(18, 32, 42, 0.9) !important;
        border: 2px solid #52b788 !important;
        box-shadow: 0 0 14px rgba(82, 183, 136, 0.5) !important;
    }}

    button[data-baseweb="tab"][aria-selected="true"] p {{
        color: #52b788 !important;
        font-weight: 700 !important;
    }}

    /* Separatore sottile sotto i pulsanti */
    .tab-divider {{
        border-bottom: 1px solid rgba(255, 255, 255, 0.12);
        margin-top: 5px;
        margin-bottom: 25px;
    }}

    /* Elementi grafici per l'Area Asta */
    .asta-title {{
        text-align: center;
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        margin-top: 10px;
        margin-bottom: 8px;
    }}

    .asta-subtitle {{
        text-align: center;
        color: #cbd5e0;
        font-size: 1.05rem;
        margin-bottom: 30px;
    }}

    .asta-caption {{
        text-align: center;
        color: #94a3b8;
        font-size: 0.9rem;
        margin-top: 15px;
    }}

    /* Badge Ruoli Fantacalcio (v0.0.4) */
    .role-badge {{
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 800;
        font-size: 0.85rem;
        color: #ffffff;
        display: inline-block;
        margin-right: 5px;
    }}
    .badge-p {{ background-color: #e67e22; }}
    .badge-d {{ background-color: #27ae60; }}
    .badge-c {{ background-color: #2980b9; }}
    .badge-a {{ background-color: #c0392b; }}

    /* Card generali */
    .fanta-card {{
        background: rgba(22, 34, 47, 0.85);
        border: 1px solid #243447;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 15px;
        backdrop-filter: blur(4px);
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. Navigazione a Pulsanti con Icone
tab_home, tab_asta, tab_formazione, tab_scambi = st.tabs([
    "🏠 Home", 
    "🔨 Asta", 
    "📋 Formazione", 
    "🔄 Scambi"
])

# 4. Contenuto delle Schede
with tab_home:
    st.markdown('<div class="tab-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="fanta-card">
        <div style="color:#52b788; font-size:1.1rem; font-weight:700; margin-bottom:8px;">🏠 Centro Comando</div>
        <p style="color:#cbd5e0; margin:0;">Interfaccia base v0.0.5 pronta per i moduli IA.</p>
    </div>
    """, unsafe_allow_html=True)

with tab_asta:
    st.markdown('<div class="tab-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="asta-title">🔨 Area Asta Live</div>', unsafe_allow_html=True)
    st.markdown('<div class="asta-subtitle">Gestisci i tuoi crediti e segui i rilanci dell\'IA.</div>', unsafe_allow_html=True)
    
    # Martello 3D centrato
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.image(URL_MARTELLO_ASTA, use_container_width=True)
    
    st.markdown('<div class="asta-caption">Martello ufficiale dell\'Asta FantaIA</div>', unsafe_allow_html=True)

with tab_formazione:
    st.markdown('<div class="tab-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="fanta-card">
        <div style="color:#52b788; font-size:1.1rem; font-weight:700; margin-bottom:8px;">📋 Assistente Schieramento</div>
        <p style="color:#cbd5e0; margin:0;">In arrivo nella v0.2.0</p>
    </div>
    """, unsafe_allow_html=True)

with tab_scambi:
    st.markdown('<div class="tab-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="fanta-card">
        <div style="color:#52b788; font-size:1.1rem; font-weight:700; margin-bottom:8px;">🔄 Radar Scambi</div>
        <p style="color:#cbd5e0; margin:0;">In arrivo nella v0.3.0</p>
    </div>
    """, unsafe_allow_html=True)
