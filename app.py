import streamlit as st
import pandas as pd
import random

# 1. Configurazione Pagina
st.set_page_config(
    page_title="FantaIA Assistant v0.7.0",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Immagine di sfondo Stadio ad alta definizione
URL_SFONDO_STADIO = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?q=80&w=1920&auto=format&fit=crop"

# DATI CALENDARIO E DIFFICOLTÀ (FDR: 1 Facile -> 5 Difficile)
CALENDARIO_SERIE_A = {
    "INT": {"opp": "VEN", "fdr": 1, "casa": True},
    "MIL": {"opp": "JUV", "fdr": 4, "casa": False},
    "JUV": {"opp": "MIL", "fdr": 4, "casa": True},
    "NAP": {"opp": "EMP", "fdr": 2, "casa": True},
    "ATA": {"opp": "ROM", "fdr": 3, "casa": False},
    "LAZ": {"opp": "FIO", "fdr": 3, "casa": True},
    "PAR": {"opp": "MON", "fdr": 2, "casa": False},
}

def get_fdr_info(squadra_sa):
    info = CALENDARIO_SERIE_A.get(squadra_sa, {"opp": "N/D", "fdr": 3, "casa": True})
    loc = "vs" if info["casa"] else "@"
    fdr = info["fdr"]
    color = "🟢" if fdr <= 2 else ("🟡" if fdr == 3 else "🔴")
    return f"{loc} {info['opp']} {color}", fdr

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

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "Ciao Mister! Sono il tuo Fanta-Coach IA. Dimmi i tuoi dubbi sul modulo o sugli esiti dei match!"}
    ]

MODULI = {
    "3-4-3": {"D": 3, "C": 4, "A": 3},
    "4-3-3": {"D": 4, "C": 3, "A": 3},
    "4-4-2": {"D": 4, "C": 4, "A": 2},
    "3-5-2": {"D": 3, "C": 5, "A": 2},
    "4-5-1": {"D": 4, "C": 5, "A": 1},
    "5-3-2": {"D": 5, "C": 3, "A": 2}
}

SLOT_MAX = {"P": 3, "D": 8, "C": 8, "A": 6}

# 3. CSS Personalizzato Integrato
st.markdown(f"""
<style>
    .stApp {{
        background-image: linear-gradient(rgba(10, 17, 24, 0.90), rgba(10, 17, 24, 0.95)), url("{URL_SFONDO_STADIO}");
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
    }}
    .version-badge {{
        background-color: #52b788;
        color: #081c15;
        font-weight: bold;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.8rem;
    }}
    .fanta-card {{
        background: rgba(22, 34, 47, 0.85);
        border: 1px solid #243447;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 15px;
    }}
    .fanta-card-title {{
        color: #52b788;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 10px;
    }}
</style>
""", unsafe_allow_html=True)

# 4. Header
st.markdown("""
<div class="header-container">
    <h1 style="margin:0; font-size:1.8rem; color:#ffffff;">⚽ FantaIA Assistant</h1>
    <span class="version-badge">v0.7.0 - Custom Tactical Engine</span>
</div>
""", unsafe_allow_html=True)

# 5. Navigazione Schede
tab_home, tab_asta, tab_modulo, tab_coach, tab_trade, tab_sim = st.tabs([
    "🏠 Home", 
    "🔨 Asta", 
    "📋 Modulo",
    "💬 Fanta-Coach",
    "🔄 Trade",
    "⚔️ Match Simulator"
])

def get_stats_squadra(nome_squadra):
    acquisti = [p for p in st.session_state.tutti_acquisti if p["fantasquadra"] == nome_squadra]
    spesi = sum(p["prezzo"] for p in acquisti)
    rimasti = st.session_state.budget_iniziale - spesi
    return {
        "acquisti": acquisti, "spesi": spesi, "rimasti": rimasti,
        "P": sum(1 for p in acquisti if p["ruolo"] == "P"),
        "D": sum(1 for p in acquisti if p["ruolo"] == "D"),
        "C": sum(1 for p in acquisti if p["ruolo"] == "C"),
        "A": sum(1 for p in acquisti if p["ruolo"] == "A"),
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
                "prezzo": random.randint(12, 38)
            })
    return completa

