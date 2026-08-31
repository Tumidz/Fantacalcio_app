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

# 2. CSS Avanzato (Unione Grafica v0.0.3 + v0.0.4)
custom_css = f"""
<style>
    /* Sfondo Stadio Vista Interna con Overlay Scuro */
    .stApp {{
        background-image: linear-gradient(rgba(10, 17, 24, 0.88), rgba(10, 17, 24, 0.94)),
                          url("{URL_SFONDO_STADIO}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #f0f4f8;
    }}

    /* Intestazione principale (Da v0.0.3) */
    .header-container {{
        background: linear-gradient(135deg, #1b4332 0%, #081c15 100%);
        border: 2px solid #2d6a4f;
        padding: 16px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
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

    /* --- PULSANTI DI NAVIGAZIONE CON BORDO (Da v0.0.4) --- */
    div[data-baseweb="tab-list"] {{
        justify-content: center !important;
        gap: 10px !important;
        border-bottom: none !important;
        background-color: transparent !important;
        padding-bottom: 10px !important;
    }}

    div[data-baseweb="tab-highlight"], 
    div[data-baseweb="tab-border"] {{
        display: none !important;
    }}

    /* Singolo Pulsante Rettangolare */
    button[data-baseweb="tab"] {{
        background-color: rgba(20, 32, 44, 0.8) !important;
        border: 1.5px solid #3d5a45 !important;
        border-radius: 10px !important;
        padding: 8px 16px !important;
        transition: all 0.25s ease-in-out !important;
    }}

    button[data-baseweb="tab"] p {{
        color: #d1d5db !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        margin: 0 !important;
    }}

    button[data-baseweb="tab"]:hover {{
        border-color: #52b788 !important;
        background-color: rgba(30, 46, 60, 0.9) !important;
    }}

    /* Pulsante Selezionato (Contorno Verde Luminoso) */
    button[data-baseweb="tab"][aria-selected="true"] {{
        background-color: rgba(18, 32, 42, 0.95) !important;
        border: 2px solid #52b788 !important;
        box-shadow: 0 0 12px rgba(82, 183, 136, 0.5) !important;
    }}

    button[data-baseweb="tab"][aria-selected="true"] p {{
        color: #52b788 !important;
        font-weight: 700 !important;
    }}

    /* --- BADGE RUOLI FANTACALCIO (Da v0.0.3) --- */
    .role-badge {{
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 800;
        font-size: 0.85rem;
        color: #ffffff;
        display: inline-block;
        margin-right: 5px;
    }}
    .badge-p {{ background-color: #e67e22; }} /* Portiere */
    .badge-d {{ background-color: #27ae60; }} /* Difensore */
    .badge-c {{ background-color: #2980b9; }} /* Centrocampista */
    .badge-a {{ background-color: #c0392b; }} /* Attaccante */

    /* Card generali */
    .fanta-card {{
        background: rgba(22, 34, 47, 0.85);
        border: 1px solid #243447;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 15px;
        backdrop-filter: blur(4px);
    }}

    .fanta-card-title {{
        color: #52b788;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 8px;
    }}

    /* --- CAMPO TATTICO VERDE (Da v0.0.3) --- */
    .pitch-container {{
        background: linear-gradient(180deg, #1e5631 0%, #143d21 100%);
        border: 2px solid #52b788;
        border-radius: 14px;
        padding: 20px 10px;
        text-align: center;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.6);
        margin-top: 10px;
    }}

    .pitch-row {{
        display: flex;
        justify-content: space-around;
        margin: 12px 0;
    }}

    .player-slot {{
        background: rgba(11, 19, 25, 0.85);
        border: 1px solid #52b788;
        border-radius: 8px;
        padding: 6px 10px;
        font-size: 0.75rem;
        font-weight: 600;
        color: #ffffff;
        min-width: 65px;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. Header Visivo
st.markdown("""
<div class="header-container">
    <h1 style="margin:0; font-size:1.8rem; color:#ffffff;">⚽ FantaIA Assistant</h1>
    <span class="version-badge">v0.0.4 - Full Edition</span>
</div>
""", unsafe_allow_html=True)

# 4. Navigazione a Schede (Icone + Bordi)
tab_home, tab_asta, tab_formazione, tab_scambi = st.tabs([
    "🏠 Home", 
    "🔨 Asta", 
    "📋 Formazione", 
    "🔄 Scambi"
])

# --- CONTENUTO SCHEDE (Tutto il contenuto di v0.0.3) ---

with tab_home:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">🎨 Ruoli & Codici Colore Fantacalcio</div>
        <p style="color:#cbd5e0; font-size:0.9rem;">
            Codifica visiva ufficiale per i calciatori:
        </p>
        <div style="margin-top:10px;">
            <span class="role-badge badge-p">P</span> Portieri<br/><br/>
            <span class="role-badge badge-d">D</span> Difensori<br/><br/>
            <span class="role-badge badge-c">C</span> Centrocampisti<br/><br/>
            <span class="role-badge badge-a">A</span> Attaccanti
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Crediti Spesi", value="0 FM")
    with col2:
        st.metric(label="Crediti Rimanenti", value="500 FM")

with tab_asta:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">🔨 Interfaccia Asta Live</div>
        <p style="color:#cbd5e0; font-size:0.9rem;">Area rilanci rapidi e gestione budget.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Martello dell'Asta in Evidenza (Da v0.0.4)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.image(URL_MARTELLO_ASTA, use_container_width=True)
    
    st.markdown("""
    <div class="fanta-card" style="border-left: 4px solid #c0392b; margin-top:15px;">
        <span class="role-badge badge-a">A</span> <b>Lautaro Martinez</b> (Inter)<br/>
        <small style="color:#a0aec0;">Prezzo Max Consigliato IA: 140 / 500 FM</small>
    </div>
    """, unsafe_allow_html=True)

with tab_formazione:
    st.markdown('<div class="fanta-card-title">📋 Campo Tattico 3-4-3</div>', unsafe_allow_html=True)
    
    # Campo Verde Tattico (Da v0.0.3)
    st.markdown("""
    <div class="pitch-container">
        <div class="pitch-row">
            <div class="player-slot"><span class="role-badge badge-a">A</span> ATT</div>
            <div class="player-slot"><span class="role-badge badge-a">A</span> ATT</div>
            <div class="player-slot"><span class="role-badge badge-a">A</span> ATT</div>
        </div>
        <div class="pitch-row">
            <div class="player-slot"><span class="role-badge badge-c">C</span> CEN</div>
            <div class="player-slot"><span class="role-badge badge-c">C</span> CEN</div>
            <div class="player-slot"><span class="role-badge badge-c">C</span> CEN</div>
            <div class="player-slot"><span class="role-badge badge-c">C</span> CEN</div>
        </div>
        <div class="pitch-row">
            <div class="player-slot"><span class="role-badge badge-d">D</span> DIF</div>
            <div class="player-slot"><span class="role-badge badge-d">D</span> DIF</div>
            <div class="player-slot"><span class="role-badge badge-d">D</span> DIF</div>
        </div>
        <div class="pitch-row">
            <div class="player-slot"><span class="role-badge badge-p">P</span> POR</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with tab_scambi:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">🔄 Area Confronto Scambi</div>
        <p style="color:#cbd5e0; font-size:0.9rem;">Spazio riservato al calcolatore convenienza trade.</p>
    </div>
    """, unsafe_allow_html=True)
