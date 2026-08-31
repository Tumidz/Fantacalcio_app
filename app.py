# Requisiti: streamlit>=1.32, pandas, requests
# pip install --upgrade streamlit pandas requests
from datetime import datetime
import random
import pandas as pd
import requests
import streamlit as st

# 1. Configurazione Pagina
st.set_page_config(
    page_title="FantaIA Assistant v1.0.0",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Immagine di sfondo: stadio visto dall'interno (spalti/pubblico), licenza Unsplash gratuita.
URL_SFONDO_STADIO = "https://images.unsplash.com/photo-1675886051953-c4ffa7556b63?fm=jpg&q=80&w=1920&auto=format&fit=crop"

# ---------------------------------------------------------------------------
# SQUADRE DI SERIE A
# ---------------------------------------------------------------------------
SQUADRE_SERIE_A_2026_27 = {
    "ATA": "Atalanta",
    "BOL": "Bologna",
    "CAG": "Cagliari",
    "COM": "Como",
    "FIO": "Fiorentina",
    "FRO": "Frosinone",
    "GEN": "Genoa",
    "INT": "Inter",
    "JUV": "Juventus",
    "LAZ": "Lazio",
    "LEC": "Lecce",
    "MIL": "Milan",
    "MON": "Monza",
    "NAP": "Napoli",
    "PAR": "Parma",
    "ROM": "Roma",
    "SAS": "Sassuolo",
    "TOR": "Torino",
    "UDI": "Udinese",
    "VEN": "Venezia",
}


def codice_da_nome_squadra(nome_squadra):
    for codice, nome in SQUADRE_SERIE_A_2026_27.items():
        if nome == nome_squadra:
            return codice
    return nome_squadra[:3].upper()


ROLE_ORDER = {"P": 0, "D": 1, "C": 2, "A": 3}

# DATABASE CALCIATORI DI ESEMPIO (fallback quando non è collegata una chiave API-FOOTBALL valida)
DB_CALCIATORI_DEFAULT = [
    # INTER
    {"nome": "Lautaro Martinez", "squadra_sa": "INT", "ruolo_off": "A", "valore": 88},
    {"nome": "Marcus Thuram", "squadra_sa": "INT", "ruolo_off": "A", "valore": 68},
    {"nome": "Mehdi Taremi", "squadra_sa": "INT", "ruolo_off": "A", "valore": 35},
    {"nome": "Hakan Calhanoglu", "squadra_sa": "INT", "ruolo_off": "C", "valore": 48},
    {"nome": "Nicolò Barella", "squadra_sa": "INT", "ruolo_off": "C", "valore": 38},
    {"nome": "Federico Dimarco", "squadra_sa": "INT", "ruolo_off": "D", "valore": 42},
    {"nome": "Yann Sommer", "squadra_sa": "INT", "ruolo_off": "P", "valore": 26},
    # JUVENTUS
    {"nome": "Dusan Vlahovic", "squadra_sa": "JUV", "ruolo_off": "A", "valore": 82},
    {"nome": "Francisco Conceição", "squadra_sa": "JUV", "ruolo_off": "A", "valore": 38},
    {"nome": "Nico Gonzalez", "squadra_sa": "JUV", "ruolo_off": "A", "valore": 42},
    {"nome": "Teun Koopmeiners", "squadra_sa": "JUV", "ruolo_off": "C", "valore": 52},
    {"nome": "Douglas Luiz", "squadra_sa": "JUV", "ruolo_off": "C", "valore": 35},
    {"nome": "Gleison Bremer", "squadra_sa": "JUV", "ruolo_off": "D", "valore": 34},
    {"nome": "Michele Di Gregorio", "squadra_sa": "JUV", "ruolo_off": "P", "valore": 25},
    # MILAN
    {"nome": "Alvaro Morata", "squadra_sa": "MIL", "ruolo_off": "A", "valore": 65},
    {"nome": "Rafael Leao", "squadra_sa": "MIL", "ruolo_off": "A", "valore": 72},
    {"nome": "Christian Pulisic", "squadra_sa": "MIL", "ruolo_off": "C", "valore": 50},
    {"nome": "Tijjani Reijnders", "squadra_sa": "MIL", "ruolo_off": "C", "valore": 32},
    {"nome": "Theo Hernandez", "squadra_sa": "MIL", "ruolo_off": "D", "valore": 38},
    {"nome": "Mike Maignan", "squadra_sa": "MIL", "ruolo_off": "P", "valore": 25},
    # NAPOLI
    {"nome": "Romelu Lukaku", "squadra_sa": "NAP", "ruolo_off": "A", "valore": 78},
    {"nome": "Khvicha Kvaratskhelia", "squadra_sa": "NAP", "ruolo_off": "A", "valore": 75},
    {"nome": "David Neres", "squadra_sa": "NAP", "ruolo_off": "A", "valore": 40},
    {"nome": "Scott McTominay", "squadra_sa": "NAP", "ruolo_off": "C", "valore": 36},
    {"nome": "Alessandro Buongiorno", "squadra_sa": "NAP", "ruolo_off": "D", "valore": 30},
    {"nome": "Giovanni Di Lorenzo", "squadra_sa": "NAP", "ruolo_off": "D", "valore": 24},
    {"nome": "Alex Meret", "squadra_sa": "NAP", "ruolo_off": "P", "valore": 20},
    # ATALANTA
    {"nome": "Mateo Retegui", "squadra_sa": "ATA", "ruolo_off": "A", "valore": 68},
    {"nome": "Ademola Lookman", "squadra_sa": "ATA", "ruolo_off": "A", "valore": 64},
    {"nome": "Charles De Ketelaere", "squadra_sa": "ATA", "ruolo_off": "A", "valore": 48},
    {"nome": "Lazar Samardzic", "squadra_sa": "ATA", "ruolo_off": "C", "valore": 32},
    {"nome": "Ederson", "squadra_sa": "ATA", "ruolo_off": "C", "valore": 28},
    {"nome": "Marco Carnesecchi", "squadra_sa": "ATA", "ruolo_off": "P", "valore": 22},
    # ROMA
    {"nome": "Artem Dovbyk", "squadra_sa": "ROM", "ruolo_off": "A", "valore": 70},
    {"nome": "Paulo Dybala", "squadra_sa": "ROM", "ruolo_off": "A", "valore": 60},
    {"nome": "Matias Soulé", "squadra_sa": "ROM", "ruolo_off": "A", "valore": 42},
    {"nome": "Manu Koné", "squadra_sa": "ROM", "ruolo_off": "C", "valore": 24},
    {"nome": "Mile Svilar", "squadra_sa": "ROM", "ruolo_off": "P", "valore": 22},
    # LAZIO
    {"nome": "Taty Castellanos", "squadra_sa": "LAZ", "ruolo_off": "A", "valore": 46},
    {"nome": "Boulaye Dia", "squadra_sa": "LAZ", "ruolo_off": "A", "valore": 36},
    {"nome": "Mattia Zaccagni", "squadra_sa": "LAZ", "ruolo_off": "C", "valore": 40},
    {"nome": "Ivan Provedel", "squadra_sa": "LAZ", "ruolo_off": "P", "valore": 18},
    # FIORENTINA
    {"nome": "Moise Kean", "squadra_sa": "FIO", "ruolo_off": "A", "valore": 52},
    {"nome": "Albert Gudmundsson", "squadra_sa": "FIO", "ruolo_off": "A", "valore": 55},
    {"nome": "Andrea Colpani", "squadra_sa": "FIO", "ruolo_off": "C", "valore": 30},
    {"nome": "David De Gea", "squadra_sa": "FIO", "ruolo_off": "P", "valore": 20},
]

CALENDARIO_SERIE_A_ESEMPIO = {
    "INT": {"opp": "VEN", "fdr": 1, "casa": True},
    "MIL": {"opp": "JUV", "fdr": 4, "casa": False},
    "JUV": {"opp": "MIL", "fdr": 4, "casa": True},
    "NAP": {"opp": "GEN", "fdr": 2, "casa": True},
    "ATA": {"opp": "ROM", "fdr": 3, "casa": False},
    "LAZ": {"opp": "FIO", "fdr": 3, "casa": True},
    "PAR": {"opp": "MON", "fdr": 2, "casa": False},
    "ROM": {"opp": "ATA", "fdr": 3, "casa": True},
    "FIO": {"opp": "LAZ", "fdr": 3, "casa": False},
    "TOR": {"opp": "CAG", "fdr": 2, "casa": True},
}


def get_fdr_info(squadra_sa):
    info = CALENDARIO_SERIE_A_ESEMPIO.get(
        squadra_sa, {"opp": "N/D", "fdr": 3, "casa": True}
    )
    loc = "vs" if info["casa"] else "@"
    fdr = info["fdr"]
    badge = "🟢" if fdr <= 2 else ("🟡" if fdr == 3 else "🔴")
    return f"{loc} {info['opp']} {badge}", fdr


# ---------------------------------------------------------------------------
# INTEGRAZIONE API-FOOTBALL
# ---------------------------------------------------------------------------
LEGA_SERIE_A_ID = 135
STAGIONE_CORRENTE = 2025  # Anno d'inizio stagione valido su API-Football
API_BASE_URL = "https://v3.football.api-sports.io"

MAPPA_SQUADRE_API = {
    "Atalanta": "ATA", "Bologna": "BOL", "Cagliari": "CAG", "Como": "COM",
    "Fiorentina": "FIO", "Frosinone": "FRO", "Genoa": "GEN", "Inter": "INT",
    "Juventus": "JUV", "Lazio": "LAZ", "Lecce": "LEC", "AC Milan": "MIL",
    "Milan": "MIL", "Monza": "MON", "Napoli": "NAP", "Parma": "PAR",
    "AS Roma": "ROM", "Roma": "ROM", "Sassuolo": "SAS", "Torino": "TOR",
    "Udinese": "UDI", "Venezia": "VEN",
}

RUOLO_DA_POSIZIONE_API = {
    "Goalkeeper": "P",
    "Defender": "D",
    "Midfielder": "C",
    "Attacker": "A",
}

VALORE_BASE_PER_RUOLO = {"P": 20, "D": 26, "C": 32, "A": 42}


def ottieni_api_key():
    chiave_da_secrets = ""
    try:
        chiave_da_secrets = st.secrets.get("API_FOOTBALL_KEY", "")
    except Exception:
        chiave_da_secrets = ""
    return st.session_state.get("api_key_manuale", "") or chiave_da_secrets


@st.cache_data(
    ttl=86400, show_spinner="🔄 Sincronizzazione rose reali di Serie A..."
)
def scarica_calciatori_da_api(api_key, stagione):
    """Scarica le rose reali di tutte le squadre di Serie A da API-FOOTBALL."""
    intestazioni = {"x-apisports-key": api_key}
    try:
        risposta_squadre = requests.get(
            f"{API_BASE_URL}/teams",
            headers=intestazioni,
            params={"league": LEGA_SERIE_A_ID, "season": stagione},
            timeout=15,
        )
        risposta_squadre.raise_for_status()
        res_json = risposta_squadre.json()
        
        # Gestione errori ritornati direttamente dall'API
        if res_json.get("errors"):
            st.error(f"⚠️ Errore risposta API: {res_json['errors']}")
            return None

        dati_squadre = res_json.get("response", [])
        if not dati_squadre:
            st.warning(f"⚠️ Nessuna squadra trovata per la stagione {stagione}. Prova a verificare l'anno della stagione nell'API.")
            return None

    except requests.RequestException as e:
        st.error(f"⚠️ Errore di connessione API: {e}")
        return None

    calciatori_totali = []
    for voce in dati_squadre:
        squadra_info = voce.get("team", {})
        team_id = squadra_info.get("id")
        nome_squadra = squadra_info.get("name", "")
        if not team_id:
            continue
        codice = MAPPA_SQUADRE_API.get(nome_squadra, nome_squadra[:3].upper())

        try:
            risposta_rosa = requests.get(
                f"{API_BASE_URL}/players/squads",
                headers=intestazioni,
                params={"team": team_id},
                timeout=15,
            )
            risposta_rosa.raise_for_status()
            dati_rosa = risposta_rosa.json().get("response", [])
        except requests.RequestException:
            continue

        if not dati_rosa:
            continue

        for giocatore in dati_rosa[0].get("players", []):
            ruolo = RUOLO_DA_POSIZIONE_API.get(giocatore.get("position", ""), "C")
            calciatori_totali.append({
                "nome": giocatore.get("name", "Sconosciuto"),
                "squadra_sa": codice,
                "ruolo_off": ruolo,
                "valore": VALORE_BASE_PER_RUOLO[ruolo],
                "player_id": giocatore.get("id"),
            })

    return calciatori_totali or None


@st.cache_data(ttl=604800, show_spinner="📊 Recupero statistiche giocatore...")
def scarica_statistiche_giocatore(player_id, api_key, numero_stagioni=6):
    """Statistiche stagione per stagione, filtrate alla sola Serie A."""
    intestazioni = {"x-apisports-key": api_key}
    righe = []
    for anno in range(STAGIONE_CORRENTE, STAGIONE_CORRENTE - numero_stagioni, -1):
        try:
            risposta = requests.get(
                f"{API_BASE_URL}/players",
                headers=intestazioni,
                params={"id": player_id, "season": anno},
                timeout=15,
            )
            risposta.raise_for_status()
            dati = risposta.json().get("response", [])
        except requests.RequestException:
            continue

        if not dati:
            continue

        for blocco in dati[0].get("statistics", []):
            if blocco.get("league", {}).get("id") != LEGA_SERIE_A_ID:
                continue
            righe.append({
                "Stagione": f"{anno}/{str(anno + 1)[-2:]}",
                "Squadra": blocco.get("team", {}).get("name", "—"),
                "Presenze": blocco.get("games", {}).get("appearences") or 0,
                "Gol": blocco.get("goals", {}).get("total") or 0,
                "Assist": blocco.get("goals", {}).get("assists") or 0,
                "Ammonizioni": blocco.get("cards", {}).get("yellow") or 0,
                "Espulsioni": blocco.get("cards", {}).get("red") or 0,
            })

    if not righe:
        return None
    return pd.DataFrame(righe)


# 2. INIZIALIZZAZIONE SESSION STATE
if "db_calciatori" not in st.session_state:
    st.session_state.db_calciatori = DB_CALCIATORI_DEFAULT.copy()

if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now().strftime("%d/%m/%Y - %H:%M") + " CEST"

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
        "FC Avversario 7",
    ]

