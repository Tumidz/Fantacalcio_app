import streamlit as st

st.set_page_config(page_title="Algo Free - 100% Automatico", page_icon="⚽", layout="wide")

st.title("⚽ Algo Smart - Calcolo Indici 100% Automatico")
st.caption("L'algoritmo calcola da solo l'indice di ogni calciatore incrociando Media Voto, Avversario e Casa/Trasferta.")

# --- LIVELlO DIFFICOLTÀ SQUADRE SERIE A (1 = Facile, 5 = Proibitiva) ---
DIFFICOLTA_SQUADRE = {
    "Inter": 5, "Juventus": 5, "Napoli": 5, "Milan": 4, "Atalanta": 4,
    "Lazio": 4, "Roma": 4, "Fiorentina": 3, "Bologna": 3, "Torino": 3,
    "Udinese": 2, "Genoa": 2, "Verona": 2, "Cagliari": 2, "Empoli": 2,
    "Parma": 2, "Lecce": 1, "Como": 1, "Venezia": 1, "Monza": 1
}

# --- DATABASE ROSA CON SQUADRE E MEDIA VOTO REALE ---
if "rosa" not in st.session_state:
    st.session_state.rosa = [
        # Portieri
        {"nome": "Maignan", "ruolo": "P", "squadra": "Milan", "mv": 6.3},
        {"nome": "Sportiello", "ruolo": "P", "squadra": "Milan", "mv": 6.0},
        # Difensori
        {"nome": "Dimarco", "ruolo": "D", "squadra": "Inter", "mv": 6.7},
        {"nome": "Theo Hernandez", "ruolo": "D", "squadra": "Milan", "mv": 6.5},
        {"nome": "Bremer", "ruolo": "D", "squadra": "Juventus", "mv": 6.4},
        {"nome": "Di Lorenzo", "ruolo": "D", "squadra": "Napoli", "mv": 6.2},
        {"nome": "Buongiorno", "ruolo": "D", "squadra": "Napoli", "mv": 6.3},
        # Centrocampisti
        {"nome": "Pulisic", "ruolo": "C", "squadra": "Milan", "mv": 6.8},
        {"nome": "Barella", "ruolo": "C", "squadra": "Inter", "mv": 6.5},
        {"nome": "Koopmeiners", "ruolo": "C", "squadra": "Juventus", "mv": 6.6},
        {"nome": "Zaccagni", "ruolo": "C", "squadra": "Lazio", "mv": 6.4},
        {"nome": "Calhanoglu", "ruolo": "C", "squadra": "Inter", "mv": 6.6},
        # Attaccanti
        {"nome": "Lautaro Martinez", "ruolo": "A", "squadra": "Inter", "mv": 7.2},
        {"nome": "Vlahovic", "ruolo": "A", "squadra": "Juventus", "mv": 7.0},
        {"nome": "Lookman", "ruolo": "A", "squadra": "Atalanta", "mv": 6.9},
        {"nome": "Retegui", "ruolo": "A", "squadra": "Atalanta", "mv": 6.8},
    ]

# --- MOTORE MATEMATICO AUTOMATICO ---
def calcola_indice_auto(mv, avversario, in_casa):
    diff = DIFFICOLTA_SQUADRE.get(avversario, 3)
    # Impatto Match: Sfidare una squadra facile (diff=1) dà bonus, una difficile (diff=5) dà malus
    bonus_match = (3 - diff) * 0.4
    bonus_casa = 0.3 if in_casa else 0.0
    
    indice = mv + bonus_match + bonus_casa
    return round(max(1.0, min(10.0, indice * 1.15)), 2)

tab_calc, tab_partire = st.tabs(["🚀 Formazione Automatica", "🗓️ Calendario Turno"])

with tab_partire:
    st.subheader("Imposta gli accoppiamenti del Turno")
    st.write("Scegli le avversarie delle principali squadre per questa giornata:")
    
    if "partite" not in st.session_state:
        st.session_state.partite = {
            "Inter": {"vs": "Monza", "casa": True},
            "Milan": {"vs": "Lazio", "casa": False},
            "Juventus": {"vs": "Venezia", "casa": True},
            "Napoli": {"vs": "Empoli", "casa": True},
            "Atalanta": {"vs": "Lecce", "casa": True},
            "Lazio": {"vs": "Milan", "casa": True},
        }

    for sq in st.session_state.partite.keys():
        c1, c2, c3 = st.columns(3)
        c1.write(f"**{sq}**")
        vs = c2.selectbox(f"contro", list(DIFFICOLTA_SQUADRE.keys()), key=f"vs_{sq}", index=list(DIFFICOLTA_SQUADRE.keys()).index(st.session_state.partite[sq]["vs"]))
        casa = c3.checkbox("In Casa 🏠", value=st.session_state.partite[sq]["casa"], key=f"casa_{sq}")
        st.session_state.partite[sq] = {"vs": vs, "casa": casa}

with tab_calc:
    if st.button("⚡ Genera Formazione con Indici Automatici", type="primary", use_container_width=True):
        # Generazione Indici in tempo reale
        rosa_aggiornata = []
        for g in st.session_state.rosa:
            info_match = st.session_state.partite.get(g["squadra"], {"vs": "Genoa", "casa": True})
            idx = calcola_indice_auto(g["mv"], info_match["vs"], info_match["casa"])
            rosa_aggiornata.append({**g, "indice": idx, "vs": info_match["vs"]})

        # Calcolo Top 11 su Modulo
        portieri = sorted([p for p in rosa_aggiornata if p["ruolo"] == "P"], key=lambda x: x["indice"], reverse=True)
        difensori = sorted([p for p in rosa_aggiornata if p["ruolo"] == "D"], key=lambda x: x["indice"], reverse=True)
        centrocampisti = sorted([p for p in rosa_aggiornata if p["ruolo"] == "C"], key=lambda x: x["indice"], reverse=True)
        attaccanti = sorted([p for p in rosa_aggiornata if p["ruolo"] == "A"], key=lambda x: x["indice"], reverse=True)

        moduli = {"3-4-3": (3, 4, 3), "4-3-3": (4, 3, 3), "3-5-2": (3, 5, 2), "4-4-2": (4, 4, 2)}
        miglior_punteggio, miglior_modulo, miglior_11 = -1, "", []

        for nome_m, (nd, nc, na) in moduli.items():
            if len(difensori) >= nd and len(centrocampisti) >= nc and len(attaccanti) >= na:
                squadra = portieri[:1] + difensori[:nd] + centrocampisti[:nc] + attaccanti[:na]
                tot = sum(p["indice"] for p in squadra)
                if tot > miglior_punteggio:
                    miglior_punteggio, miglior_modulo, miglior_11 = tot, nome_m, squadra

        st.success(f"🌟 Modulo Ottimale: **{miglior_modulo}** (Punteggio Algo: {round(miglior_punteggio, 2)})")
        st.divider()

        col_p, col_d, col_c, col_a = st.columns(4)
        for col, ruolo, emoji, titolo in [(col_p, "P", "🧤", "Portiere"), (col_d, "D", "🛡️", "Difesa"), (col_c, "C", "⚙️", "Centrocampo"), (col_a, "A", "⚽", "Attacco")]:
            with col:
                st.markdown(f"### {emoji} {titolo}")
                for p in [x for x in miglior_11 if x["ruolo"] == ruolo]:
                    st.info(f"**{p['nome']}**\n\nIndice: **{p['indice']}** *(vs {p['vs']})*")
