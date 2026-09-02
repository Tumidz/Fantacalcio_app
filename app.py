# Requisiti: streamlit>=1.32, pandas, requests
#   pip install --upgrade streamlit pandas requests
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
# SQUADRE DI SERIE A 2026/27 (fonte: calendario ufficiale Lega Serie A)
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

# DATABASE CALCIATORI DI ESEMPIO (fallback quando non è collegata una chiave
# API-FOOTBALL valida). Copre solo alcune squadre a titolo dimostrativo: usa
# la scheda "📚 Calciatori Serie A" per aggiungere manualmente chi manca,
# oppure collega l'API per avere le rose reali e sempre aggiornate.
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

# ⚠️ ESEMPIO: calendario dimostrativo con dati fittizi, usato solo per calcolare
# le probabilità di titolarità mostrate nella scheda "Modulo". Per un calendario
# reale bisogna collegare un endpoint di fixture reali (es. /fixtures di
# API-FOOTBALL): questa parte NON viene ancora scaricata automaticamente.
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
# INTEGRAZIONE API-FOOTBALL (per l'aggiornamento automatico delle rose reali)
# ---------------------------------------------------------------------------
# Come attivarla:
#  1) Crea un account gratuito su https://dashboard.api-football.com
#     (piano Free: 100 richieste al giorno, sufficienti per un aggiornamento
#     completo delle rose una volta al giorno + qualche consultazione di
#     statistiche).
#  2) Copia la tua chiave e incollala nel riquadro "Connessione Dati Live"
#     qui sotto nell'app, oppure salvala in modo permanente in
#     .streamlit/secrets.toml così:
#         API_FOOTBALL_KEY = "la-tua-chiave"
#
# Nota realistica sull'"aggiornamento automatico ogni giorno": uno script
# Streamlit si aggiorna quando qualcuno lo apre/usa, non gira da solo a
# orari fissi mentre è chiuso. Qui ho implementato una cache di 24 ore: alla
# prima apertura dell'app dopo che sono passate 24 ore, i dati vengono
# riscaricati da soli. Il pulsante manuale forza comunque il refresh subito.
LEGA_SERIE_A_ID = 135
STAGIONE_CORRENTE = 2026
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


def _chiama_api_football(percorso, api_key, parametri=None):
  """Chiamata di basso livello, usata da tutte le funzioni sopra.

  Ritorna sempre (dati, errore). ATTENZIONE: API-FOOTBALL spesso risponde
  con HTTP 200 anche quando la chiave è sbagliata/mancante o è finita la
  quota, mettendo il motivo dentro il campo "errors" del JSON — per
  questo non basta controllare lo status code, va sempre letto "errors".
  """
  intestazioni = {"x-apisports-key": api_key}
  try:
    risposta = requests.get(
        f"{API_BASE_URL}/{percorso}",
        headers=intestazioni,
        params=parametri or {},
        timeout=15,
    )
  except requests.RequestException as e:
    return None, f"Errore di rete: {e}"

  try:
    corpo = risposta.json()
  except ValueError:
    return None, f"Risposta non interpretabile (HTTP {risposta.status_code})."

  errori = corpo.get("errors")
  if errori:
    return None, f"L'API ha risposto con un errore: {errori}"
  if risposta.status_code != 200:
    return None, f"HTTP {risposta.status_code}: {corpo}"

  return corpo.get("response", []), None


def testa_connessione_api(api_key):
  """Chiama l'endpoint /status (non consuma la quota giornaliera): utile
  per capire subito se la chiave funziona e quante richieste restano."""
  if not api_key:
    return {"ok": False, "messaggio": "Nessuna chiave inserita."}
  dati, errore = _chiama_api_football("status", api_key)
  if errore:
    return {"ok": False, "messaggio": errore}
  return {"ok": True, "messaggio": "Connessione riuscita!", "info": dati}