def seleziona_formazione_fdr(roster, modulo_str="3-4-3"):
    req = MODULI[modulo_str]
    titolari = {"P": [], "D": [], "C": [], "A": []}
    panchina = []

    def calcola_score_fdr(p):
        st_p = st.session_state.stato_giocatori.get(p["nome"], "Disponibile")
        if st_p in ["Infortunato", "Squalificato"]:
            return -999.0
        
        _, fdr = get_fdr_info(p["squadra_sa"])
        base_val = p.get("prezzo", 10)
        fdr_modifier = (3 - fdr) * 3.5 
        dubbio_penalty = -15.0 if st_p == "In Dubbio" else 0.0
        return base_val + fdr_modifier + dubbio_penalty

    for r_code in ["P", "D", "C", "A"]:
        giocatori_r = [p for p in roster if p["ruolo"] == r_code]
        sorted_r = sorted(giocatori_r, key=calcola_score_fdr, reverse=True)
        n_tit = 1 if r_code == "P" else req[r_code]
        
        titolari[r_code] = sorted_r[:n_tit]
        panchina.extend(sorted_r[n_tit:])

    return titolari, panchina


# --- HOME ---
with tab_home:
    st.markdown("<div class='fanta-card'><div class='fanta-card-title'>📊 Situazione Mia Rosa</div></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Budget Iniziale", f"{st.session_state.budget_iniziale} FM")
    c2.metric("Spesi", f"{stats_mia['spesi']} FM")
    c3.metric("Crediti Rimasti", f"{stats_mia['rimasti']} FM")


# --- ASTA (LIVE & BUSTA CHIUSA) ---
with tab_asta:
    st.markdown("<div class='fanta-card'><div class='fanta-card-title'>🔨 Centro Gestione Asta</div></div>", unsafe_allow_html=True)
    
    tipo_asta = st.radio("Seleziona Modalità Asta:", ["🔴 Live Stream / Chiamata", "✉️ Busta Chiusa"], horizontal=True)

    if tipo_asta == "🔴 Live Stream / Chiamata":
        st.caption("Registra le chiamate e gli acquisti in tempo reale.")
        with st.form("form_asta_live", clear_on_submit=True):
            f_sq = st.selectbox("Acquirente", options=st.session_state.squadre_lega)
            f_nome = st.text_input("Nome Calciatore")
            col_a, col_b, col_c = st.columns(3)
            f_sa = col_a.text_input("Squadra Serie A", "INT")
            f_r = col_b.selectbox("Ruolo", ["P", "D", "C", "A"])
            f_p = col_c.number_input("Prezzo FM", min_value=1, value=1)
            if st.form_submit_button("✅ Registra Aggiudicazione"):
                if f_nome.strip():
                    st.session_state.tutti_acquisti.append({
                        "fantasquadra": f_sq, "nome": f_nome.strip(),
                        "squadra_sa": f_sa.strip().upper(), "ruolo": f_r, "prezzo": int(f_p)
                    })
                    st.success(f"{f_nome} registrato!")
                    st.rerun()

    else:
        st.caption("Calcola la puntata ideale in busta chiusa ponderata sul budget residuo e il valore target.")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            nome_target = st.text_input("Calciatore Target", placeholder="es. Lautaro Martinez")
            ruolo_target = st.selectbox("Ruolo Target", ["A", "C", "D", "P"])
        with col_b2:
            valore_stimato = st.number_input("Valore Base Stimato (FM)", min_value=1, value=30)
            priorita = st.select_slider("Livello di Priorità", options=["Basso", "Medio", "Top Player 🔥"])

        if st.button("🧠 Calcola Offerta Ottimale in Busta"):
            mult = 1.15 if priorita == "Basso" else (1.35 if priorita == "Medio" else 1.60)
            offerta_consigliata = int(min(stats_mia["rimasti"] * 0.8, valore_stimato * mult))
            
            st.markdown(f"""
            <div style="background:rgba(82, 183, 136, 0.15); border:1px solid #52b788; padding:12px; border-radius:10px; margin-top:10px;">
                💡 <b>Offerta Consigliata per {nome_target if nome_target else 'il target'}:</b><br/>
                Offri esattamente <b>{offerta_consigliata} FM</b> (Max sicurezza senza svenarti).
            </div>
            """, unsafe_allow_html=True)


