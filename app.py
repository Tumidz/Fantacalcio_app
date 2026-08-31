import streamlit as st

# 1. Configurazione della pagina
st.set_page_config(
    page_title="FantaIA v0.0.3",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. CSS Avanzato v0.0.3 (Badge Ruoli + Campo Verde)
custom_css = """
<style>
    /* Sfondo principale */
    .stApp {
        background-color: #0b1319;
        color: #f0f4f8;
    }

    /* Header elegante */
    .header-container {
        background: linear-gradient(135deg, #1b4332 0%, #081c15 100%);
        border: 1px solid #2d6a4f;
        padding: 16px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }
    
    .version-badge {
        background-color: #52b788;
        color: #081c15;
        font-weight: bold;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        display: inline-block;
        margin-top: 4px;
    }

    /* Badge Ruoli Fantacalcio */
    .role-badge {
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 800;
        font-size: 0.85rem;
        color: #ffffff;
        display: inline-block;
        margin-right: 5px;
    }
    .badge-p { background-color: #e67e22; } /* Portiere - Arancione */
    .badge-d { background-color: #27ae60; } /* Difensore - Verde */
    .badge-c { background-color: #2980b9; } /* Centrocampista - Blu */
    .badge-a { background-color: #c0392b; } /* Attaccante - Rosso */

    /* Tab Touch */
    div[data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #16222f;
        padding: 6px;
        border-radius: 12px;
    }

    div[data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        color: #a0aec0;
        font-weight: 600;
        padding: 8px 12px;
        border: none !important;
    }

    div[aria-selected="true"] {
        background-color: #2d6a4f !important;
        color: #ffffff !important;
    }

    /* Card generali */
    .fanta-card {
        background: #16222f;
        border: 1px solid #243447;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 15px;
    }

    .fanta-card-title {
        color: #52b788;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 8px;
    }

    /* Simulazione Campo Verde da Gioco */
    .pitch-container {
        background: linear-gradient(180deg, #1e5631 0%, #143d21 100%);
        border: 2px solid #52b788;
        border-radius: 14px;
        padding: 20px 10px;
        text-align: center;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.6);
        margin-top: 10px;
    }

    .pitch-row {
        display: flex;
        justify-content: space-around;
        margin: 12px 0;
    }

    .player-slot {
        background: rgba(11, 19, 25, 0.85);
        border: 1px solid #52b788;
        border-radius: 8px;
        padding: 6px 10px;
        font-size: 0.75rem;
        font-weight: 600;
        color: #ffffff;
        min-width: 65px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. Header
st.markdown("""
<div class="header-container">
    <h1 style="margin:0; font-size:1.8rem; color:#ffffff;">⚽ FantaIA Assistant</h1>
    <span class="version-badge">v0.0.3 - Style & Badges</span>
</div>
""", unsafe_allow_html=True)

# 4. Navigazione a Schede
tab_home, tab_asta, tab_formazione, tab_scambi = st.tabs([
    "🏠 Home", 
    "🔨 Asta", 
    "📋 Formazione", 
    "🔄 Scambi"
])

with tab_home:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">🎨 Anteprima Ruoli e Codici Colore</div>
        <p style="color:#cbd5e0; font-size:0.9rem;">
            Ecco come appariranno le schede dei calciatori nell'interfaccia:
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
        <p style="color:#cbd5e0; font-size:0.9rem;">Pronta per accogliere i rilanci rapidi e la suddivisione budget.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Esempio card giocatore in asta
    st.markdown("""
    <div class="fanta-card" style="border-left: 4px solid #c0392b;">
        <span class="role-badge badge-a">A</span> <b>Lautaro Martinez</b> (Inter)<br/>
        <small style="color:#a0aec0;">Prezzo Consigliato IA: 140 / 500 FM</small>
    </div>
    """, unsafe_allow_html=True)

with tab_formazione:
    st.markdown('<div class="fanta-card-title">📋 Anteprima Campo Tattico (3-4-3)</div>', unsafe_allow_html=True)
    
    # Render del campo grafico verde
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
        <p style="color:#cbd5e0; font-size:0.9rem;">Sezione pronta per l'algoritmo di calcolo convenienza scambi.</p>
    </div>
    """, unsafe_allow_html=True)