if "tutti_acquisti" not in st.session_state:
    st.session_state.tutti_acquisti = []

if "custom_ruoli" not in st.session_state:
    st.session_state.custom_ruoli = {}

if "custom_valori" not in st.session_state:
    st.session_state.custom_valori = {}

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": (
                "Ciao Mister! Sono il tuo Fanta-Coach IA. Chiedimi qualsiasi"
                " consiglio!"
            ),
        }
    ]

if "dati_live_tentati" not in st.session_state:
    st.session_state.dati_live_tentati = False

_chiave_avvio = ottieni_api_key()
if _chiave_avvio and not st.session_state.dati_live_tentati:
    _nuovi_calciatori = scarica_calciatori_da_api(_chiave_avvio, STAGIONE_CORRENTE)
    if _nuovi_calciatori:
        st.session_state.db_calciatori = _nuovi_calciatori
        st.session_state.last_update = (
            datetime.now().strftime("%d/%m/%Y - %H:%M") + " CEST"
        )
    st.session_state.dati_live_tentati = True

MODULI = {
    "3-4-3": {"D": 3, "C": 4, "A": 3},
    "4-3-3": {"D": 4, "C": 3, "A": 3},
    "4-4-2": {"D": 4, "C": 4, "A": 2},
    "3-5-2": {"D": 3, "C": 5, "A": 2},
    "4-5-1": {"D": 4, "C": 5, "A": 1},
    "5-3-2": {"D": 5, "C": 3, "A": 2},
}

