import streamlit as st

# 1. Configurazione della pagina per v0.0.4
st.set_page_config(
    page_title="FantaIA v0.0.4",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Simulazione URL immagini (usiamo placeholder per l'esempio)
# Nella realtà useresti gli URL diretti delle tue immagini hostate o file locali.
URL_SFONDO_STADIO = "https://static.vecteezy.com/system/resources/thumbnails/074/239/120/small/an-impressive-modern-and-empty-football-stadium-with-blue-and-multicolored-seats-under-a-large-roof-structure-photo.jpg" # image_0.png
URL_MARTELLO_ASTA = "https://static.vecteezy.com/system/resources/thumbnails/073/792/853/small_2x/3d-wooden-judge-gavel-on-transparent-background-legal-justice-court-law-auction-verdict-decision-ruling-judgment-authority-concept-icon-png.png" # image_2.png

# 2. CSS Avanzato v0.0.4 (Sfondo, Pulsanti centrati e bordati)
custom_css = f"""
<style>
    /* Sfondo principale con Immagine Stadio e Overlay scuro */
    .stApp {{
        background-image: linear-gradient(rgba(11, 19, 25, 0.85), rgba(11, 19, 25, 0.95)),
                          url("{URL_SFONDO_STADIO}");
        background-size: cover;
        background-attachment: fixed;
        color: #f0f4f8;
    }}

    /* Header elegante e centrato (come v0.0.3) */
    .header-container {{
        background: linear-gradient(135deg, #1b4332 0%, #081c15 100%);
        border: 2px solid #2d6a4f;
        padding: 16px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }}
    
    .version-badge {{
        background-color: #52b788;
        color: #081c15;
        font-weight: bold;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.8rem;
        display: inline-block;
        margin-top: 4px;
    }}

    /* --- Nuova Gestione Pulsanti Navigazione (Tabs) --- */
    /* Contenitore principale delle schede */
    div[data-baseweb="tab-list"] {{
        justify-content: center !important; /* Centra la lista */
        background-color: transparent !important; /* Rimuove sfondo bar */
        border: none !important;
        gap: 10px; /* Spazio tra i pulsanti */
        margin-bottom: 20px;
    }}

    /* Stile per ogni singolo Tab (ora sembrano Pulsanti) */
    div[data-baseweb="tab"] {{
        background-color: #16222f !important;
        border: 2px solid #2d6a4f !important; /* Bordo visibile */
        border-radius: 12px !important;
        color: #a0aec0 !important;
        font-weight: 700 !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease-in-out;
        min-width: 100px; /* Larghezza minima per simmetria */
        text-align: center;
    }}

    /* Testo all'interno dei Tabs */
    div[data-baseweb="tab"] p {{
        font-size: 1rem !important;
        margin: 0 !important;
    }}

    /* Stato Selezionato (Pulsante attivo) */
    div[aria-selected="true"] {{
        background-color: #2d6a4f !important;
        color: #ffffff !important;
        border-color: #52b788 !important;
        box-shadow: 0 0 10px rgba(82, 183, 136, 0.5);
    }}

    /* Hover (quando passi sopra col mouse o tocchi) */
    div[data-baseweb="tab"]:hover {{
        border-color: #52b788 !important;
        transform: translateY(-2px);
    }}

    /* --- Altri stili confermati --- */
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

    .fanta-card {{
        background: rgba(22, 34, 47, 0.8); /* Leggermente trasparente */
        border: 1px solid #243447;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 15px;
        backdrop-filter: blur(2px); /* Effetto sfocato sullo sfondo */
    }}

    .fanta-card-title {{
        color: #52b788;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 8px;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. Header
st.markdown(f"""
<div class="header-container">
    <h1 style="margin:0; font-size:1.8rem; color:#ffffff;">⚽ FantaIA Assistant</h1>
    <span class="version-badge">v0.0.4 - Stadium & Gavel Update</span>
</div>
""", unsafe_allow_html=True)

# 4. Navigazione a Schede (Tabs - ora stilizzati come pulsanti)
# Rimuoviamo gli emoji dai titoli dei tab per pulizia, 
# la stilizzazione a pulsante è sufficiente.
tab_home, tab_asta, tab_formazione, tab_scambi = st.tabs([
    "Home", 
    "Asta", 
    "Formazione", 
    "Scambi"
])

with tab_home:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">🏟️ Benvenuto nello Stadio FantaIA</div>
        <p style="color:#cbd5e0; font-size:0.9rem;">
            Guarda lo sfondo! Ora sei immerso nell'atmosfera del giorno della partita.
            I pulsanti di navigazione in alto sono stati centrati e resi più evidenti.
        </p>
    </div>
    """, unsafe_allow_html=True)

with tab_asta:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">🔨 Area Asta Live</div>
        <p style="color:#cbd5e0; font-size:0.9rem;">Gestisci i tuoi crediti e segui i rilanci dell'IA.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inserimento Immagine Reale del Martello dell'Asta
    st.image(URL_MARTELLO_ASTA, width=120)
    st.caption("Martello ufficiale dell'Asta FantaIA")

    st.markdown("""
    <div class="fanta-card" style="border-left: 4px solid #c0392b; margin-top:15px;">
        <span class="role-badge badge-a">A</span> <b>Simulazione Giocatore</b><br/>
        <small style="color:#a0aec0;">Prezzo Massimo Consigliato: 80 / 500 FM</small>
    </div>
    """, unsafe_allow_html=True)

with tab_formazione:
    st.markdown('<div class="fanta-card-title">📋 Assistente Schieramento (Anteprima Campo)</div>', unsafe_allow_html=True)
    st.write("Il campo tattico è confermato qui (come in v0.0.3).")

with tab_scambi:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">🔄 Area Confronto Scambi</div>
        <p style="color:#cbd5e0; font-size:0.9rem;">Sezione pronta per l'algoritmo.</p>
    </div>
    """, unsafe_allow_html=True)