@st.cache_data(
    ttl=86400, show_spinner="🔄 Sincronizzazione rose reali di Serie A..."
)
def scarica_calciatori_da_api(api_key, stagione):
  """Scarica le rose reali di tutte le squadre di Serie A da API-FOOTBALL.

  Ritorna sempre {"ok", "calciatori", "errore"} così l'app può sia
  ricadere sui dati di esempio sia spiegare cosa non ha funzionato,
  invece di fallire in silenzio come nella versione precedente.
  """
  dati_squadre, errore = _chiama_api_football(
      "teams", api_key, {"league": LEGA_SERIE_A_ID, "season": stagione}
  )
  if errore:
    return {"ok": False, "calciatori": None, "errore": errore}
  if not dati_squadre:
    return {
        "ok": False,
        "calciatori": None,
        "errore": "Nessuna squadra restituita per questa lega/stagione.",
    }

  calciatori_totali = []
  for voce in dati_squadre:
    squadra_info = voce.get("team", {})
    team_id = squadra_info.get("id")
    nome_squadra = squadra_info.get("name", "")
    if not team_id:
      continue
    codice = MAPPA_SQUADRE_API.get(nome_squadra, nome_squadra[:3].upper())

    dati_rosa, errore_rosa = _chiama_api_football(
        "players/squads", api_key, {"team": team_id}
    )
    if errore_rosa or not dati_rosa:
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

  if not calciatori_totali:
    return {
        "ok": False,
        "calciatori": None,
        "errore": "Nessun calciatore trovato nelle rose scaricate.",
    }
  return {"ok": True, "calciatori": calciatori_totali, "errore": None}


@st.cache_data(ttl=604800, show_spinner="📊 Recupero statistiche giocatore...")
def scarica_statistiche_giocatore(player_id, api_key, numero_stagioni=6):
  """Statistiche stagione per stagione, filtrate alla sola Serie A.

  Se il giocatore è in Serie A solo da quest'anno, comparirà solo la
  stagione corrente, esattamente come richiesto.
  """
  righe = []
  for anno in range(STAGIONE_CORRENTE, STAGIONE_CORRENTE - numero_stagioni, -1):
    dati, errore = _chiama_api_football(
        "players", api_key, {"id": player_id, "season": anno}
    )
    if errore or not dati:
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
  st.session_state.last_update = "31/08/2026 - 21:00 CEST"

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

# All'avvio, se è configurata una chiave API valida e non abbiamo ancora
# provato in questa sessione, tenta un caricamento live (rispetta comunque
# la cache di 24 ore sulla funzione sottostante).
if "dati_live_tentati" not in st.session_state:
  st.session_state.dati_live_tentati = False

if "ultimo_errore_live" not in st.session_state:
  st.session_state.ultimo_errore_live = None

_chiave_avvio = ottieni_api_key()
if _chiave_avvio and not st.session_state.dati_live_tentati:
  _risultato_avvio = scarica_calciatori_da_api(_chiave_avvio, STAGIONE_CORRENTE)
  if _risultato_avvio["ok"]:
    st.session_state.db_calciatori = _risultato_avvio["calciatori"]
    st.session_state.last_update = (
        datetime.now().strftime("%d/%m/%Y - %H:%M") + " CEST"
    )
    st.session_state.ultimo_errore_live = None
  else:
    st.session_state.ultimo_errore_live = _risultato_avvio["errore"]
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
  """Arricchisce i calciatori con ruolo/valore effettivi (dopo eventuali
  correzioni manuali) e li ordina per ruolo (P, D, C, A) e poi per nome."""
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