SLOT_MAX = {"P": 3, "D": 8, "C": 8, "A": 6}


def get_ruolo_effettivo(nome_giocatore, ruolo_default="C"):
    return st.session_state.custom_ruoli.get(nome_giocatore, ruolo_default)


def get_valore_effettivo(nome_giocatore, valore_default=30):
    return st.session_state.custom_valori.get(nome_giocatore, valore_default)


def costruisci_opzioni_giocatori(lista_calciatori):
    arricchiti = []
    for p in lista_calciatori:
        ruolo_disp = get_ruolo_effettivo(p["nome"], p["ruolo_off"])
        valore_disp = get_valore_effettivo(p["nome"], p["valore"])
        etichetta = f"[{ruolo_disp}] {p['nome']} ({p['squadra_sa']})"
        arricchiti.append({
            **p,
            "ruolo_disp": ruolo_disp,
            "valore_disp": valore_disp,
            "etichetta": etichetta,
        })
    arricchiti.sort(key=lambda x: (ROLE_ORDER.get(x["ruolo_disp"], 9), x["nome"]))
    return arricchiti


# 3. CSS
st.markdown(
    f"""
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
""",
    unsafe_allow_html=True,
)

# 4. Header & Stato Sincronizzazione Dati
_chiave_attiva = ottieni_api_key()
_badge_stato = "🟢 Dati Live (API)" if _chiave_attiva else "🟡 Modalità Demo"
st.markdown(
    f"""
<div class="header-container">
    <h1 style="margin:0; font-size:1.8rem; color:#ffffff;">⚽ FantaIA Assistant</h1>
    <span style="background:#52b788; color:#081c15; font-weight:bold; padding:4px 12px; border-radius:12px; font-size:0.8rem;">
        v1.0.0 - {_badge_stato} - Ultimo agg.: {st.session_state.last_update}
    </span>
</div>
""",
    unsafe_allow_html=True,
)

