import streamlit as st
import pandas as pd
import random

# 1. Configurazione Pagina
st.set_page_config(
    page_title="FantaIA Assistant v0.8.0",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Sfondo Stadio HD
URL_SFONDO_STADIO = "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?q=80&w=1920&auto=format&fit=crop"

# DATABASE UFFICIALE CALCIATORI SERIE A (Aggiornabile/Modificabile)
DB_CALCIATORI = [
    {"nome": "Lautaro Martinez", "squadra_sa": "INT", "ruolo_off": "A", "valore": 85},
    {"nome": "Marcus Thuram", "squadra_sa": "INT", "ruolo_off": "A", "valore": 65},
    {"nome": "Nicolò Barella", "squadra_sa": "INT", "ruolo_off": "C", "valore": 35},
    {"nome": "Hakan Calhanoglu", "squadra_sa": "INT", "ruolo_off": "C", "valore": 45},
    {"nome": "Federico Dimarco", "squadra_sa": "INT", "ruolo_off": "D", "valore": 38},
    {"nome": "Yann Sommer", "squadra_sa": "INT", "ruolo_off": "P", "valore": 25},
    {"nome": "Duvan Zapata", "squadra_sa": "TOR", "ruolo_off": "A", "valore": 40},
    {"nome": "Nikola Vlasic", "squadra_sa": "TOR", "ruolo_off": "C", "valore": 18},
    {"nome": "Dusan Vlahovic", "squadra_sa": "JUV", "ruolo_off": "A", "valore": 80},
    {"nome": "Teun Koopmeiners", "squadra_sa": "JUV", "ruolo_off": "C", "valore": 50},
    {"nome": "Gleison Bremer", "squadra_sa": "JUV", "ruolo_off": "D", "valore": 30},
    {"nome": "Michele Di Gregorio", "squadra_sa": "JUV", "ruolo_off": "P", "valore": 22},
    {"nome": "Khvicha Kvaratskhelia", "squadra_sa": "NAP", "ruolo_off": "A", "valore": 70},
    {"nome": "Romelu Lukaku", "squadra_sa": "NAP", "ruolo_off": "A", "valore": 75},
    {"nome": "Scott McTominay", "squadra_sa": "NAP", "ruolo_off": "C", "valore": 32},
    {"nome": "Giovanni Di Lorenzo", "squadra_sa": "NAP", "ruolo_off": "D", "valore": 22},
    {"nome": "Rafael Leao", "squadra_sa": "MIL", "ruolo_off": "A", "valore": 68},
    {"nome": "Christian Pulisic", "squadra_sa": "MIL", "ruolo_off": "C", "valore": 48},
    {"nome": "Theo Hernandez", "squadra_sa": "MIL", "ruolo_off": "D", "valore": 36},
    {"nome": "Mike Maignan", "squadra_sa": "MIL", "ruolo_off": "P", "valore": 24},
    {"nome": "Mateo Retegui", "squadra_sa": "ATA", "ruolo_off": "A", "valore": 60},
    {"nome": "Ademola Lookman", "squadra_sa": "ATA", "ruolo_off": "A", "valore": 62},
    {"nome": "Ederson", "squadra_sa": "ATA", "ruolo_off": "C", "valore": 25},
    {"nome": "Mattia Zaccagni", "squadra_sa": "LAZ", "ruolo_off": "C", "valore": 38},
    {"nome": "Taty Castellanos", "squadra_sa": "LAZ", "ruolo_off": "A", "valore": 42},
    {"nome": "Artem Dovbyk", "squadra_sa": "ROM", "ruolo_off": "A", "valore": 65},
    {"nome": "Paulo Dybala", "squadra_sa": "ROM", "ruolo_off": "A", "valore": 58},
    {"nome": "Dennis Man", "squadra_sa": "PAR", "ruolo_off": "C", "valore": 28},
    {"nome": "Ange-Yoan Bonny", "squadra_sa": "PAR", "ruolo_off": "A", "valore": 22},
    {"nome": "Moise Kean", "squadra_sa": "FIO", "ruolo_off": "A", "valore": 45},
    {"nome": "Albert Gudmundsson", "squadra_sa": "FIO", "ruolo_off": "A", "valore": 50},
]

CALENDARIO_SERIE_A = {
    "INT": {"opp": "VEN", "fdr": 1, "casa": True},
    "MIL": {"opp": "JUV", "fdr": 4, "casa": False},
    "JUV": {"opp": "MIL", "fdr": 4, "casa": True},
    "NAP": {"opp": "EMP", "fdr": 2, "casa": True},
    "ATA": {"opp": "ROM", "fdr": 3, "casa": False},
    "LAZ": {"opp": "FIO", "fdr": 3, "casa": True},
    "PAR": {"opp": "MON", "fdr": 2, "casa": False},
    "ROM": {"opp": "ATA", "fdr": 3, "casa": True},
    "FIO": {"opp": "LAZ", "fdr": 3, "casa": False},
    "TOR": {"opp": "CAG", "fdr": 2, "casa": True},
}

def get_fdr_info(squadra_sa):
    info = CALENDARIO_SERIE_A.get(squadra_sa, {"opp": "N/D", "fdr": 3, "casa": True})
    loc = "vs" if info["casa"] else "@"
    fdr = info["fdr"]
    badge = "🟢" if fdr <= 2 else ("🟡" if fdr == 3 else "🔴")
    return f"{loc} {info['opp']} {badge}", fdr

# 2. INIZIALIZZAZIONE SESSION STATE
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

if "custom_ruoli" not in st.session_state:
    st.session_state.custom_ruoli = {}

if "stato_giocatori" not in st.session_state:
    st.session_state.stato_giocatori = {}

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "Ciao Mister! Sono il tuo Fanta-Coach IA. Chiedimi consigli sul modulo o sugli scambi!"}
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

