import streamlit as st
import pandas as pd

# 1. Configurazione della pagina
st.set_page_config(
    page_title="FantaIA Assistant v0.1.1",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Immagini per lo sfondo e il martello 3D
URL_SFONDO_STADIO = "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?q=80&w=1920&auto=format&fit=crop"
URL_MARTELLO_ASTA = "https://cdn3d.iconscout.com/3d/premium/thumb/auction-gavel-4721151-3927976.png"

# 2. INIZIALIZZAZIONE "QUADERNO DI MEMORIA" (Session State)
if "budget_iniziale" not in st.session_state:
    st.session_state.budget_iniziale = 500

if "nome_mia_squadra" not in st.session_state:
    st.session_state.nome_mia_squadra = "Mia Squadra ⭐️"

if "squadre_lega" not in st.session_state:
    st.session_state.squadre_lega = [
        "Mia Squadra ⭐️",
        "FC Avversario 1",
        "FC Avversario 2",
        "FC Avversario 3",
        "FC Avversario 4",
        "FC Avversario 5",
        "FC Avversario 6",
        "FC Avversario 7"
    ]

if "tutti_acquisti" not in st.session_state:
    # Struttura: {"fantasquadra": str, "nome": str, "squadra_sa": str, "ruolo": str, "prezzo": int}
    st.session_state.tutti_acquisti = []

# Slot standard Fantacalcio
SLOT_MAX = {"P": 3, "D": 8, "C": 8, "A": 6}

# 3. CSS Avanzato (Grafica Unificata v0.0.4 + Tabella Avversari)
custom_css = f"""
<style>
    .stApp {{
        background-image: linear-gradient(rgba(10, 17, 24, 0.90), rgba(10, 17, 24, 0.95)),
                          url("{URL_SFONDO_STADIO}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #f0f4f8;
    }}

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

    /* Pulsanti di navigazione */
    div[data-baseweb="tab-list"] {{
        justify-content: center !important;
        gap: 8px !important;
        border-bottom: none !important;
        background-color: transparent !important;
        padding-bottom: 10px !important;
    }}

    div[data-baseweb="tab-highlight"], 
    div[data-baseweb="tab-border"] {{
        display: none !important;
    }}

    button[data-baseweb="tab"] {{
        background-color: rgba(20, 32, 44, 0.8) !important;
        border: 1.5px solid #3d5a45 !important;
        border-radius: 10px !important;
        padding: 8px 14px !important;
        transition: all 0.25s ease-in-out !important;
    }}

    button[data-baseweb="tab"] p {{
        color: #d1d5db !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        margin: 0 !important;
    }}

    button[data-baseweb="tab"]:hover {{
        border-color: #52b788 !important;
        background-color: rgba(30, 46, 60, 0.9) !important;
    }}

    button[data-baseweb="tab"][aria-selected="true"] {{
        background-color: rgba(18, 32, 42, 0.95) !important;
        border: 2px solid #52b788 !important;
        box-shadow: 0 0 12px rgba(82, 183, 136, 0.5) !important;
    }}

    button[data-baseweb="tab"][aria-selected="true"] p {{
        color: #52b788 !important;
        font-weight: 700 !important;
    }}

    /* Badge Ruoli */
    .role-badge {{
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 800;
        font-size: 0.8rem;
        color: #ffffff;
        display: inline-block;
        margin-right: 6px;
    }}
    .badge-p {{ background-color: #e67e22; }}
    .badge-d {{ background-color: #27ae60; }}
    .badge-c {{ background-color: #2980b9; }}
    .badge-a {{ background-color: #c0392b; }}

    /* Card Generali */
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
        margin-bottom: 10px;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 4. Header Visivo
st.markdown("""
<div class="header-container">
    <h1 style="margin:0; font-size:1.8rem; color:#ffffff;">⚽ FantaIA Assistant</h1>
    <span class="version-badge">v0.1.1 - League & Radar Avversari</span>
</div>
""", unsafe_allow_html=True)

# 5. Navigazione a Schede
tab_home, tab_asta, tab_radar, tab_formazione = st.tabs([
    "🏠 Home", 
    "🔨 Asta Live", 
    "📊 Radar Lega", 
    "📋 Formazione"
])

# --- FUNZIONI UTILI DI CALCOLO LEGA ---
def get_stats_squadra(nome_squadra):
    acquisti = [p for p in st.session_state.tutti_acquisti if p["fantasquadra"] == nome_squadra]
    spesi = sum(p["prezzo"] for p in acquisti)
    rimasti = st.session_state.budget_iniziale - spesi
    count_p = sum(1 for p in acquisti if p["ruolo"] == "P")
    count_d = sum(1 for p in acquisti if p["ruolo"] == "D")
    count_c = sum(1 for p in acquisti if p["ruolo"] == "C")
    count_a = sum(1 for p in acquisti if p["ruolo"] == "A")
    totali = len(acquisti)
    slot_mancanti = 25 - totali
    return {
        "squadra": nome_squadra,
        "acquisti": acquisti,
        "spesi": spesi,
        "rimasti": rimasti,
        "P": count_p, "D": count_d, "C": count_c, "A": count_a,
        "totali": totali,
        "slot_mancanti": slot_mancanti
    }

stats_mia_squadra = get_stats_squadra(st.session_state.nome_mia_squadra)

# --- CONTENUTO SCHEDE ---

with tab_home:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">📊 Centro Comando & Situazione Rosa</div>
        <p style="color:#cbd5e0; font-size:0.9rem;">
            Stato attuale della tua fanta-squadra:
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Budget Iniziale", value=f"{st.session_state.budget_iniziale} FM")
    with col2:
        st.metric(label="Spesi", value=f"{stats_mia_squadra['spesi']} FM")
    with col3:
        st.metric(label="Crediti Rimasti", value=f"{stats_mia_squadra['rimasti']} FM")

    st.markdown("<br/>", unsafe_allow_html=True)
    st.subheader("📋 Tuoi Slot Completati")
    col_p, col_d, col_c, col_a = st.columns(4)
    with col_p:
        st.metric(label="Portieri", value=f"{stats_mia_squadra['P']} / 3")
    with col_d:
        st.metric(label="Difensori", value=f"{stats_mia_squadra['D']} / 8")
    with col_c:
        st.metric(label="Centrocampisti", value=f"{stats_mia_squadra['C']} / 8")
    with col_a:
        st.metric(label="Attaccanti", value=f"{stats_mia_squadra['A']} / 6")


with tab_asta:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">🔨 Registrazione Chiamate Asta</div>
        <p style="color:#cbd5e0; font-size:0.9rem; margin-bottom:0;">
            Registra rapidamente i calciatori aggiudicati a te o agli altri fanta-allenatori.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Form Registrazione Chiamata Asta
    with st.form("form_acquisto_unificato", clear_on_submit=True):
        st.markdown("##### 🛒 Nuovo Calciatore Aggiudicato")
        
        col_sq_fanta, col_nome = st.columns([1.2, 1.8])
        with col_sq_fanta:
            fantasquadra_acquirente = st.selectbox("Acquirente", options=st.session_state.squadre_lega)
        with col_nome:
            nome_giocatore = st.text_input("Nome Calciatore", placeholder="es. Lautaro Martinez")

        col_squadra_sa, col_ruolo, col_prezzo = st.columns([1, 1, 1])
        with col_squadra_sa:
            squadra_serie_a = st.text_input("Squadra Serie A", placeholder="es. Inter")
        with col_ruolo:
            ruolo = st.selectbox("Ruolo", options=["P", "D", "C", "A"])
        with col_prezzo:
            stats_acq = get_stats_squadra(fantasquadra_acquirente)
            max_p = max(1, stats_acq["rimasti"])
            prezzo = st.number_input("Prezzo FM", min_value=1, max_value=max_p, value=1)

        submit_btn = st.form_submit_button("✅ Registra Aggiudicazione")

        if submit_btn:
            if nome_giocatore.strip() == "":
                st.error("Inserisci il nome del calciatore!")
            elif stats_acq[ruolo] >= SLOT_MAX[ruolo]:
                st.warning(f"{fantasquadra_acquirente} ha già raggiunto il limite di {SLOT_MAX[ruolo]} per il ruolo {ruolo}!")
            else:
                st.session_state.tutti_acquisti.append({
                    "fantasquadra": fantasquadra_acquirente,
                    "nome": nome_giocatore.strip(),
                    "squadra_sa": squadra_serie_a.strip().upper(),
                    "ruolo": ruolo,
                    "prezzo": int(prezzo)
                })
                st.success(f"{nome_giocatore} assegnato a {fantasquadra_acquirente} per {prezzo} FM!")
                st.rerun()

    st.markdown("---")

    # Consigliere IA Tattico per l'Asta
    st.markdown("### 💡 Intelligence IA Competitiva")
    
    # Trova il rivale più ricco
    altre_stats = [get_stats_squadra(sq) for sq in st.session_state.squadre_lega if sq != st.session_state.nome_mia_squadra]
    if altre_stats:
        ricco = max(altre_stats, key=lambda x: x["rimasti"])
        st.info(f"🏆 **Rivale più pericoloso:** `{ricco['squadra']}` con **{ricco['rimasti']} FM** rimasti ({ricco['A']}/6 Attaccanti).\n\n"
                f"💡 **Tuo Budget Rimasto:** `{stats_mia_squadra['rimasti']} FM`")

    st.markdown("---")

    # Gestione Impostazioni Lega
    with st.expander("⚙️ Personalizza Nomi Squadre & Budget Lega", expanded=False):
        nuovo_budget = st.number_input("Budget Iniziale per tutti (FM):", min_value=100, max_value=2000, value=st.session_state.budget_iniziale, step=50)
        
        st.write("**Rinomina la tua Squadra:**")
        mio_nome = st.text_input("Tuo Nome", value=st.session_state.nome_mia_squadra)
        
        if st.button("Salva Impostazioni Lega"):
            st.session_state.budget_iniziale = nuovo_budget
            if mio_nome.strip() != "":
                # Aggiorna il nome nei vecchi acquisti se cambiato
                old_name = st.session_state.nome_mia_squadra
                st.session_state.nome_mia_squadra = mio_nome.strip()
                st.session_state.squadre_lega[0] = mio_nome.strip()
                for p in st.session_state.tutti_acquisti:
                    if p["fantasquadra"] == old_name:
                        p["fantasquadra"] = mio_nome.strip()
            st.rerun()


with tab_radar:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">📊 Classifica Crediti & Rose della Lega</div>
        <p style="color:#cbd5e0; font-size:0.9rem;">
            Panoramica in tempo reale di tutte le fantasquadre partecipanti.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Costruzione Tabella Riassuntiva Lega
    dati_tabella = []
    for sq in st.session_state.squadre_lega:
        st_sq = get_stats_squadra(sq)
        dati_tabella.append({
            "Fantasquadra": sq,
            "Crediti Rimasti": f"{st_sq['rimasti']} FM",
            "Spesi": f"{st_sq['spesi']} FM",
            "P": f"{st_sq['P']}/3",
            "D": f"{st_sq['D']}/8",
            "C": f"{st_sq['C']}/8",
            "A": f"{st_sq['A']}/6",
            "Totali": f"{st_sq['totali']}/25"
        })

    df_lega = pd.DataFrame(dati_tabella)
    st.dataframe(df_lega, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Ispezione Singola Rosa
    st.markdown("### 🔍 Ispeziona Rosa Avversaria")
    squadra_scelta = st.selectbox("Seleziona una squadra da analizzare:", options=st.session_state.squadre_lega)
    
    st_scelta = get_stats_squadra(squadra_scelta)
    if len(st_scelta["acquisti"]) == 0:
        st.write(f"Nessun calciatore acquistato da {squadra_scelta}.")
    else:
        for r_code, r_name in [("P", "Portieri"), ("D", "Difensori"), ("C", "Centrocampisti"), ("A", "Attaccanti")]:
            giocatori_r = [p for p in st_scelta["acquisti"] if p["ruolo"] == r_code]
            if giocatori_r:
                st.markdown(f"##### <span class='role-badge badge-{r_code.lower()}'>{r_code}</span> {r_name}", unsafe_allow_html=True)
                for idx, player in enumerate(st.session_state.tutti_acquisti):
                    if player["fantasquadra"] == squadra_scelta and player["ruolo"] == r_code:
                        col_i, col_d = st.columns([4, 1])
                        with col_i:
                            st.write(f"• **{player['nome']}** ({player['squadra_sa']}) — **{player['prezzo']} FM**")
                        with col_d:
                            if st.button("❌", key=f"del_all_{idx}"):
                                st.session_state.tutti_acquisti.pop(idx)
                                st.rerun()


with tab_formazione:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">📋 Assistente Schieramento (In arrivo nella v0.2.0)</div>
        <p style="color:#cbd5e0; font-size:0.9rem;">
            Il Modulo Asta v0.1.1 è ora completo! Prossimo step: l'IA per schierare la formazione ideale.
        </p>
    </div>
    """, unsafe_allow_html=True)
