import streamlit as st

# 1. Configurazione della pagina
st.set_page_config(
    page_title="FantaIA v0.0.2",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Iniezione CSS per tema personalizzato "Campo da Gioco / Dark Sport UI"
custom_css = """
<style>
    /* Sfondo principale e colore testo */
    .stApp {
        background-color: #0b1319;
        color: #f0f4f8;
    }

    /* Stile per l'intestazione e badge versione */
    .header-container {
        background: linear-gradient(135deg, #1b4332 0%, #081c15 100%);
        border: 1px solid #2d6a4f;
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }
    
    .version-badge {
        background-color: #52b788;
        color: #081c15;
        font-weight: bold;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        display: inline-block;
        margin-top: 6px;
    }

    /* Stile per le schede (Tabs) touch-friendly per smartphone */
    div[data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #16222f;
        padding: 8px;
        border-radius: 12px;
    }

    div[data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        color: #a0aec0;
        font-weight: 600;
        padding: 10px 14px;
        border: none !important;
    }

    div[aria-selected="true"] {
        background-color: #2d6a4f !important;
        color: #ffffff !important;
    }

    /* Card grafiche personalizzate */
    .fanta-card {
        background: #16222f;
        border: 1px solid #243447;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 15px;
    }

    .fanta-card-title {
        color: #52b788;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 8px;
    }

    /* Bottoni touch potenziati */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #2d6a4f 0%, #40916c 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 12px 20px;
        border-radius: 10px;
        font-size: 1rem;
        transition: all 0.2s ease-in-out;
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #40916c 0%, #52b788 100%);
        color: #081c15;
        transform: translateY(-1px);
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. Header grafico v0.0.2
st.markdown("""
<div class="header-container">
    <h1 style="margin:0; font-size:2rem; color:#ffffff;">⚽ FantaIA Assistant</h1>
    <span class="version-badge">Versione 0.0.2 - Design Update</span>
</div>
""", unsafe_allow_html=True)

# 4. Navigazione a Schede (Tabs)
tab_home, tab_asta, tab_formazione, tab_scambi = st.tabs([
    "🏠 Home", 
    "🔨 Asta", 
    "📋 Formazione", 
    "🔄 Scambi"
])

with tab_home:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">👋 Benvenuto nel tuo Centro Comando</div>
        <p style="color:#cbd5e0; margin-bottom:0;">
            La grafica è stata ottimizzata per dispositivi mobili. Le schede in alto permettono di navigare facilmente anche con il pollice da smartphone.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Crediti Residui (Simulazione)", value="500 / 500")
    with col2:
        st.metric(label="Stato Rosa", value="0 / 25 Giocatori")

    st.subheader("🚀 Prossimo Passo")
    st.info("Siamo pronti per la **v0.1.0**: implementeremo la gestione reale dei crediti e delle rose degli avversari per l'Asta!")

with tab_asta:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">🔨 Modulo Asta in Evidenza</div>
        <p style="color:#cbd5e0;">Interfaccia predisposta per l'immissione rapida dei rilanci durante l'asta live.</p>
    </div>
    """, unsafe_allow_html=True)
    st.button("⚡ Test Bottone Asta Touch")

with tab_formazione:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">📋 Assistente Schieramento</div>
        <p style="color:#cbd5e0;">Grafica predisposta per il campo tattico e le percentuali di titolarità dell'IA.</p>
    </div>
    """, unsafe_allow_html=True)

with tab_scambi:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">🔄 Radar Scambi</div>
        <p style="color:#cbd5e0;">Predisposizione per il confronto a due o tre giocatori tra rose.</p>
    </div>
    """, unsafe_allow_html=True)