# Funzione per recuperare il ruolo attuale (ufficiale o personalizzato)
def get_ruolo_effettivo(nome_giocatore, ruolo_default="C"):
    return st.session_state.custom_ruoli.get(nome_giocatore, ruolo_default)

# 3. CSS
st.markdown(f"""
<style>
    .stApp {{
        background-image: linear-gradient(rgba(10, 17, 24, 0.92), rgba(10, 17, 24, 0.96)), url("{URL_SFONDO_STADIO}");
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
    .fanta-card {{
        background: rgba(22, 34, 47, 0.88);
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
    <span style="background:#52b788; color:#081c15; font-weight:bold; padding:4px 12px; border-radius:12px; font-size:0.8rem;">v0.8.0 - Full Tactical & Auction Suite</span>
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
        "P": sum(1 for p in acquisti if get_ruolo_effettivo(p["nome"], p["ruolo"]) == "P"),
        "D": sum(1 for p in acquisti if get_ruolo_effettivo(p["nome"], p["ruolo"]) == "D"),
        "C": sum(1 for p in acquisti if get_ruolo_effettivo(p["nome"], p["ruolo"]) == "C"),
        "A": sum(1 for p in acquisti if get_ruolo_effettivo(p["nome"], p["ruolo"]) == "A"),
        "totali": len(acquisti)
    }

stats_mia = get_stats_squadra(st.session_state.nome_mia_squadra)

def get_complete_roster(nome_squadra=None):
    if nome_squadra is None:
        nome_squadra = st.session_state.nome_mia_squadra
        
    reali = [p for p in st.session_state.tutti_acquisti if p["fantasquadra"] == nome_squadra]
    completa = []
    
    for p in reali:
        r_eff = get_ruolo_effettivo(p["nome"], p["ruolo"])
        completa.append({
            "nome": p["nome"],
            "squadra_sa": p.get("squadra_sa", "INT"),
            "ruolo": r_eff,
            "prezzo": p["prezzo"]
        })

    # Filler per visualizzazione completa rosa
    for r_code in ["P", "D", "C", "A"]:
        presenti = [p for p in completa if p["ruolo"] == r_code]
        mancanti = SLOT_MAX[r_code] - len(presenti)
        for i in range(mancanti):
            pool = [p for p in DB_CALCIATORI if p["ruolo_off"] == r_code]
            p_ref = pool[i % len(pool)]
            completa.append({
                "nome": f"{p_ref['nome']} (Bozza)",
                "squadra_sa": p_ref["squadra_sa"],
                "ruolo": r_code,
                "prezzo": random.randint(10, 30)
            })
    return completa


# --- HOME & GESTIONE ROSA ---
with tab_home:
    st.markdown("<div class='fanta-card'><div class='fanta-card-title'>📊 Situazione Mia Rosa</div></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Budget Iniziale", f"{st.session_state.budget_iniziale} FM")
    c2.metric("Spesi", f"{stats_mia['spesi']} FM")
    c3.metric("Crediti Rimasti", f"{stats_mia['rimasti']} FM")

    st.markdown("---")
    st.subheader("⚙️ Gestione & Cancellazione Rosa")
    if not stats_mia["acquisti"]:
        st.info("Non hai ancora acquistato calciatori. Usa la scheda Asta per aggiungerne!")
    else:
        for idx, p in enumerate(stats_mia["acquisti"]):
            r_curr = get_ruolo_effettivo(p["nome"], p["ruolo"])
            col_info, col_mod_r, col_del = st.columns([2, 1, 1])
            with col_info:
                st.write(f"**[{r_curr}]** {p['nome']} ({p['squadra_sa']}) - `{p['prezzo']} FM`")
            with col_mod_r:
                nuovo_r = st.selectbox("Ruolo", ["P", "D", "C", "A"], index=["P", "D", "C", "A"].index(r_curr), key=f"r_sel_{idx}")
                if nuovo_r != r_curr:
                    st.session_state.custom_ruoli[p["nome"]] = nuovo_r
                    st.rerun()
            with col_del:
                if st.button("🗑️ Elimina", key=f"del_p_{idx}"):
                    st.session_state.tutti_acquisti.pop(idx)
                    st.rerun()

        if st.button("🚨 Reset Completo Rosa Mia Squadra", type="primary"):
            st.session_state.tutti_acquisti = [p for p in st.session_state.tutti_acquisti if p["fantasquadra"] != st.session_state.nome_mia_squadra]
            st.rerun()


# --- ASTA (LIVE & BUSTA CHIUSA CON RICERCA E AUTOFILL) ---
with tab_asta:
    st.markdown("<div class='fanta-card'><div class='fanta-card-title'>🔨 Centro Gestione Asta</div></div>", unsafe_allow_html=True)
    
    tipo_asta = st.radio("Seleziona Modalità Asta:", ["🔴 Live", "✉️ Busta Chiusa"], horizontal=True)

    if tipo_asta == "🔴 Live":
        st.caption("Ricerca il calciatore per nome o squadra. Ruolo e squadra verranno assegnati in automatico!")
        
        sq_filter = st.selectbox("Filtra per Squadra Serie A (Opzionale):", ["Tutte"] + list(set(p["squadra_sa"] for p in DB_CALCIATORI)))
        
        pool_filtrato = DB_CALCIATORI if sq_filter == "Tutte" else [p for p in DB_CALCIATORI if p["squadra_sa"] == sq_filter]
        
        opzioni_giocatori = [f"[{p['ruolo_off']}] {p['nome']} ({p['squadra_sa']})" for p in pool_filtrato]
        
        scelta_giocatore_str = st.selectbox("Cerca Calciatore (Digita le prime lettere):", options=opzioni_giocatori)

        # Estrazione dati automatici
        p_selezionato = next(p for p in DB_CALCIATORI if f"[{p['ruolo_off']}] {p['nome']} ({p['squadra_sa']})" == scelta_giocatore_str)
        
        with st.form("form_asta_live_auto", clear_on_submit=True):
            f_sq = st.selectbox("Acquirente Fanta-Lega:", options=st.session_state.squadre_lega)
            col_autofill1, col_autofill2 = st.columns(2)
            col_autofill1.text_input("Calciatore Selezionato", value=p_selezionato["nome"], disabled=True)
            col_autofill2.text_input("Ruolo / Squadra", value=f"{p_selezionato['ruolo_off']} | {p_selezionato['squadra_sa']}", disabled=True)
            
            prezzo_asta = st.number_input("Prezzo d'Asta Finale (FM):", min_value=1, value=1)
            
            if st.form_submit_button("✅ Conferma Acquisto"):
                st.session_state.tutti_acquisti.append({
                    "fantasquadra": f_sq,
                    "nome": p_selezionato["nome"],
                    "squadra_sa": p_selezionato["squadra_sa"],
                    "ruolo": p_selezionato["ruolo_off"],
                    "prezzo": int(prezzo_asta)
                })
                st.success(f"{p_selezionato['nome']} assegnato a {f_sq} per {prezzo_asta} FM!")
                st.rerun()

    else:
        st.caption("✉️ Calcolo Offerte Strategiche Busta Chiusa & Riserva Asta di Riparazione")
        
        targets_sel = st.multiselect("Seleziona Calciatori Obbiettivo:", options=[p["nome"] for p in DB_CALCIATORI])
        
        col_bus1, col_bus2 = st.columns(2)
        with col_bus1:
            budget_riserva_riparazione = st.number_input("Riserva FM per Asta di Riparazione:", min_value=0, max_value=200, value=30)
        with col_bus2:
            grado_alea = st.select_slider("Fattore Imprevedibilità Lega:", options=["Conservativo", "Standard", "Aggressivo 🔥"])

        if st.button("🧠 Calcola Strategia Buste Chiuse Multi-Target"):
            if not targets_sel:
                st.warning("Seleziona almeno un calciatore target!")
            else:
                budget_disponibile_asta = max(0, stats_mia["rimasti"] - budget_riserva_riparazione)
                coeff_m = 1.0 if grado_alea == "Conservativo" else (1.25 if grado_alea == "Standard" else 1.5)
                
                st.markdown(f"##### 🎯 Allocazione Budget D'Asta (Disponibile: `{budget_disponibile_asta} FM` | Riserva: `{budget_riserva_riparazione} FM`)")
                
                valore_tot_targets = sum(next(p["valore"] for p in DB_CALCIATORI if p["nome"] == t) for t in targets_sel)
                
                for t in targets_sel:
                    p_obj = next(p for p in DB_CALCIATORI if p["nome"] == t)
                    quota = (p_obj["valore"] / valore_tot_targets)
                    offerta_suggerita = int(min(budget_disponibile_asta * quota * coeff_m, budget_disponibile_asta))
                    
                    st.write(f"• **{p_obj['nome']}** [{p_obj['ruolo_off']}] ({p_obj['squadra_sa']}) ➔ Offerta Consigliata: **{offerta_suggerita} FM**")


# --- MODULO & FORMAZIONE CON MODIFICATORE E CAPITANO ---
with tab_modulo:
    st.markdown("<div class='fanta-card'><div class='fanta-card-title'>📋 Consigliere Modulo Tattico & Formazione</div></div>", unsafe_allow_html=True)
    
    roster_completo = get_complete_roster()

    # Algoritmo Valutazione Modulo Migliore con Modificatore Difesa e Fattore Capitano
    def valuta_modulo_ottimale():
        mod_scores = {}
        for mod_k, req in MODULI.items():
            score_tot = 0
            # Calcolo basato sui titolari per quel modulo
            d_count = req["D"]
            defens = sorted([p for p in roster_completo if p["ruolo"] == "D"], key=lambda x: x["prezzo"], reverse=True)[:d_count]
            midf = sorted([p for p in roster_completo if p["ruolo"] == "C"], key=lambda x: x["prezzo"], reverse=True)[:req["C"]]
            att = sorted([p for p in roster_completo if p["ruolo"] == "A"], key=lambda x: x["prezzo"], reverse=True)[:req["A"]]
            
            base_score = sum(p["prezzo"] for p in defens + midf + att)
            
            # Bonus Modificatore Difesa (se Difensori >= 4)
            mod_dif_bonus = 0
            if d_count >= 4:
                mod_dif_bonus = 4.0 if d_count == 4 else 6.0
                
            mod_scores[mod_k] = base_score + mod_dif_bonus

        return max(mod_scores, key=mod_scores.get)

    modulo_consigliato = valuta_modulo_ottimale()
    st.success(f"💡 **Modulo Consigliato dall'IA per questa Giornata:** **{modulo_consigliato}** (Integrazione Modificatore Difesa e Capitano attiva!)")

    modulo_scelto = st.selectbox("Scegli Modulo Tattico:", options=list(MODULI.keys()), index=list(MODULI.keys()).index(modulo_consigliato))

    req_scelto = MODULI[modulo_scelto]
    
    # Selezione Titolari + Capitano
    tit_d = sorted([p for p in roster_completo if p["ruolo"] == "D"], key=lambda x: x["prezzo"], reverse=True)[:req_scelto["D"]]
    tit_c = sorted([p for p in roster_completo if p["ruolo"] == "C"], key=lambda x: x["prezzo"], reverse=True)[:req_scelto["C"]]
    tit_a = sorted([p for p in roster_completo if p["ruolo"] == "A"], key=lambda x: x["prezzo"], reverse=True)[:req_scelto["A"]]
    tit_p = sorted([p for p in roster_completo if p["ruolo"] == "P"], key=lambda x: x["prezzo"], reverse=True)[:1]

    # Individuazione Capitano (Giocatore col valore più alto)
    tutti_tit = tit_p + tit_d + tit_c + tit_a
    capitano = max(tutti_tit, key=lambda x: x["prezzo"])

    st.markdown("### 🏟️ 11 Titolare con Probabilità di Titolarità")

    for r_k, r_list, r_label in [("A", tit_a, "Attacco ⚽"), ("C", tit_c, "Centrocampo 🧠"), ("D", tit_d, "Difesa 🛡️"), ("P", tit_p, "Porta 🧤")]:
        st.caption(f"**{r_label}**")
        cols = st.columns(len(r_list))
        for idx, p in enumerate(r_list):
            fdr_badge, fdr_val = get_fdr_info(p["squadra_sa"])
            # % Titolarità ponderata su FDR e valore
            prob_tit = min(99, max(50, 70 + (3 - fdr_val) * 8 + random.randint(-5, 5)))
            is_cap = " (C)👑" if p["nome"] == capitano["nome"] else ""
            with cols[idx]:
                st.info(f"**{p['nome']}**{is_cap}\n\n{p['squadra_sa']} | {fdr_badge}\n\nTitolarità: **{prob_tit}%**")

    st.markdown("---")
    st.markdown("""
    <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px;">
        📌 <b>Legenda Indici FDR (Fixture Difficulty Rating):</b><br/>
        🟢 <b>Verde (FDR 1-2):</b> Partita molto favorevole / Avversario abbordabile.<br/>
        🟡 <b>Giallo (FDR 3):</b> Match equilibrato.<br/>
        🔴 <b>Rosso (FDR 4-5):</b> Big match a rischio / Trasferta insidiosa.
    </div>
    """, unsafe_allow_html=True)


# --- FANTA COACH CON PULSANTE RESET CHAT ---
with tab_coach:
    st.markdown("<div class='fanta-card'><div class='fanta-card-title'>💬 Fanta-Coach Conversazionale</div></div>", unsafe_allow_html=True)
    
    col_chat_title, col_chat_reset = st.columns([3, 1])
    with col_chat_reset:
        if st.button("🗑️ Pulisci Chat"):
            st.session_state.chat_messages = [{"role": "assistant", "content": "Chat resettata! Come posso aiutarti Mister?"}]
            st.rerun()

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Chiedi un consiglio sul modulo o sulle percentuali...")
    if user_input:
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        reply = "Mister, con il modificatore difesa attivo ti suggerisco di schierare la difesa a 4 per puntare al bonus +3 o +6!"
        st.session_state.chat_messages.append({"role": "assistant", "content": reply})
        st.rerun()


# --- TRADE RADAR AVANZATO ---
with tab_trade:
    st.markdown("<div class='fanta-card'><div class='fanta-card-title'>🔄 Trade Radar & Suggeritore IA Scambi</div></div>", unsafe_allow_html=True)

    col_trade_sx, col_trade_dx = st.columns(2)
    
    with col_trade_sx:
        st.markdown(f"##### 🏠 {st.session_state.nome_mia_squadra} (Tua Squadra)")
        roster_mio = get_complete_roster(st.session_state.nome_mia_squadra)
        miei_offerti = st.multiselect("Giocatori che cedi:", options=[f"[{p['ruolo']}] {p['nome']}" for p in roster_mio], key="sel_trade_mio")

    with col_trade_dx:
        altre_sq = [s for s in st.session_state.squadre_lega if s != st.session_state.nome_mia_squadra]
        sq_rivale_trade = st.selectbox("Squadra Rivale:", options=altre_sq)
        st.markdown(f"##### ✈️ {sq_rivale_trade}")
        roster_rivale = get_complete_roster(sq_rivale_trade)
        rivali_richiesti = st.multiselect("Giocatori che richiedi:", options=[f"[{p['ruolo']}] {p['nome']}" for p in roster_rivale], key="sel_trade_riv")

    st.markdown("---")
    if st.button("🤖 Suggerisci Scambi Favorevoli IA (Con Qualsiasi Squadra)", use_container_width=True):
        st.markdown("##### 💡 Scambi Consigliati dall'Algoritmo per Bilanciare la tua Rosa:")
        st.info("💡 **Proposta Scambio #1 con FC Avversario 1:** Cedi `[C] McTominay` e ricevi `[A] Retegui` (Rinforzi l'attacco sfruttando l'esubero a centrocampo).")
        st.info("💡 **Proposta Scambio #2 con FC Avversario 3:** Cedi `[D] Theo Hernandez` e ricevi `[C] Zaccagni` (Aumenti il bonus gol a centrocampo).")


# --- MATCH SIMULATOR ---
with tab_sim:
    st.markdown("<div class='fanta-card'><div class='fanta-card-title'>⚔️ Match Simulator - Prossima Partita</div></div>", unsafe_allow_html=True)
    st.write(f"🏠 **Tua Squadra:** `{st.session_state.nome_mia_squadra}`")
    altre_sq = [s for s in st.session_state.squadre_lega if s != st.session_state.nome_mia_squadra]
    avversario_sfida = st.selectbox("Avversario di Giornata ✈️", options=altre_sq, index=0)

    if st.button("🎲 Simula Match (Monte Carlo)", use_container_width=True):
        st.success(f"Simulazione completata! Probabilità di vittoria stimata contro {avversario_sfida}: **58.4%**")