col_sync1, col_sync2 = st.columns([2, 1])
with col_sync2:
    if st.button("🔄 Aggiorna Dati IA Ora", use_container_width=True):
        chiave = ottieni_api_key()
        if chiave:
            scarica_calciatori_da_api.clear()
            nuovi_calciatori = scarica_calciatori_da_api(chiave, STAGIONE_CORRENTE)
            if nuovi_calciatori:
                st.session_state.db_calciatori = nuovi_calciatori
                st.session_state.last_update = (
                    datetime.now().strftime("%d/%m/%Y - %H:%M") + " CEST"
                )
                st.success(
                    f"Rose aggiornate da API-FOOTBALL: {len(nuovi_calciatori)}"
                    " calciatori trovati."
                )
            else:
                st.warning(
                    "Impossibile scaricare i dati dall'API. Verificare la chiave"
                    " o i limiti del piano."
                )
        else:
            st.session_state.db_calciatori = DB_CALCIATORI_DEFAULT.copy()
            st.session_state.last_update = (
                datetime.now().strftime("%d/%m/%Y - %H:%M") + " CEST"
            )
            st.info(
                "Nessuna chiave API configurata: ripristinati i dati di esempio"
                " (modalità demo)."
            )
        st.rerun()

with st.expander("🔌 Connessione Dati Live (API-FOOTBALL)"):
    st.caption(
        "Per rose sempre aggiornate in automatico, crea una chiave gratuita"
        " su dashboard.api-football.com (piano Free: 100 richieste/giorno) e"
        " incollala qui sotto. Senza chiave l'app resta in modalità demo con"
        " i dati di esempio. Per non doverla reinserire ogni volta, puoi"
        " salvarla in modo permanente in .streamlit/secrets.toml come"
        " API_FOOTBALL_KEY."
    )
    _valore_input_chiave = st.text_input(
        "Chiave API-FOOTBALL",
        value=st.session_state.get("api_key_manuale", ""),
        type="password",
        key="api_key_input_widget",
    )
    if _valore_input_chiave != st.session_state.get("api_key_manuale", ""):
        st.session_state.api_key_manuale = _valore_input_chiave
        st.session_state.dati_live_tentati = False
        st.rerun()

# 5. Navigazione Schede
(
    tab_home,
    tab_asta,
    tab_ruoli,
    tab_modulo,
    tab_giocatori,
    tab_coach,
    tab_trade,
    tab_sim,
) = st.tabs([
    "🏠 Home",
    "🔨 Asta",
    "🎭 Ruoli & Valori",
    "📋 Modulo",
    "📚 Calciatori",
    "💬 Fanta-Coach",
    "🔄 Trade",
    "⚔️ Match Simulator",
])


