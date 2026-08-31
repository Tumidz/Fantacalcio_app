import streamlit as st
import pandas as pd
import random

# 1. Configurazione della pagina
st.set_page_config(
    page_title="FantaIA Assistant v0.6.0",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

URL_SFONDO_STADIO = "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?q=80&w=1920&auto=format&fit=crop"

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
    color = "#27ae60" if fdr <= 2 else ("#f39c12" if fdr == 3 else "#c0392b")
    badge_html = f"<span style='background-color:{color}; color:white; padding:2px 5px; border-radius:4px; font-size:0.7rem; font-weight:bold;'>{loc} {info['opp']}</span>"
    return badge_html, fdr

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
        {"role": "assistant", "content": "Ciao Mister! Sono il tuo Fanta-Coach IA. Dimmi i tuoi dubbi di formazione o usa i prompt rapidi qui sotto!"}
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
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 800;
        font-size: 0.75rem;
        color: #ffffff;
        display: inline-block;
        margin-right: 4px;
    }}
    .badge-p {{ background-color: #e67e22; }}
    .badge-d {{ background-color: #27ae60; }}
    .badge-c {{ background-color: #2980b9; }}
    .badge-a {{ background-color: #c0392b; }}

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
        font-size: 0.75rem;
        font-weight: 600;
        color: #ffffff;
        flex: 1;
        max-width: 115px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.4);
    }}

    .player-name {{
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        font-weight: 700;
    }}

    .player-team {{
        font-size: 0.65rem;
        color: #94a3b8;
        margin-bottom: 2px;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 4. Header Visivo
st.markdown("""
<div class="header-container">
    <h1 style="margin:0; font-size:1.8rem; color:#ffffff;">⚽ FantaIA Assistant</h1>
    <span class="version-badge">v0.6.0 - Fanta-Coach Chatbot & Quick Prompts</span>
</div>
""", unsafe_allow_html=True)

# 5. Navigazione a Schede
tab_home, tab_asta, tab_radar, tab_formazione, tab_coach, tab_trade, tab_sim = st.tabs([
    "🏠 Home", 
    "🔨 Asta Live", 
    "📊 Lega", 
    "📋 Formazione FDR",
    "💬 Fanta-Coach",
    "🔄 Trade",
    "⚔️ Scontro"
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


# --- LOGICA DEL FANTA-COACH ---
def rispondi_fanta_coach(user_query):
    query_lower = user_query.lower()
    roster = get_complete_roster()
    
    indisponibili = [p["nome"] for p in roster if st.session_state.stato_giocatori.get(p["nome"]) in ["Infortunato", "Squalificato"]]
    in_dubbio = [p["nome"] for p in roster if st.session_state.stato_giocatori.get(p["nome"]) == "In Dubbio"]
    
    if "modulo" in query_lower or "3-4-3" in query_lower or "4-3-3" in query_lower:
        attaccanti_top = [p for p in roster if p["ruolo"] == "A" and p["prezzo"] >= 20]
        if len(attaccanti_top) >= 3:
            return "💡 **Consiglio Modulo:** Con la qualità dei tuoi attaccanti ti consiglio decisamente il **3-4-3** per massimizzare i bonus in avanti!"
        else:
            return "💡 **Consiglio Modulo:** Ti conviene puntare su un **4-4-2** o **4-3-3** per rinforzare il centrocampo e sfruttare i modifcatori di difesa."
    
    elif "infortunat" in query_lower or "indisponibil" in query_lower or "chi manca" in query_lower:
        if not indisponibili and not in_dubbio:
            return "🟢 Buone notizie Mister! La rosa è al completo e non hai infortunati o squalificati segnalati."
        res = "🚨 **Report Indisponibili:**\n"
        if indisponibili:
            res += f"• **Out:** {', '.join(indisponibili)}\n"
        if in_dubbio:
            res += f"• **In dubbio:** {', '.join(in_dubbio)}\n"
        return res

    elif "consiglio" in query_lower or "titolari" in query_lower or "schiero" in query_lower:
        tit, _ = seleziona_formazione_fdr(roster, "3-4-3")
        att_names = [p["nome"] for p in tit["A"]]
        cent_names = [p["nome"] for p in tit["C"][:3]]
        return f"⚽ **Consiglio Formazione Express:**\nIn attacco vai con **{', '.join(att_names)}** (partite favorevoli secondo l'FDR). A centrocampo perni inamovibili: **{', '.join(cent_names)}**."

    else:
        return f"🤖 Ho analizzato la rosa: per questa giornata ti suggerisco di prestare attenzione all'indice di difficoltà partita (FDR) dei tuoi difensori. Schiera la linea a 4 con FDR più basso!"


# --- SCHEDE INTERFACCIA ---
with tab_home:
    st.markdown("<div class='fanta-card'><div class='fanta-card-title'>📊 Stato Rosa</div></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Budget", f"{st.session_state.budget_iniziale} FM")
    c2.metric("Spesi", f"{stats_mia['spesi']} FM")
    c3.metric("Rimasti", f"{stats_mia['rimasti']} FM")

with tab_asta:
    st.markdown("<div class='fanta-card'><div class='fanta-card-title'>🔨 Registrazione Asta</div></div>", unsafe_allow_html=True)
    with st.form("form_asta", clear_on_submit=True):
        f_sq = st.selectbox("Acquirente", options=st.session_state.squadre_lega)
        f_nome = st.text_input("Calciatore")
        col_a, col_b, col_c = st.columns(3)
        f_sa = col_a.text_input("Squadra Serie A", "INT")
        f_r = col_b.selectbox("Ruolo", ["P", "D", "C", "A"])
        f_p = col_c.number_input("Prezzo FM", min_value=1, value=1)
        if st.form_submit_button("✅ Registra"):
            if f_nome.strip():
                st.session_state.tutti_acquisti.append({
                    "fantasquadra": f_sq, "nome": f_nome.strip(),
                    "squadra_sa": f_sa.strip().upper(), "ruolo": f_r, "prezzo": int(f_p)
                })
                st.rerun()

with tab_radar:
    st.markdown("<div class='fanta-card'><div class='fanta-card-title'>📊 Classifica Lega</div></div>", unsafe_allow_html=True)
    dati = [{"Fantasquadra": sq, "Rimasti": f"{get_stats_squadra(sq)['rimasti']} FM", "Totali": f"{get_stats_squadra(sq)['totali']}/25"} for sq in st.session_state.squadre_lega]
    st.dataframe(pd.DataFrame(dati), use_container_width=True)

with tab_formazione:
    st.markdown("<div class='fanta-card'><div class='fanta-card-title'>📋 Formazione FDR</div></div>", unsafe_allow_html=True)
    roster_completo = get_complete_roster()
    modulo_scelto = st.selectbox("Modulo Tattico:", options=list(MODULI.keys()), index=0)
    tit_fdr, panch_fdr = seleziona_formazione_fdr(roster_completo, modulo_scelto)

    st.markdown(f"<h4 style='text-align:center; color:#52b788;'>🏟️ 11 Titolare ({modulo_scelto})</h4>", unsafe_allow_html=True)
    
    def render_card_fdr(p):
        badge_fdr, _ = get_fdr_info(p["squadra_sa"])
        return f"""
        <div class='player-card-pitch'>
            <span class='role-badge badge-{p['ruolo'].lower()}'>{p['ruolo']}</span>
            <div class='player-name'>{p['nome']}</div>
            <div class='player-team'>{p['squadra_sa']}</div>
            {badge_fdr}
        </div>
        """

    html_pitch = "<div class='pitch-container'>"
    for r in ["A", "C", "D", "P"]:
        html_pitch += "<div class='pitch-row'>"
        for p in tit_fdr[r]:
            html_pitch += render_card_fdr(p)
        html_pitch += "</div>"
    html_pitch += "</div>"
    st.markdown(html_pitch, unsafe_allow_html=True)


# --- NUOVA SCHEDA v0.6.0: FANTA-COACH CHATBOT ---
with tab_coach:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">💬 Fanta-Coach IA & Prompts dell'Ultimo Minuto</div>
        <p style="color:#cbd5e0; font-size:0.85rem; margin-bottom:0;">
            Chiedi un consiglio rapido al tuo assistente o clicca su uno dei prompt preimpostati.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##### ⚡ Quick Tactical Prompts")
    c_p1, c_p2, c_p3 = st.columns(3)
    
    prompt_click = None
    if c_p1.button("⚽ Chi schiero oggi?", use_container_width=True):
        prompt_click = "Chi schiero oggi in attacco?"
    if c_p2.button("📐 Meglio 3-4-3 o 4-3-3?", use_container_width=True):
        prompt_click = "Meglio schierare il 3-4-3 o il 4-3-3?"
    if c_p3.button("🚑 Report Indisponibili", use_container_width=True):
        prompt_click = "Chi sono gli infortunati e gli squalificati?"

    st.markdown("---")

    # Render Storico Chat
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Gestione Input o Prompt Rapido
    user_input = st.chat_input("Scrivi un messaggio al Fanta-Coach...")
    query_da_elaborare = prompt_click if prompt_click else user_input

    if query_da_elaborare:
        st.session_state.chat_messages.append({"role": "user", "content": query_da_elaborare})
        with st.chat_message("user"):
            st.markdown(query_da_elaborare)

        risposta_bot = rispondi_fanta_coach(query_da_elaborare)
        st.session_state.chat_messages.append({"role": "assistant", "content": risposta_bot})
        st.rerun()

with tab_trade:
    st.markdown("<div class='fanta-card'><div class='fanta-card-title'>🔄 Trade Radar</div></div>", unsafe_allow_html=True)

with tab_sim:
    st.markdown("<div class='fanta-card'><div class='fanta-card-title'>⚔️ Match Simulator</div></div>", unsafe_allow_html=True)