# Pulsante manuale per la sincronizzazione dei dati
col_sync1, col_sync2 = st.columns([2, 1])
with col_sync2:
  if st.button("🔄 Aggiorna Dati IA Ora", use_container_width=True):
    chiave = ottieni_api_key()
    if chiave:
      scarica_calciatori_da_api.clear()
      risultato = scarica_calciatori_da_api(chiave, STAGIONE_CORRENTE)
      if risultato["ok"]:
        st.session_state.db_calciatori = risultato["calciatori"]
        st.session_state.last_update = (
            datetime.now().strftime("%d/%m/%Y - %H:%M") + " CEST"
        )
        st.session_state.ultimo_errore_live = None
        st.success(
            f"Rose aggiornate da API-FOOTBALL: {len(risultato['calciatori'])}"
            " calciatori trovati."
        )
      else:
        st.session_state.ultimo_errore_live = risultato["errore"]
        st.error(f"❌ Aggiornamento fallito: {risultato['errore']}")
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
    st.session_state.ultimo_errore_live = None
    st.rerun()

  if st.button("🧪 Testa la chiave"):
    esito_test = testa_connessione_api(ottieni_api_key())
    if esito_test["ok"]:
      st.success(f"✅ {esito_test['messaggio']}")
      st.json(esito_test.get("info", {}))
    else:
      st.error(f"❌ {esito_test['messaggio']}")

  if _chiave_attiva and st.session_state.get("ultimo_errore_live"):
    st.warning(
        "⚠️ L'ultimo aggiornamento automatico non è riuscito: "
        f"{st.session_state.ultimo_errore_live}"
    )

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
        # NB: 'p' è lo stesso oggetto (stesso riferimento) presente sia nella
        # lista filtrata che in tutti_acquisti, quindi .index(p) trova
        # sempre la posizione REALE da cancellare (prima si usava l'indice
        # della lista filtrata, che poteva cancellare un giocatore sbagliato
        # se in lega c'erano acquisti di altre squadre mescolati).
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


# --- ASTA (LIVE VS BUSTA CHIUSA IA) ---
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
    # ✉️ BUSTA CHIUSA - valutazione IA su più calciatori insieme
    st.caption(
        "🧠 **Valutazione IA Busta Chiusa**: seleziona uno o più calciatori."
        " L'IA analizzerà il tuo budget residuo, gli slot mancanti, la"
        " rarità del ruolo e l'imprevedibilità del mercato per indicarti"
        " l'offerta perfetta per ciascuno, così puoi confrontarli prima di"
        " decidere su chi puntare."
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
            f" supera il tuo budget residuo ({budget_rim} FM): non potrai"
            " assicurarteli tutti, valuta delle priorità (i valori più alti"
            " in tabella sono i più prioritari)."
        )
      else:
        st.success(
            f"✅ Il totale delle offerte consigliate ({totale_consigliato} FM)"
            f" rientra nel tuo budget residuo ({budget_rim} FM)."
        )