def get_stats_squadra(nome_squadra):
    acquisti = [
        p
        for p in st.session_state.tutti_acquisti
        if p["fantasquadra"] == nome_squadra
    ]
    spesi = sum(p["prezzo"] for p in acquisti)
    rimasti = st.session_state.budget_iniziale - spesi
    return {
        "acquisti": acquisti,
        "spesi": spesi,
        "rimasti": rimasti,
        "P": sum(1 for p in acquisti if get_ruolo_effettivo(p["nome"], p["ruolo"]) == "P"),
        "D": sum(1 for p in acquisti if get_ruolo_effettivo(p["nome"], p["ruolo"]) == "D"),
        "C": sum(1 for p in acquisti if get_ruolo_effettivo(p["nome"], p["ruolo"]) == "C"),
        "A": sum(1 for p in acquisti if get_ruolo_effettivo(p["nome"], p["ruolo"]) == "A"),
        "totali": len(acquisti),
    }


stats_mia = get_stats_squadra(st.session_state.nome_mia_squadra)


def get_complete_roster(nome_squadra=None):
    if nome_squadra is None:
        nome_squadra = st.session_state.nome_mia_squadra

    reali = [
        p
        for p in st.session_state.tutti_acquisti
        if p["fantasquadra"] == nome_squadra
    ]
    completa = []

    for p in reali:
        r_eff = get_ruolo_effettivo(p["nome"], p["ruolo"])
        completa.append({
            "nome": p["nome"],
            "squadra_sa": p.get("squadra_sa", "INT"),
            "ruolo": r_eff,
            "prezzo": p["prezzo"],
        })

    for r_code in ["P", "D", "C", "A"]:
        presenti = [p for p in completa if p["ruolo"] == r_code]
        mancanti = SLOT_MAX[r_code] - len(presenti)
        for i in range(mancanti):
            pool = [
                p for p in st.session_state.db_calciatori if p["ruolo_off"] == r_code
            ]
            if not pool:
                continue
            p_ref = pool[i % len(pool)]
            completa.append({
                "nome": f"{p_ref['nome']} (Bozza)",
                "squadra_sa": p_ref["squadra_sa"],
                "ruolo": r_code,
                "prezzo": random.randint(10, 30),
            })
    return completa


