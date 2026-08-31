import streamlit as st
import pandas as pd
import random

# 1. Configurazione della pagina
st.set_page_config(
    page_title="FantaIA Assistant v0.4.0",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Immagini di sfondo
URL_SFONDO_STADIO = "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?q=80&w=1920&auto=format&fit=crop"

# 2. INIZIALIZZAZIONE Session State
if "budget_iniziale" not in st.session_state:
    st.session_state.budget_iniziale = 500

if "nome_mia_squadra" not in st.session_state:
    st.session_state.nome_mia_squadra = "Mia Squadra ⭐️"

if "squadre_lega" not in st.session_state:
    st.session_state.squadre_lega = [
        "Mia Squadra ⭐️", "FC Avversario 1", "FC Avversario 2", 
        "FC Avversario 3", "FC Avversario 4", "FC Avversario 5", 
        "FC Avversario 6", "FC Avversario 7"
    ]

if "tutti_acquisti" not in st.session_state:
    st.session_state.tutti_acquisti = []

if "stato_giocatori" not in st.session_state:
    st.session_state.stato_giocatori = {}

# Configurazione Moduli Tattici
MODULI = {
    "3-4-3": {"D": 3, "C": 4, "A": 3},
    "4-3-3": {"D": 4, "C": 3, "A": 3},
    "4-4-2": {"D": 4, "C": 4, "A": 2},
    "3-5-2": {"D": 3, "C": 5, "A": 2},
    "4-5-1": {"D": 4, "C": 5, "A": 1},
    "5-3-2": {"D": 5, "C": 3, "A": 2}
}

SLOT_MAX = {"P": 3, "D": 8, "C": 8, "A": 6}

# 3. CSS Avanzato
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

    /* Tabs Navigazione */
    div[data-baseweb="tab-list"] {{
        justify-content: center !important;
        gap: 4px !important;
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
        padding: 6px 10px !important;
        transition: all 0.25s ease-in-out !important;
    }}

    button[data-baseweb="tab"] p {{
        color: #d1d5db !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
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

    .status-badge {{
        font-size: 0.75rem;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: bold;
        display: inline-block;
        margin-left: 4px;
    }}
    .status-inf {{ background-color: #c0392b; color: white; }}
    .status-squ {{ background-color: #d35400; color: white; }}
    .status-dub {{ background-color: #f39c12; color: black; }}

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

    .pitch-container {{
        background: linear-gradient(180deg, #1b4d27 0%, #11331a 100%);
        border: 2px solid #52b788;
        border-radius: 16px;
        padding: 22px 12px;
        text-align: center;
        box-shadow: inset 0 0 25px rgba(0,0,0,0.7);
        margin: 15px 0;
    }}

    .pitch-row {{
        display: flex;
        justify-content: space-around;
        align-items: center;
        margin: 14px 0;
        gap: 6px;
    }}

    .player-card-pitch {{
        background: rgba(15, 25, 35, 0.92);
        border: 1px solid #52b788;
        border-radius: 8px;
        padding: 6px 8px;
        font-size: 0.78rem;
        font-weight: 600;
        color: #ffffff;
        flex: 1;
        max-width: 110px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.4);
    }}

    .player-name {{
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        font-weight: 700;
    }}

    .player-team {{
        font-size: 0.68rem;
        color: #94a3b8;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 4. Header Visivo
st.markdown("""
<div class="header-container">
    <h1 style="margin:0; font-size:1.8rem; color:#ffffff;">⚽ FantaIA Assistant</h1>
    <span class="version-badge">v0.4.0 - Match Simulator & Odds Engine</span>
</div>
""", unsafe_allow_html=True)

# 5. Navigazione a Schede
tab_home, tab_asta, tab_radar, tab_formazione, tab_trade, tab_sim = st.tabs([
    "🏠 Home", 
    "🔨 Asta Live", 
    "📊 Lega", 
    "📋 Formazione",
    "🔄 Trade",
    "⚔️ Scontro Diretto"
])

# --- FUNZIONI DI SUPPORTO ---
def get_stats_squadra(nome_squadra):
    acquisti = [p for p in st.session_state.tutti_acquisti if p["fantasquadra"] == nome_squadra]
    spesi = sum(p["prezzo"] for p in acquisti)
    rimasti = st.session_state.budget_iniziale - spesi
    count_p = sum(1 for p in acquisti if p["ruolo"] == "P")
    count_d = sum(1 for p in acquisti if p["ruolo"] == "D")
    count_c = sum(1 for p in acquisti if p["ruolo"] == "C")
    count_a = sum(1 for p in acquisti if p["ruolo"] == "A")
    return {
        "acquisti": acquisti, "spesi": spesi, "rimasti": rimasti,
        "P": count_p, "D": count_d, "C": count_c, "A": count_a,
        "totali": len(acquisti)
    }

stats_mia = get_stats_squadra(st.session_state.nome_mia_squadra)

TEST_PLAYERS = {
    "P": [("Sommer", "INT"), ("Maignan", "MIL"), ("Di Gregorio", "JUV")],
    "D": [("Dimarco", "INT"), ("Theo", "MIL"), ("Bremer", "JUV"), ("Di Lorenzo", "NAP"), ("Bastoni", "INT"), ("Buongiorno", "NAP"), ("Pavard", "INT"), ("Darmian", "INT")],
    "C": [("Barella", "INT"), ("Pulisic", "MIL"), ("Koopmeiners", "JUV"), ("Zaccagni", "LAZ"), ("Calhanoglu", "INT"), ("Man", "PAR"), ("McTominay", "NAP"), ("Ederson", "ATA")],
    "A": [("Lautaro", "INT"), ("Vlahovic", "JUV"), ("Thuram", "INT"), ("Kvaratskhelia", "NAP"), ("Retegui", "ATA"), ("Lukaku", "NAP")]
}

def get_complete_roster(nome_squadra=None):
    if nome_squadra is None:
        nome_squadra = st.session_state.nome_mia_squadra
        
    reali = [p for p in st.session_state.tutti_acquisti if p["fantasquadra"] == nome_squadra]
    completa = []
    
    for r_code in ["P", "D", "C", "A"]:
        giocatori_r = [p for p in reali if p["ruolo"] == r_code]
        n_mancanti = SLOT_MAX[r_code] - len(giocatori_r)
        completa.extend(giocatori_r)
        
        test_pool = TEST_PLAYERS[r_code]
        for i in range(n_mancanti):
            nome_t, sq_t = test_pool[(i + hash(nome_squadra)) % len(test_pool)]
            completa.append({
                "nome": f"{nome_t} ({nome_squadra[:3]})*",
                "squadra_sa": sq_t,
                "ruolo": r_code,
                "prezzo": random.randint(10, 38)
            })
    return completa

def seleziona_formazione_ottimale(roster, modulo_str="3-4-3"):
    req = MODULI[modulo_str]
    titolari = []
    for r_code in ["P", "D", "C", "A"]:
        giocatori_r = [p for p in roster if p["ruolo"] == r_code]
        sorted_r = sorted(giocatori_r, key=lambda x: x["prezzo"], reverse=True)
        n_tit = 1 if r_code == "P" else req[r_code]
        titolari.extend(sorted_r[:n_tit])
    return titolari


# --- CONTENUTO SCHEDE ---

with tab_home:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">📊 Centro Comando & Situazione Rosa</div>
        <p style="color:#cbd5e0; font-size:0.9rem;">Stato attuale della tua fanta-squadra:</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1: st.metric(label="Budget Iniziale", value=f"{st.session_state.budget_iniziale} FM")
    with col2: st.metric(label="Spesi", value=f"{stats_mia['spesi']} FM")
    with col3: st.metric(label="Crediti Rimasti", value=f"{stats_mia['rimasti']} FM")

    st.markdown("<br/>", unsafe_allow_html=True)
    st.subheader("📋 Tuoi Slot Acquistati")
    col_p, col_d, col_c, col_a = st.columns(4)
    with col_p: st.metric(label="Portieri", value=f"{stats_mia['P']} / 3")
    with col_d: st.metric(label="Difensori", value=f"{stats_mia['D']} / 8")
    with col_c: st.metric(label="Centrocampisti", value=f"{stats_mia['C']} / 8")
    with col_a: st.metric(label="Attaccanti", value=f"{stats_mia['A']} / 6")


with tab_asta:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">🔨 Registrazione Chiamate Asta</div>
        <p style="color:#cbd5e0; font-size:0.9rem; margin-bottom:0;">
            Registra rapidamente i calciatori aggiudicati a te o agli altri fanta-allenatori.
        </p>
    </div>
    """, unsafe_allow_html=True)

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
            prezzo = st.number_input("Prezzo FM", min_value=1, value=1)

        submit_btn = st.form_submit_button("✅ Registra Aggiudicazione")

        if submit_btn:
            if nome_giocatore.strip() == "":
                st.error("Inserisci il nome del calciatore!")
            else:
                st.session_state.tutti_acquisti.append({
                    "fantasquadra": fantasquadra_acquirente,
                    "nome": nome_giocatore.strip(),
                    "squadra_sa": squadra_serie_a.strip().upper(),
                    "ruolo": ruolo,
                    "prezzo": int(prezzo)
                })
                st.success(f"{nome_giocatore} assegnato a {fantasquadra_acquirente}!")
                st.rerun()


with tab_radar:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">📊 Classifica Crediti & Rose della Lega</div>
    </div>
    """, unsafe_allow_html=True)
    dati_tabella = []
    for sq in st.session_state.squadre_lega:
        st_sq = get_stats_squadra(sq)
        dati_tabella.append({
            "Fantasquadra": sq,
            "Crediti Rimasti": f"{st_sq['rimasti']} FM",
            "Spesi": f"{st_sq['spesi']} FM",
            "P": f"{st_sq['P']}/3", "D": f"{st_sq['D']}/8",
            "C": f"{st_sq['C']}/8", "A": f"{st_sq['A']}/6",
            "Totali": f"{st_sq['totali']}/25"
        })
    st.dataframe(pd.DataFrame(dati_tabella), use_container_width=True, hide_index=True)


with tab_formazione:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">📋 Assistente Schieramento IA</div>
    </div>
    """, unsafe_allow_html=True)

    roster_completo = get_complete_roster()

    with st.expander("🚑 Gestione Infortunati e Squalificati", expanded=False):
        cols_indis = st.columns(2)
        for idx, p in enumerate(roster_completo):
            col_target = cols_indis[idx % 2]
            p_nome = p["nome"]
            stato_attuale = st.session_state.stato_giocatori.get(p_nome, "Disponibile")
            
            nuovo_stato = col_target.selectbox(
                f"{p['nome']} ({p['ruolo']})",
                options=["Disponibile 🟢", "Infortunato 🚑", "Squalificato 🟥", "In Dubbio ❓"],
                index=["Disponibile 🟢", "Infortunato 🚑", "Squalificato 🟥", "In Dubbio ❓"].index(
                    f"{stato_attuale} 🟢" if stato_attuale == "Disponibile" else
                    f"{stato_attuale} 🚑" if stato_attuale == "Infortunato" else
                    f"{stato_attuale} 🟥" if stato_attuale == "Squalificato" else
                    f"{stato_attuale} ❓"
                ),
                key=f"status_sel_{p_nome}"
            )
            st.session_state.stato_giocatori[p_nome] = nuovo_stato.split()[0]

    modulo_scelto = st.selectbox("Seleziona Modulo:", options=list(MODULI.keys()), index=0)
    
    titolari_list = seleziona_formazione_ottimale(roster_completo, modulo_scelto)
    st.success(f"Formazione schierata correttamente per il modulo **{modulo_scelto}**!")


with tab_trade:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">🔄 Trade Radar IA</div>
    </div>
    """, unsafe_allow_html=True)

    col_sq1, col_sq2 = st.columns(2)
    with col_sq1:
        squadra_mia = st.selectbox("La tua squadra:", options=[st.session_state.nome_mia_squadra], index=0)
        roster_mio = get_complete_roster(squadra_mia)
        offerti_sel = st.multiselect("Offri:", options=[f"[{p['ruolo']}] {p['nome']} - {p['prezzo']} FM" for p in roster_mio])

    with col_sq2:
        altre_squadre = [sq for sq in st.session_state.squadre_lega if sq != st.session_state.nome_mia_squadra]
        squadra_rivale = st.selectbox("Squadra rivale:", options=altre_squadre, index=0)
        roster_rivale = get_complete_roster(squadra_rivale)
        richiesti_sel = st.multiselect("Richiedi:", options=[f"[{p['ruolo']}] {p['nome']} - {p['prezzo']} FM" for p in roster_rivale])


# --- NUOVA SCHEDA v0.4.0: SIMULATORE SCONTRO DIRETTO ---
with tab_sim:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">⚔️ Simulatore Scontro Diretto & Match Odds</div>
        <p style="color:#cbd5e0; font-size:0.9rem; margin-bottom:0;">
            Simula lo scontro di giornata contro una fanta-squadra rivale e calcola le probabilità di vittoria.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_home_sq, col_away_sq = st.columns(2)
    with col_home_sq:
        team_home = st.selectbox("Fanta-Squadra Casa 🏠", options=st.session_state.squadre_lega, index=0)
        mod_home = st.selectbox("Modulo Casa:", options=list(MODULI.keys()), index=0, key="mod_h")
    with col_away_sq:
        altre_sq = [s for s in st.session_state.squadre_lega if s != team_home]
        team_away = st.selectbox("Fanta-Squadra Trasferta ✈️", options=altre_sq, index=0)
        mod_away = st.selectbox("Modulo Trasferta:", options=list(MODULI.keys()), index=0, key="mod_a")

    st.markdown("<br/>", unsafe_allow_html=True)
    btn_simula = st.button("🎲 Esegui 1.000 Simulazioni Monte Carlo", use_container_width=True)

    if btn_simula:
        roster_h = get_complete_roster(team_home)
        roster_a = get_complete_roster(team_away)

        tit_h = seleziona_formazione_ottimale(roster_h, mod_home)
        tit_a = seleziona_formazione_ottimale(roster_a, mod_away)

        def punteggio_base_giocatore(p):
            # Valore atteso base tra 6.0 e 8.0 in base al valore d'asta/prezzo
            b = 6.0 + min(p["prezzo"] * 0.06, 2.2)
            st_p = st.session_state.stato_giocatori.get(p["nome"], "Disponibile")
            if st_p == "In Dubbio": b -= 1.0
            elif st_p in ["Infortunato", "Squalificato"]: b = 0.0
            return b

        def calcola_gol(punteggio_totale):
            if punteggio_totale < 66.0: return 0
            return int(1 + (punteggio_totale - 66.0) // 6.0)

        wins_h, draws, wins_a = 0, 0, 0
        tot_score_h_sum, tot_score_a_sum = 0, 0
        N_SIM = 1000

        for _ in range(N_SIM):
            # Simulazione voti con rumore gaussiano (+ bonus casa di +2.0 pt)
            score_h = sum(max(0, random.gauss(punteggio_base_giocatore(p), 1.3)) for p in tit_h) + 2.0
            score_a = sum(max(0, random.gauss(punteggio_base_giocatore(p), 1.3)) for p in tit_a)

            tot_score_h_sum += score_h
            tot_score_a_sum += score_a

            gol_h = calcola_gol(score_h)
            gol_a = calcola_gol(score_a)

            if gol_h > gol_a: wins_h += 1
            elif gol_a > gol_h: wins_a += 1
            else: draws += 1

        pct_h = round((wins_h / N_SIM) * 100, 1)
        pct_draw = round((draws / N_SIM) * 100, 1)
        pct_a = round((wins_a / N_SIM) * 100, 1)
        avg_score_h = round(tot_score_h_sum / N_SIM, 1)
        avg_score_a = round(tot_score_a_sum / N_SIM, 1)

        st.markdown("---")
        st.markdown(f"<h3 style='text-align:center; color:#52b788;'>📊 Esito Simulazione Match Odds</h3>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1: st.metric(f"Vittoria {team_home}", f"{pct_h}%", f"Media pt: {avg_score_h}")
        with c2: st.metric("Pareggio 🤝", f"{pct_draw}%")
        with c3: st.metric(f"Vittoria {team_away}", f"{pct_a}%", f"Media pt: {avg_score_a}")

        st.markdown("##### 📈 Distribuzione delle Probabilità")
        st.progress(pct_h / 100.0, text=f"🏠 {team_home}: {pct_h}%")
        st.progress(pct_draw / 100.0, text=f"🤝 Pareggio: {pct_draw}%")
        st.progress(pct_a / 100.0, text=f"✈️ {team_away}: {pct_a}%")

        st.markdown("##### 🥊 Duelli Chiave Reparto per Reparto")
        att_h_val = sum(p["prezzo"] for p in tit_h if p["ruolo"] == "A")
        att_a_val = sum(p["prezzo"] for p in tit_a if p["ruolo"] == "A")
        
        st.write(f"• **Forza Attacco Casa:** `{att_h_val} FM` vs **Forza Attacco Trasferta:** `{att_a_val} FM`")
        if att_h_val > att_a_val:
            st.info(f"🔥 L'attacco di **{team_home}** ha una potenza di fuoco superiore (+{att_h_val - att_a_val} FM).")
        else:
            st.info(f"🔥 L'attacco di **{team_away}** ha una potenza di fuoco superiore (+{att_a_val - att_h_val} FM).")