# --- MODULO (EX FORMAZIONE FDR - CORRETTO SENZA BUG CODICE) ---
with tab_modulo:
    st.markdown("<div class='fanta-card'><div class='fanta-card-title'>📋 Configurazione Modulo Tattico & 11 Titolare</div></div>", unsafe_allow_html=True)
    
    roster_completo = get_complete_roster()
    modulo_scelto = st.selectbox("Seleziona Modulo Tattico:", options=list(MODULI.keys()), index=0)
    
    tit_fdr, panch_fdr = seleziona_formazione_fdr(roster_completo, modulo_scelto)

    st.markdown(f"### 🏟️ Campo da Gioco ({modulo_scelto})")

    # Renderizazione pulita mediante colonne native Streamlit per eliminare il bug delle righe di codice
    for ruolo_key, ruolo_nome in [("A", "Attacco ⚽"), ("C", "Centrocampo 🧠"), ("D", "Difesa 🛡️"), ("P", "Porta 🧤")]:
        st.caption(f"**{ruolo_nome}**")
        giocatori = tit_fdr[ruolo_key]
        cols = st.columns(len(giocatori))
        for idx, p in enumerate(giocatori):
            fdr_badge, _ = get_fdr_info(p["squadra_sa"])
            with cols[idx]:
                st.info(f"**{p['nome']}**\n\n{p['squadra_sa']} | {fdr_badge}")

    st.markdown("---")
    st.markdown("##### 🪑 Panchina")
    for p in panch_fdr[:7]:
        fdr_b, _ = get_fdr_info(p["squadra_sa"])
        st.write(f"• **[{p['ruolo']}]** {p['nome']} ({p['squadra_sa']}) - {fdr_b}")


# --- FANTA COACH ---
with tab_coach:
    st.markdown("<div class='fanta-card'><div class='fanta-card-title'>💬 Fanta-Coach Conversazionale</div></div>", unsafe_allow_html=True)
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Fai una domanda al Coach...")
    if user_input:
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        reply = "Mister, basandomi sul calendario ti consiglio di confermare il modulo attuale e verificare l'indice FDR della difesa."
        st.session_state.chat_messages.append({"role": "assistant", "content": reply})
        st.rerun()


# --- TRADE ---
with tab_trade:
    st.markdown("<div class='fanta-card'><div class='fanta-card-title'>🔄 Trade Radar</div></div>", unsafe_allow_html=True)
    st.info("Seleziona i giocatori per valutare l'equità dello scambio.")


# --- MATCH SIMULATOR (PER LA PARTITA ATTUALE) ---
with tab_sim:
    st.markdown("<div class='fanta-card'><div class='fanta-card-title'>⚔️ Match Simulator - Prossima Sfida</div></div>", unsafe_allow_html=True)
    
    st.write(f"🏠 **Squadra di Casa:** `{st.session_state.nome_mia_squadra}`")
    
    altre_sq = [s for s in st.session_state.squadre_lega if s != st.session_state.nome_mia_squadra]
    avversario_sfida = st.selectbox("Seleziona Avversario di Giornata ✈️", options=altre_sq, index=0)

    mod_mia = st.selectbox("Tuo Modulo:", options=list(MODULI.keys()), index=0, key="sim_m")
    mod_opp = st.selectbox("Modulo Avversario:", options=list(MODULI.keys()), index=0, key="sim_o")

    if st.button("🎲 Simula Gara (1.000 Monte Carlo)", use_container_width=True):
        roster_h = get_complete_roster(st.session_state.nome_mia_squadra)
        roster_a = get_complete_roster(avversario_sfida)

        tit_h, _ = seleziona_formazione_fdr(roster_h, mod_mia)
        tit_a, _ = seleziona_formazione_fdr(roster_a, mod_opp)

        wins_h, draws, wins_a = 0, 0, 0
        N_SIM = 1000

        for _ in range(N_SIM):
            score_h = sum(random.gauss(6.8, 1.2) for r in tit_h for p in tit_h[r]) + 2.0
            score_a = sum(random.gauss(6.7, 1.2) for r in tit_a for p in tit_a[r])
            
            gol_h = 0 if score_h < 66 else int(1 + (score_h - 66) // 6)
            gol_a = 0 if score_a < 66 else int(1 + (score_a - 66) // 6)

            if gol_h > gol_a: wins_h += 1
            elif gol_a > gol_h: wins_a += 1
            else: draws += 1

        pct_h = round((wins_h / N_SIM) * 100, 1)
        pct_d = round((draws / N_SIM) * 100, 1)
        pct_a = round((wins_a / N_SIM) * 100, 1)

        st.markdown("---")
        st.markdown(f"#### 📊 Probabilità Esito Match")
        c_w1, c_w2, c_w3 = st.columns(3)
        c_w1.metric("Vittoria Tua", f"{pct_h}%")
        c_w2.metric("Pareggio 🤝", f"{pct_d}%")
        c_w3.metric(f"Vittoria {avversario_sfida[:10]}", f"{pct_a}%")

        st.progress(pct_h / 100.0, text=f"Tu: {pct_h}%")
        st.progress(pct_d / 100.0, text=f"Pareggio: {pct_d}%")
        st.progress(pct_a / 100.0, text=f"{avversario_sfida}: {pct_a}%")