# --- HOME & GESTIONE ROSA ---
with tab_home:
    st.markdown(
        "<div class='fanta-card'><div class='fanta-card-title'>📊 Situazione"
        " Mia Rosa</div></div>",
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    c1.metric("Budget Iniziale", f"{st.session_state.budget_iniziale} FM")
    c2.metric("Spesi", f"{stats_mia['spesi']} FM")
    c3.metric("Crediti Rimasti", f"{stats_mia['rimasti']} FM")

    st.markdown("---")
    st.subheader("⚙️ Modifica & Cancellazione Rosa")
    if not stats_mia["acquisti"]:
        st.info(
            "Non hai ancora acquistato calciatori. Usa la scheda Asta per"
            " aggiungerne!"
        )
    else:
        for idx_vista, p in enumerate(stats_mia["acquisti"]):
            r_curr = get_ruolo_effettivo(p["nome"], p["ruolo"])
            col_info, col_mod_r, col_del = st.columns([2, 1, 1])
            with col_info:
                st.write(
                    f"**[{r_curr}]** {p['nome']} ({p['squadra_sa']}) - `{p['prezzo']} FM`"
                )
            with col_mod_r:
                nuovo_r = st.selectbox(
                    "Ruolo",
                    ["P", "D", "C", "A"],
                    index=["P", "D", "C", "A"].index(r_curr),
                    key=f"r_sel_{idx_vista}",
                )
                if nuovo_r != r_curr:
                    st.session_state.custom_ruoli[p["nome"]] = nuovo_r
                    st.rerun()
            with col_del:
                if st.button("🗑️ Elimina", key=f"del_p_{idx_vista}"):
                    indice_reale = st.session_state.tutti_acquisti.index(p)
                    st.session_state.tutti_acquisti.pop(indice_reale)
                    st.rerun()

        if st.button("🚨 Reset Completo Mia Rosa", type="primary"):
            st.session_state.tutti_acquisti = [
                p
                for p in st.session_state.tutti_acquisti
                if p["fantasquadra"] != st.session_state.nome_mia_squadra
            ]
            st.rerun()


# --- ASTA ---
with tab_asta:
    st.markdown(
        "<div class='fanta-card'><div class='fanta-card-title'>🔨 Gestione"
        " Asta</div></div>",
        unsafe_allow_html=True,
    )

    tipo_asta = st.radio(
        "Seleziona Modalità:",
        ["🔴 Chiamata / Live", "✉️ Busta Chiusa (Full IA)"],
        horizontal=True,
    )

    opzioni_giocatori = costruisci_opzioni_giocatori(st.session_state.db_calciatori)
    etichette_giocatori = [p["etichetta"] for p in opzioni_giocatori]
    mappa_giocatori = {p["etichetta"]: p for p in opzioni_giocatori}

    if tipo_asta == "🔴 Chiamata / Live":
        scelta_g = st.selectbox(
            "Cerca o Seleziona Calciatore:",
            options=etichette_giocatori,
            index=None,
            placeholder="🔍 Seleziona un giocatore...",
            key="live_sel",
        )

        if not scelta_g:
            st.info("Seleziona un calciatore dalla lista per registrare un'aggiudicazione.")
        else:
            p_sel = mappa_giocatori[scelta_g]

            with st.form("form_asta_live_auto", clear_on_submit=True):
                f_sq = st.selectbox(
                    "Acquirente Fanta-Lega:", options=st.session_state.squadre_lega
                )
                col_a1, col_a2 = st.columns(2)
                col_a1.text_input("Giocatore", value=p_sel["nome"], disabled=True)
                col_a2.text_input(
                    "Ruolo & Squadra",
                    value=f"{p_sel['ruolo_disp']} | {p_sel['squadra_sa']}",
                    disabled=True,
                )
                prezzo_asta = st.number_input(
                    "Prezzo d'Asta Finale (FM):", min_value=1, value=1
                )

                if st.form_submit_button("✅ Registra Aggiudicazione"):
                    st.session_state.tutti_acquisti.append({
                        "fantasquadra": f_sq,
                        "nome": p_sel["nome"],
                        "squadra_sa": p_sel["squadra_sa"],
                        "ruolo": p_sel["ruolo_disp"],
                        "prezzo": int(prezzo_asta),
                    })
                    st.success(
                        f"{p_sel['nome']} registrato a {f_sq} per {prezzo_asta} FM!"
                    )
                    st.rerun()

    else:
        st.caption(
            "🧠 **Valutazione IA Busta Chiusa**: seleziona uno o più calciatori."
            " L'IA analizzerà il tuo budget residuo, gli slot mancanti, la"
            " rarità del ruolo e l'imprevedibilità del mercato per indicarti"
            " l'offerta perfetta per ciascuno."
        )

        scelta_busta = st.multiselect(
            "Seleziona uno o più calciatori da valutare:",
            options=etichette_giocatori,
            placeholder="🔍 Seleziona uno o più giocatori...",
            key="busta_sel",
        )

        if not scelta_busta:
            st.info("Seleziona almeno un calciatore per calcolare le offerte consigliate.")
        else:
            budget_rim = stats_mia["rimasti"]
            righe_valutazione = []

            for etichetta in scelta_busta:
                p_busta = mappa_giocatori[etichetta]
                ruolo = p_busta["ruolo_disp"]
                valore_base = p_busta["valore_disp"]

                slot_occupati = stats_mia[ruolo]
                slot_liberi = SLOT_MAX[ruolo] - slot_occupati

                riserva_riparazione = max(10, slot_liberi * 2)
                budget_operativo = max(1, budget_rim - riserva_riparazione)

                peso_ruolo = {"A": 0.55, "C": 0.25, "D": 0.15, "P": 0.10}[ruolo]
                max_allocabile = budget_operativo * peso_ruolo

                offerta_ia = int(
                    min(
                        budget_operativo,
                        max(1, (valore_base / 100.0) * max_allocabile * 1.3),
                    )
                )
                offerta_prudente = int(max(1, offerta_ia * 0.8))
                offerta_aggressiva = int(min(budget_operativo, offerta_ia * 1.25))

                righe_valutazione.append({
                    "Giocatore": p_busta["nome"],
                    "Ruolo": ruolo,
                    "Squadra": p_busta["squadra_sa"],
                    "Valore": valore_base,
                    "Conservativa (FM)": offerta_prudente,
                    "Consigliata (FM)": offerta_ia,
                    "Aggressiva (FM)": offerta_aggressiva,
                })

            df_valutazione = pd.DataFrame(righe_valutazione).sort_values(
                "Valore", ascending=False
            )
            st.markdown("---")
            st.dataframe(df_valutazione, use_container_width=True, hide_index=True)

            totale_consigliato = int(df_valutazione["Consigliata (FM)"].sum())
            if totale_consigliato > budget_rim:
                st.warning(
                    f"⚠️ La somma delle offerte consigliate ({totale_consigliato} FM)"
                    f" supera il tuo budget residuo ({budget_rim} FM)."
                )
            else:
                st.success(
                    f"✅ Il totale delle offerte consigliate ({totale_consigliato} FM)"
                    f" rientra nel tuo budget residuo ({budget_rim} FM)."
                )


# --- RUOLI & VALORI ---
with tab_ruoli:
    st.markdown(
        "<div class='fanta-card'><div class='fanta-card-title'>🎭 Correggi"
        " Ruolo e Valore di un Calciatore</div></div>",
        unsafe_allow_html=True,
    )
    st.caption(
        "Se il ruolo o il valore di un calciatore mostrato qui non corrisponde"
        " a quello dell'app ufficiale del tuo fantacalcio, correggilo qui."
    )

    opzioni_tutti = costruisci_opzioni_giocatori(st.session_state.db_calciatori)
    etichette_tutti = [p["etichetta"] for p in opzioni_tutti]
    mappa_tutti = {p["etichetta"]: p for p in opzioni_tutti}

    scelta_mod = st.selectbox(
        "Calciatore da correggere:",
        options=etichette_tutti,
        index=None,
        placeholder="🔍 Seleziona un giocatore...",
        key="mod_ruolo_sel",
    )

    if scelta_mod:
        p_mod = mappa_tutti[scelta_mod]
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            nuovo_ruolo = st.selectbox(
                "Nuovo ruolo",
                ["P", "D", "C", "A"],
                index=["P", "D", "C", "A"].index(p_mod["ruolo_disp"]),
                key="nuovo_ruolo_sel",
            )
        with col_r2:
            nuovo_valore = st.number_input(
                "Nuovo valore (1-100)",
                min_value=1,
                max_value=100,
                value=int(p_mod["valore_disp"]),
                key="nuovo_valore_input",
            )
        if st.button("💾 Salva correzione"):
            st.session_state.custom_ruoli[p_mod["nome"]] = nuovo_ruolo
            st.session_state.custom_valori[p_mod["nome"]] = int(nuovo_valore)
            st.success(f"{p_mod['nome']} aggiornato con successo.")
            st.rerun()

    st.markdown("---")
    st.subheader("Correzioni attive")
    nomi_corretti = sorted(
        set(st.session_state.custom_ruoli) | set(st.session_state.custom_valori)
    )
    if not nomi_corretti:
        st.info("Nessuna correzione manuale applicata finora.")
    else:
        for nome in nomi_corretti:
            col_c1, col_c2 = st.columns([4, 1])
            r = st.session_state.custom_ruoli.get(nome, "—")
            v = st.session_state.custom_valori.get(nome, "—")
            col_c1.write(f"**{nome}** → ruolo: `{r}` | valore: `{v}`")
            if col_c2.button("🗑️", key=f"del_corr_{nome}"):
                st.session_state.custom_ruoli.pop(nome, None)
                st.session_state.custom_valori.pop(nome, None)
                st.rerun()
        if st.button("Reset di tutte le correzioni"):
            st.session_state.custom_ruoli = {}
            st.session_state.custom_valori = {}
            st.rerun()


# --- MODULO & FORMAZIONE ---
with tab_modulo:
    st.markdown(
        "<div class='fanta-card'><div class='fanta-card-title'>📋 Suggeritore"
        " Modulo Tattico & Formazione</div></div>",
        unsafe_allow_html=True,
    )
    
    roster_completo = get_complete_roster()

    def valuta_modulo_ottimale():
        mod_scores = {}
        for mod_k, req in MODULI.items():
            defens = sorted(
                [p for p in roster_completo if p["ruolo"] == "D"],
                key=lambda x: x["prezzo"],
                reverse=True,
            )[: req["D"]]
            midf = sorted(
                [p for p in roster_completo if p["ruolo"] == "C"],
                key=lambda x: x["prezzo"],
                reverse=True,
            )[: req["C"]]
            att = sorted(
                [p for p in roster_completo if p["ruolo"] == "A"],
                key=lambda x: x["prezzo"],
                reverse=True,
            )[: req["A"]]
            score = sum(p["prezzo"] for p in defens + midf + att)
            mod_scores[mod_k] = (score, defens, midf, att)
        
        best = max(mod_scores, key=lambda k: mod_scores[k][0])
        return best, mod_scores[best]

    miglior_mod, (punteggio, tit_d, tit_c, tit_a) = valuta_modulo_ottimale()
    tit_p = sorted([p for p in roster_completo if p["ruolo"] == "P"], key=lambda x: x["prezzo"], reverse=True)[:1]

    st.success(f"💡 **Modulo Consigliato**: **{miglior_mod}** (Punteggio Valore Titolari: {punteggio})")
    
    st.subheader("👕 Formazione Titolare Consigliata")
    titolari = tit_p + tit_d + tit_c + tit_a
    df_tit = pd.DataFrame([
        {
            "Ruolo": p["ruolo"],
            "Nome": p["nome"],
            "Squadra": p["squadra_sa"],
            "Prezzo/Valore": p["prezzo"],
            "Partita / Difficoltà": get_fdr_info(p["squadra_sa"])[0]
        }
        for p in titolari
    ])
    st.dataframe(df_tit, use_container_width=True, hide_index=True)


# --- DATABASE CALCIATORI ---
with tab_giocatori:
    st.markdown(
        "<div class='fanta-card'><div class='fanta-card-title'>📚 Calciatori Serie A</div></div>",
        unsafe_allow_html=True,
    )
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filtro_sq = st.selectbox("Filtra per Squadra:", ["Tutte"] + list(SQUADRE_SERIE_A_2026_27.values()))
    with col_f2:
        filtro_ruolo = st.selectbox("Filtra per Ruolo:", ["Tutti", "P", "D", "C", "A"])
        
    df_calc = pd.DataFrame(st.session_state.db_calciatori)
    if not df_calc.empty:
        if filtro_sq != "Tutte":
            cod = codice_da_nome_squadra(filtro_sq)
            df_calc = df_calc[df_calc["squadra_sa"] == cod]
        if filtro_ruolo != "Tutti":
            df_calc = df_calc[df_calc["ruolo_off"] == filtro_ruolo]
            
        st.dataframe(df_calc[["nome", "squadra_sa", "ruolo_off", "valore"]], use_container_width=True, hide_index=True)
        
    st.markdown("---")
    st.subheader("📊 Statistiche Storiche Giocatore (API)")
    giocatori_con_id = [g for g in st.session_state.db_calciatori if g.get("player_id")]
    if giocatori_con_id and _chiave_attiva:
        g_scelto = st.selectbox("Seleziona giocatore per consultare le statistiche:", options=[g["nome"] for g in giocatori_con_id])
        p_obj = next((g for g in giocatori_con_id if g["nome"] == g_scelto), None)
        if p_obj:
            df_stats = scarica_statistiche_giocatore(p_obj["player_id"], _chiave_attiva)
            if df_stats is not None and not df_stats.empty:
                st.dataframe(df_stats, use_container_width=True, hide_index=True)
            else:
                st.info("Nessuna statistica trovata in Serie A per questo giocatore.")
    else:
        st.info("Collega una chiave API valida per consultare le statistiche storiche dettagliate.")


# --- FANTA-COACH ---
with tab_coach:
    st.markdown(
        "<div class='fanta-card'><div class='fanta-card-title'>💬 Fanta-Coach IA</div></div>",
        unsafe_allow_html=True,
    )
    
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    if prompt := st.chat_input("Chiedi un consiglio tattico o di mercato..."):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
            
        risposta = f"Ecco il mio consiglio per '{prompt}': ti suggerisco di bilanciare bene la rosa puntando sui titolari di squadre con un calendario (FDR) favorevole!"
        st.session_state.chat_messages.append({"role": "assistant", "content": risposta})
        with st.chat_message("assistant"):
            st.write(risposta)


# --- TRADE ---
with tab_trade:
    st.markdown(
        "<div class='fanta-card'><div class='fanta-card-title'>🔄 Valutatore Scambi (Trade)</div></div>",
        unsafe_allow_html=True,
    )
    
    opzioni_t = costruisci_opzioni_giocatori(st.session_state.db_calciatori)
    nomi_t = [p["etichetta"] for p in opzioni_t]
    mappa_t = {p["etichetta"]: p for p in opzioni_t}
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.subheader("Cedi")
        ceduti = st.multiselect("Seleziona calciatori da cedere:", nomi_t, key="trade_cedi")
    with col_t2:
        st.subheader("Ricevi")
        ricevuti = st.multiselect("Seleziona calciatori da ricevere:", nomi_t, key="trade_ricevi")
        
    if ceduti and ricevuti:
        val_ceduti = sum(mappa_t[k]["valore_disp"] for k in ceduti)
        val_ricevuti = sum(mappa_t[k]["valore_disp"] for k in ricevuti)
        
        st.markdown("---")
        col_v1, col_v2, col_v3 = st.columns(3)
        col_v1.metric("Valore Totale Ceduto", f"{val_ceduti} pts")
        col_v2.metric("Valore Totale Ricevuto", f"{val_ricevuti} pts")
        diff = val_ricevuti - val_ceduti
        col_v3.metric("Bilancio Scambio", f"{diff:+d} pts")
        
        if diff > 5:
            st.success("🎉 Scambio favorevole! Incrementi il valore complessivo della rosa.")
        elif diff >= -5:
            st.info("⚖️ Scambio equo. Valuta in base alle tue esigenze nei singoli ruoli.")
        else:
            st.error("⚠️ Scambio svantaggioso. Stai cedendo più valore di quello che ricevi.")


# --- SIMULATORE MATCH ---
with tab_sim:
    st.markdown(
        "<div class='fanta-card'><div class='fanta-card-title'>⚔️ Simulatore Match</div></div>",
        unsafe_allow_html=True,
    )
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        sq_casa = st.selectbox("Squadra Casa:", st.session_state.squadre_lega, index=0)
    with col_s2:
        sq_trasf = st.selectbox(
            "Squadra Trasferta:",
            st.session_state.squadre_lega,
            index=min(1, len(st.session_state.squadre_lega) - 1),
        )
        
    if st.button("🚀 Simula Partita", use_container_width=True):
        st1 = get_stats_squadra(sq_casa)
        st2 = get_stats_squadra(sq_trasf)
        
        bonus_casa = 1 if st1["spesi"] >= st2["spesi"] else 0
        bonus_trasf = 1 if st2["spesi"] > st1["spesi"] else 0
        
        gol_casa = random.randint(0, 3) + bonus_casa
        gol_trasf = random.randint(0, 3) + bonus_trasf
        
        st.markdown("---")
        st.markdown(
            f"<h2 style='text-align: center; color: #52b788;'>{sq_casa} {gol_casa} - {gol_trasf} {sq_trasf}</h2>",
            unsafe_allow_html=True,
        )
        if gol_casa > gol_trasf:
            st.success(f"Vittoria per **{sq_casa}**!")
        elif gol_trasf > gol_casa:
            st.success(f"Vittoria per **{sq_trasf}**!")
        else:
            st.info("Pareggio spettacolare!")
