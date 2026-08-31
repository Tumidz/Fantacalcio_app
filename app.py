import streamlit as st

# 1. Configurazione della pagina
st.set_page_config(
    page_title="FantaIA v0.0.5",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Immagini usate per il layout (Stadio e Martello 3D)
URL_SFONDO_STADIO = "https://images.unsplash.com/photo-1489944440615-453fc2b6a9a9?q=80&w=2000&auto=format&fit=crop"
URL_MARTELLO_ASTA = "https://cdn3d.iconscout.com/3d/premium/thumb/auction-gavel-4721151-3927976.png"

# 2. CSS Avanzato v0.0.5 (Fix per i bottoni in stile "App")
custom_css = f"""
<style>
    /* Sfondo Stadio Scurito */
    .stApp {{
        background-image: linear-gradient(rgba(15, 23, 30, 0.88), rgba(15, 23, 30, 0.95)),
                          url("{URL_SFONDO_STADIO}");
        background-size: cover;
        background-attachment: fixed;
        color: #f0f4f8;
    }}

    /* Nasconde la linea grigia di default sotto i tab di Streamlit */
    div[data-baseweb="tab-list"] {{
        justify-content: center !important;
        gap: 15px !important;
        border-bottom: none !important; 
        margin-bottom: 30px !important;
    }}

    /* Stile per i bottoni non selezionati (Bordo grigio/verde) */
    button[data-baseweb="tab"] {{
        background-color: rgba(22, 34, 47, 0.6) !important;
        border: 2px solid #3a4f41 !important; 
        border-radius: 12px !important;
        padding: 10px 20px !important;
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        transition: all 0.3s ease;
    }}

    /* Stile per il bottone SELEZIONATO (Bordo verde fluo e ombra) */
    button[data-baseweb="tab"][aria-selected="true"] {{
        border-color: #52b788 !important;
        box-shadow: 0 0 15px rgba(82, 183, 136, 0.4) !important;
        color: #52b788 !important;
        background-color: rgba(82, 183, 136, 0.1) !important;
    }}

    /* Rimuove i bordi blu di default quando clicchi */
    button[data-baseweb="tab"]:focus {{
        outline: none !important;
    }}

    /* Grandezza del testo e delle icone nei bottoni */
    button[data-baseweb="tab"] p {{
        font-size: 1.1rem !important;
        margin: 0 !important;
    }}

    /* Header e Testi Centrati */
    .center-text {{
        text-align: center;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. Navigazione a Schede (con le immaginine/emoji reinserite)
tab_home, tab_asta, tab_formazione, tab_scambi = st.tabs([
    "🏠 Home", 
    "🔨 Asta", 
    "📋 Formazione", 
    "🔄 Scambi"
])

# CONTENUTO DELLE SCHEDE
with tab_home:
    st.markdown("<h2 class='center-text'>🏠 Home</h2>", unsafe_allow_html=True)
    st.markdown("<p class='center-text' style='color:#cbd5e0;'>Benvenuto nel tuo Centro Comando IA per il Fantacalcio.</p>", unsafe_allow_html=True)

with tab_asta:
    # Ricreiamo esattamente la schermata dell'immagine generata
    st.markdown("<h2 class='center-text'>🔨 Area Asta Live</h2>", unsafe_allow_html=True)
    st.markdown("<p class='center-text' style='color:#cbd5e0; font-size:1.1rem; margin-bottom: 40px;'>Gestisci i tuoi crediti e segui i rilanci dell'IA.</p>", unsafe_allow_html=True)
    
    # Impaginazione per centrare perfettamente l'immagine del martello
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.image(URL_MARTELLO_ASTA, use_container_width=True)
        st.markdown("<p class='center-text' style='color:#8c9bab; font-size:0.9rem;'>Martello ufficiale dell'Asta FantaIA</p>", unsafe_allow_html=True)

with tab_formazione:
    st.markdown("<h2 class='center-text'>📋 Formazione</h2>", unsafe_allow_html=True)
    st.markdown("<p class='center-text' style='color:#cbd5e0;'>L'Assistente Schieramento arriverà qui.</p>", unsafe_allow_html=True)

with tab_scambi:
    st.markdown("<h2 class='center-text'>🔄 Scambi</h2>", unsafe_allow_html=True)
    st.markdown("<p class='center-text' style='color:#cbd5e0;'>Il radar per valutare le trade arriverà qui.</p>", unsafe_allow_html=True)
