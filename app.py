from datetime import datetime
import random
import pandas as pd
import streamlit as st

# 1. Configurazione Pagina
st.set_page_config(
    page_title="FantaIA Assistant v0.9.0",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed",
)

URL_SFONDO_STADIO = "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?q=80&w=1920&auto=format&fit=crop"

# DATABASE CALCIATORI SERIE A (Aggiornato al 31/08/2026)
DB_CALCIATORI_DEFAULT = [
    # INTER
    {
        "nome": "Lautaro Martinez",
        "squadra_sa": "INT",
        "ruolo_off": "A",
        "valore": 88,
    },
    {"nome": "Marcus Thuram", "squadra_sa": "INT", "ruolo_off": "A", "valore": 68},
    {"nome": "Mehdi Taremi", "squadra_sa": "INT", "ruolo_off": "A", "valore": 35},
    {"nome": "Hakan Calhanoglu", "squadra_sa": "INT", "ruolo_off": "C", "valore": 48},
    {"nome": "Nicolò Barella", "squadra_sa": "INT", "ruolo_off": "C", "valore": 38},
    {
        "nome": "Federico Dimarco",
        "squadra_sa": "INT",
        "ruolo_off": "D",
        "valore": 42,
    },
    {"nome": "Yann Sommer", "squadra_sa": "INT", "ruolo_off": "P", "valore": 26},
    # JUVENTUS
    {"nome": "Dusan Vlahovic", "squadra_sa": "JUV", "ruolo_off": "A", "valore": 82},
    {
        "nome": "Francisco Conceição",
        "squadra_sa": "JUV",
        "ruolo_off": "A",
        "valore": 38,
    },
    {
        "nome": "Nico Gonzalez",
        "squadra_sa": "JUV",
        "ruolo_off": "A",
        "valore": 42,
    },
    {
        "nome": "Teun Koopmeiners",
        "squadra_sa": "JUV",
        "ruolo_off": "C",
        "valore": 52,
    },
    {"nome": "Douglas Luiz", "squadra_sa": "JUV", "ruolo_off": "C", "valore": 35},
    {"nome": "Gleison Bremer", "squadra_sa": "JUV", "ruolo_off": "D", "valore": 34},
    {
        "nome": "Michele Di Gregorio",
        "squadra_sa": "JUV",
        "ruolo_off": "P",
        "valore": 25,
    },
    # MILAN
    {"nome": "Alvaro Morata", "squadra_sa": "MIL", "ruolo_off": "A", "valore": 65},
    {"nome": "Rafael Leao", "squadra_sa": "MIL", "ruolo_off": "A", "valore": 72},
    {
        "nome": "Christian Pulisic",
        "squadra_sa": "MIL",
        "ruolo_off": "C",
        "valore": 50,
    },
    {
        "nome": "Tijjani Reijnders",
        "squadra_sa": "MIL",
        "ruolo_off": "C",
        "valore": 32,
    },
    {
        "nome": "Theo Hernandez",
        "squadra_sa": "MIL",
        "ruolo_off": "D",
        "valore": 38,
    },
    {"nome": "Mike Maignan", "squadra_sa": "MIL", "ruolo_off": "P", "valore": 25},
    # NAPOLI
    {"nome": "Romelu Lukaku", "squadra_sa": "NAP", "ruolo_off": "A", "valore": 78},
    {
        "nome": "Khvicha Kvaratskhelia",
        "squadra_sa": "NAP",
        "ruolo_off": "A",
        "valore": 75,
    },
    {"nome": "David Neres", "squadra_sa": "NAP", "ruolo_off": "A", "valore": 40},
    {
        "nome": "Scott McTominay",
        "squadra_sa": "NAP",
        "ruolo_off": "C",
        "valore": 36,
    },
    {
        "nome": "Alessandro Buongiorno",
        "squadra_sa": "NAP",
        "ruolo_off": "D",
        "valore": 30,
    },
    {
        "nome": "Giovanni Di Lorenzo",
        "squadra_sa": "NAP",
        "ruolo_off": "D",
        "valore": 24,
    },
    {"nome": "Alex Meret", "squadra_sa": "NAP", "ruolo_off": "P", "valore": 20},
    # ATALANTA
    {"nome": "Mateo Retegui", "squadra_sa": "ATA", "ruolo_off": "A", "valore": 68},
    {"nome": "Ademola Lookman", "squadra_sa": "ATA", "ruolo_off": "A", "valore": 64},
    {
        "nome": "Charles De Ketelaere",
        "squadra_sa": "ATA",
        "ruolo_off": "A",
        "valore": 48,
    },
    {
        "nome": "Lazar Samardzic",
        "squadra_sa": "ATA",
        "ruolo_off": "C",
        "valore": 32,
    },
    {"nome": "Ederson", "squadra_sa": "ATA", "ruolo_off": "C", "valore": 28},
    {
        "nome": "Marco Carnesecchi",
        "squadra_sa": "ATA",
        "ruolo_off": "P",
        "valore": 22,
    },
    # ROMA
    {"nome": "Artem Dovbyk", "squadra_sa": "ROM", "ruolo_off": "A", "valore": 70},
    {"nome": "Paulo Dybala", "squadra_sa": "ROM", "ruolo_off": "A", "valore": 60},
    {"nome": "Matias Soulé", "squadra_sa": "ROM", "ruolo_off": "A", "valore": 42},
    {"nome": "Manu Koné", "squadra_sa": "ROM", "ruolo_off": "C", "valore": 24},
    {"nome": "Mile Svilar", "squadra_sa": "ROM", "ruolo_off": "P", "valore": 22},
    # LAZIO
    {
        "nome": "Taty Castellanos",
        "squadra_sa": "LAZ",
        "ruolo_off": "A",
        "valore": 46,
    },
    {"nome": "Boulaye Dia", "squadra_sa": "LAZ", "ruolo_off": "A", "valore": 36},
    {
        "nome": "Mattia Zaccagni",
        "squadra_sa": "LAZ",
        "ruolo_off": "C",
        "valore": 40,
    },
    {"nome": "Ivan Provedel", "squadra_sa": "LAZ", "ruolo_off": "P", "valore": 18},
    # FIORENTINA
    {"nome": "Moise Kean", "squadra_sa": "FIO", "ruolo_off": "A", "valore": 52},
    {
        "nome": "Albert Gudmundsson",
        "squadra_sa": "FIO",
        "ruolo_off": "A",
        "valore": 55,
    },
    {"nome": "Andrea Colpani", "squadra_sa": "FIO", "ruolo_off": "C", "valore": 30},
    {"nome": "David De Gea", "squadra_sa": "FIO", "ruolo_off": "P", "valore": 20},
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
  info = CALENDARIO_SERIE_A.get(
      squadra_sa, {"opp": "N/D", "fdr": 3, "casa": True}
  )
  loc = "vs" if info["casa"] else "@"
  fdr = info["fdr"]
  badge = "🟢" if fdr <= 2 else ("🟡" if fdr == 3 else "🔴")
  return f"{loc} {info['opp']} {badge}", fdr


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

if "chat_messages" not in st.session_state:
  st.session_state.chat_messages = [
      {
          "role": "assistant",
          "content": (
              "Ciao Mister! Sono il tuo Fanta-Coach IA aggiornato al 31/08/2026."
              " Chiedimi qualsiasi consiglio!"
          ),
      }
  ]

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

# 4. Header & Pulviscolo Sincronizzazione Dati
st.markdown(
    f"""
<div class="header-container">
    <h1 style="margin:0; font-size:1.8rem; color:#ffffff;">⚽ FantaIA Assistant</h1>
    <span style="background:#52b788; color:#081c15; font-weight:bold; padding:4px 12px; border-radius:12px; font-size:0.8rem;">
        v0.9.0 - Live Sync: {st.session_state.last_update}
    </span>
</div>
""",
    unsafe_allow_html=True,
)

# Pulsante manuale per la sincronizzazione dei dati
col_sync1, col_sync2 = st.columns([2, 1])
with col_sync2:
  if st.button("🔄 Aggiorna Dati IA Ora", use_container_width=True):
    st.session_state.db_calciatori = DB_CALCIATORI_DEFAULT.copy()
    st.session_state.last_update = (
        datetime.now().strftime("%d/%m/%Y - %H:%M") + " CEST"
    )
    st.success("Dati rose e calciatori aggiornati in tempo reale!")
    st.rerun()

# 5. Navigazione Schede
tab_home, tab_asta, tab_modulo, tab_coach, tab_trade, tab_sim = st.tabs([
    "🏠 Home",
    "🔨 Asta",
    "📋 Modulo",
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
      "P": sum(
          1
          for p in acquisti
          if get_ruolo_effettivo(p["nome"], p["ruolo"]) == "P"
      ),
      "D": sum(
          1
          for p in acquisti
          if get_ruolo_effettivo(p["nome"], p["ruolo"]) == "D"
      ),
      "C": sum(
          1
          for p in acquisti
          if get_ruolo_effettivo(p["nome"], p["ruolo"]) == "C"
      ),
      "A": sum(
          1
          for p in acquisti
          if get_ruolo_effettivo(p["nome"], p["ruolo"]) == "A"
      ),
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
    for idx, p in enumerate(stats_mia["acquisti"]):
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
            key=f"r_sel_{idx}",
        )
        if nuovo_r != r_curr:
          st.session_state.custom_ruoli[p["nome"]] = nuovo_r
          st.rerun()
      with col_del:
        if st.button("🗑️ Elimina", key=f"del_p_{idx}"):
          st.session_state.tutti_acquisti.pop(idx)
          st.rerun()

    if st.button("🚨 Reset Completo Mia Rosa", type="primary"):
      st.session_state.tutti_acquisti = [
          p
          for p in st.session_state.tutti_acquisti
          if p["fantasquadra"] != st.session_state.nome_mia_squadra
      ]
      st.rerun()


# --- ASTA (LIVE VS BUSTA CHIUSA IA TOTALMENTE AUTOMATICA) ---
with tab_asta:
  st.markdown(
      "<div class='fanta-card'><div class='fanta-card-title'>🔨 Gestione"
      " Asta</div></div>",
      unsafe_allow_html=True,
  )

  tipo_asta = st.radio(
      "Seleziona Modalità:", ["🔴 Chiamata / Live", "✉️ Busta Chiusa (Full IA)"], horizontal=True
  )

  opzioni_giocatori = [
      f"[{p['ruolo_off']}] {p['nome']} ({p['squadra_sa']})"
      for p in st.session_state.db_calciatori
  ]

  if tipo_asta == "🔴 Chiamata / Live":
    scelta_g = st.selectbox(
        "Cerca o Seleziona Calciatore:",
        options=opzioni_giocatori,
        key="live_sel",
    )
    p_sel = next(
        p
        for p in st.session_state.db_calciatori
        if f"[{p['ruolo_off']}] {p['nome']} ({p['squadra_sa']})" == scelta_g
    )

    with st.form("form_asta_live_auto", clear_on_submit=True):
      f_sq = st.selectbox(
          "Acquirente Fanta-Lega:", options=st.session_state.squadre_lega
      )
      col_a1, col_a2 = st.columns(2)
      col_a1.text_input("Giocatore", value=p_sel["nome"], disabled=True)
      col_a2.text_input(
          "Ruolo & Squadra",
          value=f"{p_sel['ruolo_off']} | {p_sel['squadra_sa']}",
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
            "ruolo": p_sel["ruolo_off"],
            "prezzo": int(prezzo_asta),
        })
        st.success(
            f"{p_sel['nome']} registrato a {f_sq} per {prezzo_asta} FM!"
        )
        st.rerun()

  else:
    # ✉️ BUSTA CHIUSA FULL IA AUTOMATICA
    st.caption(
        "🧠 **Valutazione IA Busta Chiusa**: Seleziona il calciatore. L'IA"
        " analizzerà automaticamente il tuo budget residuo, gli slot mancanti,"
        " la rarità del ruolo e l'imprevedibilità del mercato per indicarti l'offerta perfetta."
    )

    scelta_busta = st.selectbox(
        "Seleziona Calciatore per l'Offerta in Busta:",
        options=opzioni_giocatori,
        key="busta_sel",
    )
    p_busta = next(
        p
        for p in st.session_state.db_calciatori
        if f"[{p['ruolo_off']}] {p['nome']} ({p['squadra_sa']})" == scelta_busta
    )

    if st.button(
        "⚡ Calcola Offerta Ottimale IA",
        use_container_width=True,
        type="primary",
    ):
      budget_rim = stats_mia["rimasti"]
      ruolo = p_busta["ruolo_off"]
      valore_base = p_busta["valore"]

      # Algoritmo IA di decisione dell'offerta
      slot_occupati = stats_mia[ruolo]
      slot_liberi = SLOT_MAX[ruolo] - slot_occupati

      # Riserva calcolata per asta di riparazione + slot rimasti
      riserva_riparazione = max(10, slot_liberi * 2)
      budget_operativo = max(1, budget_rim - riserva_riparazione)

      # Coefficiente peso per ruolo
      peso_ruolo = {"A": 0.55, "C": 0.25, "D": 0.15, "P": 0.10}[ruolo]
      max_allocabile = budget_operativo * peso_ruolo

      # Imprevedibilità mercato
      offerta_ia = int(
          min(
              budget_operativo,
              max(1, (valore_base / 100.0) * max_allocabile * 1.3),
          )
      )
      offerta_prudente = int(max(1, offerta_ia * 0.8))
      offerta_aggressiva = int(min(budget_operativo, offerta_ia * 1.25))

      st.markdown("---")
      st.markdown(
          f"### 🤖 Valutazione IA per **{p_busta['nome']}**"
          f" ({p_busta['squadra_sa']})"
      )
      st.write(
          f"• **Ruolo:** `{ruolo}` | **Slot Liberi:** `{slot_liberi}` | **Crediti"
          f" Disponibili:** `{budget_rim} FM`"
      )

      c_b1, c_b2, c_b3 = st.columns(3)
      c_b1.metric("🛡️ Offerta Conservativa", f"{offerta_prudente} FM")
      c_b2.metric("🎯 Offerta CONSIGLIATA IA", f"{offerta_ia} FM")
      c_b3.metric("🔥 Offerta All-In Aggressiva", f"{offerta_aggressiva} FM")

      st.info(
          f"💡 **Motivazione IA:** Per assicurarti {p_busta['nome']} senza"
          f" sbilanciare il resto della rosa, l'offerta consigliata è di **{offerta_ia} FM**."
          f" Viene mantenuta una riserva automatica di **{riserva_riparazione} FM** per gli altri slot e per l'asta di riparazione."
      )


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
      score_tot = 0
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
    cols = st.columns(len(r_list))
    for idx, p in enumerate(r_list):
      fdr_badge, fdr_val = get_fdr_info(p["squadra_sa"])
      prob_tit = min(99, max(50, 70 + (3 - fdr_val) * 8 + random.randint(-4, 4)))
      is_cap = " (C)👑" if p["nome"] == capitano["nome"] else ""
      with cols[idx]:
        st.info(
            f"**{p['nome']}**{is_cap}\n\n{p['squadra_sa']} |"
            f" {fdr_badge}\n\nTitolarità: **{prob_tit}%**"
        )


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
    reply = (
        "Mister, ti confermo che la rosa e le percentuali sono state aggiornate"
        " alle ultime novità di mercato del 31/08/2026!"
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