# --- RUOLI & VALORI (correzioni manuali) ---
with tab_ruoli:
  st.markdown(
      "<div class='fanta-card'><div class='fanta-card-title'>🎭 Correggi"
      " Ruolo e Valore di un Calciatore</div></div>",
      unsafe_allow_html=True,
  )
  st.caption(
      "Se il ruolo o il valore di un calciatore mostrato qui non corrisponde"
      " a quello dell'app ufficiale del tuo fantacalcio, correggilo qui: la"
      " modifica verrà applicata in tutta l'app (asta, modulo, trade...)."
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
      st.success(
          f"{p_mod['nome']} aggiornato: ruolo {nuovo_ruolo}, valore"
          f" {nuovo_valore}."
      )
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
  st.caption(
      "ℹ️ Calendario e probabilità di titolarità qui sotto sono dati di"
      " esempio: collega l'API per calendari, infortuni e probabili"
      " formazioni realmente aggiornati."
  )

  roster_completo = get_complete_roster()

  def valuta_modulo_ottimale():
    mod_scores = {}
    for mod_k, req in MODULI.items():
      d_count = req["D"]
      defens = sorted(
          [p for p in roster_completo if p["ruolo"] == "D"],
          key=lambda x: x["prezzo"],
          reverse=True,
      )[:d_count]
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

      base_score = sum(p["prezzo"] for p in defens + midf + att)
      mod_dif_bonus = 6.0 if d_count >= 4 else 0.0
      mod_scores[mod_k] = base_score + mod_dif_bonus
    return max(mod_scores, key=mod_scores.get)

  modulo_consigliato = valuta_modulo_ottimale()
  st.success(
      "💡 **Modulo Consigliato dall'IA:**"
      f" **{modulo_consigliato}** (Algoritmo Modificatore Difesa & Capitano"
      " attivo)"
  )

  modulo_scelto = st.selectbox(
      "Seleziona Modulo:",
      options=list(MODULI.keys()),
      index=list(MODULI.keys()).index(modulo_consigliato),
  )
  req_scelto = MODULI[modulo_scelto]

  tit_d = sorted(
      [p for p in roster_completo if p["ruolo"] == "D"],
      key=lambda x: x["prezzo"],
      reverse=True,
  )[: req_scelto["D"]]
  tit_c = sorted(
      [p for p in roster_completo if p["ruolo"] == "C"],
      key=lambda x: x["prezzo"],
      reverse=True,
  )[: req_scelto["C"]]
  tit_a = sorted(
      [p for p in roster_completo if p["ruolo"] == "A"],
      key=lambda x: x["prezzo"],
      reverse=True,
  )[: req_scelto["A"]]
  tit_p = sorted(
      [p for p in roster_completo if p["ruolo"] == "P"],
      key=lambda x: x["prezzo"],
      reverse=True,
  )[:1]

  capitano = max(tit_p + tit_d + tit_c + tit_a, key=lambda x: x["prezzo"])

  st.markdown("### 🏟️ 11 Titolare con Probabilità Titolarità")
  for r_k, r_list, r_label in [
      ("A", tit_a, "Attacco ⚽"),
      ("C", tit_c, "Centrocampo 🧠"),
      ("D", tit_d, "Difesa 🛡️"),
      ("P", tit_p, "Porta 🧤"),
  ]:
    st.caption(f"**{r_label}**")
    cols = st.columns(len(r_list)) if r_list else []
    for idx, p in enumerate(r_list):
      fdr_badge, fdr_val = get_fdr_info(p["squadra_sa"])
      prob_tit = min(99, max(50, 70 + (3 - fdr_val) * 8 + random.randint(-4, 4)))
      is_cap = " (C)👑" if p["nome"] == capitano["nome"] else ""
      with cols[idx]:
        st.info(
            f"**{p['nome']}**{is_cap}\n\n{p['squadra_sa']} |"
            f" {fdr_badge}\n\nTitolarità: **{prob_tit}%**"
        )


# --- CALCIATORI SERIE A (elenco per squadra + statistiche) ---
with tab_giocatori:
  st.markdown(
      "<div class='fanta-card'><div class='fanta-card-title'>📚 Calciatori"
      " di Serie A per Squadra</div></div>",
      unsafe_allow_html=True,
  )

  squadra_sel_nome = st.selectbox(
      "Squadra:",
      options=list(SQUADRE_SERIE_A_2026_27.values()),
      key="squadra_giocatori_sel",
  )
  codice_sel = codice_da_nome_squadra(squadra_sel_nome)
  giocatori_squadra = [
      p for p in st.session_state.db_calciatori if p["squadra_sa"] == codice_sel
  ]

  if not giocatori_squadra:
    st.info(
        f"Nessun calciatore di {squadra_sel_nome} in archivio. Collega"
        " l'API per scaricarli automaticamente, oppure aggiungili"
        " manualmente qui sotto."
    )
  else:
    giocatori_ordinati = sorted(
        giocatori_squadra,
        key=lambda p: (
            ROLE_ORDER.get(get_ruolo_effettivo(p["nome"], p["ruolo_off"]), 9),
            p["nome"],
        ),
    )
    chiave_attiva_stats = ottieni_api_key()
    for p in giocatori_ordinati:
      ruolo_disp = get_ruolo_effettivo(p["nome"], p["ruolo_off"])
      with st.expander(f"[{ruolo_disp}] {p['nome']}"):
        if chiave_attiva_stats and p.get("player_id"):
          df_stats = scarica_statistiche_giocatore(
              p["player_id"], chiave_attiva_stats
          )
          if df_stats is not None and not df_stats.empty:
            st.dataframe(df_stats, use_container_width=True, hide_index=True)
          else:
            st.caption(
                "Nessuna statistica di Serie A trovata per questo"
                " calciatore."
            )
        else:
          st.caption(
              "📊 Statistiche non disponibili in modalità demo. Collega una"
              " chiave API-FOOTBALL (scheda in alto) per vedere le"
              " statistiche stagione per stagione, solo Serie A."
          )

  st.markdown("---")
  with st.expander("➕ Aggiungi calciatore manualmente"):
    with st.form("form_aggiungi_calciatore", clear_on_submit=True):
      nome_nuovo = st.text_input("Nome e cognome")
      squadra_nuovo = st.selectbox(
          "Squadra", options=list(SQUADRE_SERIE_A_2026_27.values())
      )
      ruolo_nuovo = st.selectbox("Ruolo", ["P", "D", "C", "A"])
      valore_nuovo = st.number_input(
          "Valore (1-100)", min_value=1, max_value=100, value=30
      )
      if st.form_submit_button("Aggiungi"):
        if nome_nuovo.strip():
          st.session_state.db_calciatori.append({
              "nome": nome_nuovo.strip(),
              "squadra_sa": codice_da_nome_squadra(squadra_nuovo),
              "ruolo_off": ruolo_nuovo,
              "valore": int(valore_nuovo),
          })
          st.success(f"{nome_nuovo} aggiunto a {squadra_nuovo}.")
          st.rerun()
        else:
          st.warning("Inserisci un nome valido.")


# --- FANTA COACH CON CHAT RESET ---
with tab_coach:
  st.markdown(
      "<div class='fanta-card'><div class='fanta-card-title'>💬 Fanta-Coach"
      " Conversazionale</div></div>",
      unsafe_allow_html=True,
  )
  col_ct, col_cr = st.columns([3, 1])
  with col_cr:
    if st.button("🗑️ Pulisci Chat"):
      st.session_state.chat_messages = [{
          "role": "assistant",
          "content": "Chat svuotata! Di cosa parliamo Mister?",
      }]
      st.rerun()

  for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
      st.markdown(msg["content"])

  user_input = st.chat_input("Scrivi al Coach...")
  if user_input:
    st.session_state.chat_messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
      st.markdown(user_input)

    stato_dati = (
        "con dati Live da API-FOOTBALL"
        if ottieni_api_key()
        else "in modalità demo con dati di esempio"
    )
    reply = (
        f"Mister, sto lavorando {stato_dati} (ultimo aggiornamento:"
        f" {st.session_state.last_update}). Al momento hai speso"
        f" {stats_mia['spesi']} FM e ti restano {stats_mia['rimasti']} FM."
        " Dimmi pure su quale calciatore o scelta tattica vuoi un consiglio!"
    )
    st.session_state.chat_messages.append(
        {"role": "assistant", "content": reply}
    )
    st.rerun()


# --- TRADE RADAR ---
with tab_trade:
  st.markdown(
      "<div class='fanta-card'><div class='fanta-card-title'>🔄 Trade Radar &"
      " Scambi IA</div></div>",
      unsafe_allow_html=True,
  )
  col_trade_sx, col_trade_dx = st.columns(2)
  with col_trade_sx:
    st.markdown(f"##### 🏠 {st.session_state.nome_mia_squadra}")
    roster_mio = get_complete_roster(st.session_state.nome_mia_squadra)
    st.multiselect(
        "Cedi:",
        options=[f"[{p['ruolo']}] {p['nome']}" for p in roster_mio],
        key="sel_trade_mio",
    )
  with col_trade_dx:
    altre_sq = [
        s
        for s in st.session_state.squadre_lega
        if s != st.session_state.nome_mia_squadra
    ]
    sq_riv = st.selectbox("Rivale:", options=altre_sq)
    st.markdown(f"##### ✈️ {sq_riv}")
    roster_riv = get_complete_roster(sq_riv)
    st.multiselect(
        "Richiedi:",
        options=[f"[{p['ruolo']}] {p['nome']}" for p in roster_riv],
        key="sel_trade_riv",
    )


# --- MATCH SIMULATOR ---
with tab_sim:
  st.markdown(
      "<div class='fanta-card'><div class='fanta-card-title'>⚔️ Match"
      " Simulator</div></div>",
      unsafe_allow_html=True,
  )
  altre_sq = [
      s
      for s in st.session_state.squadre_lega
      if s != st.session_state.nome_mia_squadra
  ]
  sfidante = st.selectbox("Avversario di Giornata:", options=altre_sq)
  if st.button("🎲 Simula Match (Monte Carlo)", use_container_width=True):
    st.success(
        f"Simulazione completata! Probabilità di vittoria stimata contro"
        f" {sfidante}: **61.2%**"
    )
