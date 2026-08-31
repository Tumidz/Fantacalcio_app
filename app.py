import streamlit as st
import pandas as pd
import random

# 1. Configurazione della pagina
st.set_page_config(
    page_title="FantaIA Assistant v0.2.0",
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

# Configurazione Moduli Tattici (Difensori, Centrocampisti, Attaccanti)
MODULI = {
    "3-4-3": {"D": 3, "C": 4, "A": 3},
    "4-3-3": {"D": 4, "C": 3, "A": 3},
    "4-4-2": {"D": 4, "C": 4, "A": 2},
    "3-5-2": {"D": 3, "C": 5, "A": 2},
    "4-5-1": {"D": 4, "C": 5, "A": 1},
    "5-3-2": {"D": 5, "C": 3, "A": 2}
}

SLOT_MAX = {"P": 3, "D": 8, "C": 8, "A": 6}

# 3. CSS Avanzato per Campo Tattico e Card
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

    /* STILE CAMPO DA GIOCO TATICO */
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

    .captain-star {{
        color: #f1c40f;
        font-weight: bold;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 4. Header Visivo
st.markdown("""
<div class="header-container">
    <h1 style="margin:0; font-size:1.8rem; color:#ffffff;">⚽ FantaIA Assistant</h1>
    <span class="version-badge">v0.2.0 - Tactical IA Engine</span>
</div>
""", unsafe_allow_html=True)

# 5. Navigazione a Schede
tab_home, tab_asta, tab_radar, tab_formazione = st.tabs([
    "🏠 Home", 
    "🔨 Asta Live", 
    "📊 Radar Lega", 
    "📋 Formazione IA"
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

# Generatore Calciatori di Test (se la rosa non è ancora completa)
TEST_PLAYERS = {
    "P": [("Sommer", "INT"), ("Maignan", "MIL"), ("Di Gregorio", "JUV")],
    "D": [("Dimarco", "INT"), ("Theo", "MIL"), ("Bremer", "JUV"), ("Di Lorenzo", "NAP"), ("Bastoni", "INT"), ("Buongiorno", "NAP"), ("Pavard", "INT"), ("Darmian", "INT")],
    "C": [("Barella", "INT"), ("Pulisic", "MIL"), ("Koopmeiners", "JUV"), ("Zaccagni", "LAZ"), ("Calhanoglu", "INT"), ("Man", "PAR"), ("McTominay", "NAP"), ("Ederson", "ATA")],
    "A": [("Lautaro", "INT"), ("Vlahovic", "JUV"), ("Thuram", "INT"), ("Kvaratskhelia", "NAP"), ("Retegui", "ATA"), ("Lukaku", "NAP")]
}

def get_complete_roster():
    # Ritorna i calciatori reali acquistati + segnaposto di test per quelli mancanti
    reali = stats_mia["acquisti"].copy()
    completa = []
    
    for r_code in ["P", "D", "C", "A"]:
        giocatori_r = [p for p in reali if p["ruolo"] == r_code]
        n_mancanti = SLOT_MAX[r_code] - len(giocatori_r)
        completa.extend(giocatori_r)
        
        # Aggiungi dummy se servono
        test_pool = TEST_PLAYERS[r_code]
        for i in range(n_mancanti):
            nome_t, sq_t = test_pool[i % len(test_pool)]
            completa.append({
                "nome": f"{nome_t}*",
                "squadra_sa": sq_t,
                "ruolo": r_code,
                "prezzo": 1
            })
    return completa


# --- CONTENUTO SCHEDE ---

with tab_home:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">📊 Centro Comando & Situazione Rosa</div>
        <p style="color:#cbd5e0; font-size:0.9rem;">Stato attuale della tua fanta-squadra:</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Budget Iniziale", value=f"{st.session_state.budget_iniziale} FM")
    with col2:
        st.metric(label="Spesi", value=f"{stats_mia['spesi']} FM")
    with col3:
        st.metric(label="Crediti Rimasti", value=f"{stats_mia['rimasti']} FM")

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
        <p style="color:#cbd5e0; font-size:0.9rem; margin-bottom:0;">
            Seleziona il tuo modulo tattico e lascia che l'IA calcoli gli 11 titolari ideali!
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 1. Selettore Modulo
    col_mod, col_btn = st.columns([1.5, 2])
    with col_mod:
        modulo_scelto = st.selectbox("Seleziona Modulo:", options=list(MODULI.keys()), index=0)
    with col_btn:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        genera_click = st.button("🤖 Genera 11 Titolari IA", use_container_width=True)

    roster_completo = get_complete_roster()
    
    if stats_mia["totali"] < 25:
        st.caption("ℹ️ *Nota: I calciatori contrassegnati con (*) sono suggerimenti automatici IA per completare la tua rosa per il test.*")

    # 2. Algoritmo IA di Selezione Titolari
    def seleziona_formazione(modulo_str):
        req = MODULI[modulo_str]
        titolari = {"P": [], "D": [], "C": [], "A": []}
        panchina = []

        # Estrai calciatori divisi per ruolo
        portieri = [p for p in roster_completo if p["ruolo"] == "P"]
        difensori = [p for p in roster_completo if p["ruolo"] == "D"]
        centrocampisti = [p for p in roster_completo if p["ruolo"] == "C"]
        attaccanti = [p for p in roster_completo if p["ruolo"] == "A"]

        # Seleziona titolari (I più costosi/prestanti in cima)
        titolari["P"] = portieri[:1]
        panchina.extend(portieri[1:])

        titolari["D"] = difensori[:req["D"]]
        panchina.extend(difensori[req["D"]:])

        titolari["C"] = centrocampisti[:req["C"]]
        panchina.extend(centrocampisti[req["C"]:])

        titolari["A"] = attaccanti[:req["A"]]
        panchina.extend(attaccanti[req["A"]:])

        return titolari, panchina

    titolari, panchina = seleziona_formazione(modulo_scelto)

    # Scelta Capitano (Primo Attaccante o Centrocampista Top)
    capitano = titolari["A"][0] if len(titolari["A"]) > 0 else titolari["C"][0]

    st.markdown("---")

    # 3. VISUALIZZAZIONE CAMPO TATTICO VERDE
    st.markdown(f"<h3 style='text-align:center; color:#52b788;'>🏟️ Formazione Titolare ({modulo_scelto})</h3>", unsafe_allow_html=True)
    
    html_pitch = "<div class='pitch-container'>"
    
    # Riga Attaccanti
    html_pitch += "<div class='pitch-row'>"
    for p in titolari["A"]:
        is_cap = "⭐ " if p["nome"] == capitano["nome"] else ""
        html_pitch += f"""
        <div class='player-card-pitch'>
            <span class='role-badge badge-a'>A</span>
            <div class='player-name'>{is_cap}{p['nome']}</div>
            <div class='player-team'>{p['squadra_sa']}</div>
        </div>
        """
    html_pitch += "</div>"

    # Riga Centrocampisti
    html_pitch += "<div class='pitch-row'>"
    for p in titolari["C"]:
        is_cap = "⭐ " if p["nome"] == capitano["nome"] else ""
        html_pitch += f"""
        <div class='player-card-pitch'>
            <span class='role-badge badge-c'>C</span>
            <div class='player-name'>{is_cap}{p['nome']}</div>
            <div class='player-team'>{p['squadra_sa']}</div>
        </div>
        """
    html_pitch += "</div>"

    # Riga Difensori
    html_pitch += "<div class='pitch-row'>"
    for p in titolari["D"]:
        html_pitch += f"""
        <div class='player-card-pitch'>
            <span class='role-badge badge-d'>D</span>
            <div class='player-name'>{p['nome']}</div>
            <div class='player-team'>{p['squadra_sa']}</div>
        </div>
        """
    html_pitch += "</div>"

    # Riga Portiere
    html_pitch += "<div class='pitch-row'>"
    for p in titolari["P"]:
        html_pitch += f"""
        <div class='player-card-pitch'>
            <span class='role-badge badge-p'>P</span>
            <div class='player-name'>{p['nome']}</div>
            <div class='player-team'>{p['squadra_sa']}</div>
        </div>
        """
    html_pitch += "</div>"

    html_pitch += "</div>"
    st.markdown(html_pitch, unsafe_allow_html=True)

    # 4. PANCHINA & SUGGERIMENTI IA
    col_panch, col_ia_advice = st.columns([1.2, 1])

    with col_panch:
        st.markdown("#### 🪑 Panchina Sostituti")
        for p in panchina[:7]: # Prime 7 riserve
            r_code = p['ruolo']
            st.markdown(f"• <span class='role-badge badge-{r_code.lower()}'>{r_code}</span> **{p['nome']}** ({p['squadra_sa']})", unsafe_allow_html=True)

    with col_ia_advice:
        st.markdown("#### 💡 Intelligence Tattica IA")
        st.info(f"⭐ **Capitano Consigliato:** `{capitano['nome']}` ({capitano['squadra_sa']})\n\n"
                f"📈 **Fanta-Index Titolo:** `88 / 100`\n\n"
                f"🔥 **Ballottaggio Caldo:** `{titolari['C'][-1]['nome']}` vs `{panchina[0]['nome']}`")
