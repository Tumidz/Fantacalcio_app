import streamlit as st

st.set_page_config(page_title="Algo Free - Formazione Smart", page_icon="⚽", layout="wide")

st.title("⚽ Algo Smart Assistant - Modulo & Formazione")
st.caption("Seleziona la tua rosa, imposta gli indici e l'algoritmo calcolerà il modulo e gli 11 titolari perfetti.")

# --- DATABASE ROSA DIMOSTRATIVA / MODIFICABILE ---
if "rosa" not in st.setdefault("rosa", {}):
    st.session_state.rosa = [
        # Portieri (P)
        {"nome": "Maignan", "ruolo": "P", "indice": 7.5, "disponibile": True},
        {"nome": "Sportiello", "ruolo": "P", "indice": 6.0, "disponibile": True},
        # Difensori (D)
        {"nome": "Dimarco", "ruolo": "D", "indice": 8.2, "disponibile": True},
        {"nome": "Theo Hernandez", "ruolo": "D", "indice": 7.8, "disponibile": True},
        {"nome": "Bremer", "ruolo": "D", "indice": 7.1, "disponibile": True},
        {"nome": "Di Lorenzo", "ruolo": "D", "indice": 6.8, "disponibile": True},
        {"nome": "Buongiorno", "ruolo": "D", "indice": 6.5, "disponibile": True},
        {"nome": "Bastoni", "ruolo": "D", "indice": 6.0, "disponibile": False}, # Es. Infortunato
        # Centrocampisti (C)
        {"nome": "Pulisic", "ruolo": "C", "indice": 8.5, "disponibile": True},
        {"nome": "Barella", "ruolo": "C", "indice": 7.4, "disponibile": True},
        {"nome": "Koopmeiners", "ruolo": "C", "indice": 7.2, "disponibile": True},
        {"nome": "Calhanoglu", "ruolo": "C", "indice": 7.0, "disponibile": True},
        {"nome": "Zaccagni", "ruolo": "C", "indice": 6.9, "disponibile": True},
        {"nome": "Loftus-Cheek", "ruolo": "C", "indice": 6.2, "disponibile": True},
        # Attaccanti (A)
        {"nome": "Lautaro Martinez", "ruolo": "A", "indice": 8.8, "disponibile": True},
        {"nome": "Vlahovic", "ruolo": "A", "indice": 8.0, "disponibile": True},
        {"nome": "Lookman", "ruolo": "A", "indice": 7.6, "disponibile": True},
        {"nome": "Retegui", "ruolo": "A", "indice": 7.3, "disponibile": True},
        {"nome": "Dybala", "ruolo": "A", "indice": 6.1, "disponibile": True},
    ]

tab_formazione, tab_rosa = st.tabs(["🚀 Genera 11 Titolare", "📋 Gestisci la tua Rosa"])

# --- TAB 1: CALCOLO FORMAZIONE E MODULO MIGLIORE ---
with tab_formazione:
    st.subheader("🤖 Algoritmo Consigliatore Formazione")
    st.write("L'algoritmo valuta tutti i moduli possibili (3-4-3, 4-3-3, 3-5-2, 4-4-2, 4-5-1, 5-3-2) e sceglie la combinazione con il punteggio complessivo più alto.")
    
    # Filtra solo i giocatori disponibili
    disponibili = [p for p in st.session_state.rosa if p["disponibile"]]
    
    portieri = sorted([p for p in disponibili if p["ruolo"] == "P"], key=lambda x: x["indice"], reverse=True)
    difensori = sorted([p for p in disponibili if p["ruolo"] == "D"], key=lambda x: x["indice"], reverse=True)
    centrocampisti = sorted([p for p in disponibili if p["ruolo"] == "C"], key=lambda x: x["indice"], reverse=True)
    attaccanti = sorted([p for p in disponibili if p["ruolo"] == "A"], key=lambda x: x["indice"], reverse=True)

    # Elenco moduli standard: (Difensori, Centrocampisti, Attaccanti)
    moduli = {
        "3-4-3": (3, 4, 3),
        "4-3-3": (4, 3, 3),
        "3-5-2": (3, 5, 2),
        "4-4-2": (4, 4, 2),
        "4-5-1": (4, 5, 1),
        "5-3-2": (5, 3, 2),
    }

    if st.button("⚡ Calcola Miglior Formazione & Modulo", type="primary", use_container_width=True):
        if not portieri or len(difensori) < 3 or len(centrocampisti) < 3 or len(attaccanti) < 1:
            st.error("⚠️ Non hai abbastanza giocatori disponibili per schierare una formazione!")
        else:
            miglior_punteggio = -1
            miglior_modulo = ""
            miglior_tit_11 = []

            # Simulazione di ogni modulo
            for nome_m, (num_d, num_c, num_a) in moduli.items():
                if len(difensori) >= num_d and len(centrocampisti) >= num_c and len(attaccanti) >= num_a:
                    
                    tit_p = portieri[:1]
                    tit_d = difensori[:num_d]
                    tit_c = centrocampisti[:num_c]
                    tit_a = attaccanti[:num_a]
                    
                    squadra = tit_p + tit_d + tit_c + tit_a
                    punteggio_totale = sum(p["indice"] for p in squadra)
                    
                    if punteggio_totale > miglior_punteggio:
                        miglior_punteggio = punteggio_totale
                        miglior_modulo = nome_m
                        miglior_tit_11 = squadra

            # RISULTATO
            st.success(f"🌟 **Modulo Consigliato per questa giornata: {miglior_modulo}** (Punteggio Algo: {round(miglior_punteggio, 2)})")
            st.divider()

            # SCHERMATA TITOLARI
            col_p, col_d, col_c, col_a = st.columns(4)
            
            with col_p:
                st.markdown("### 🧤 Portiere")
                for p in [x for x in miglior_tit_11 if x["ruolo"] == "P"]:
                    st.info(f"**{p['nome']}** (Indice: {p['indice']})")
                    
            with col_d:
                st.markdown("### 🛡️ Difesa")
                for p in [x for x in miglior_tit_11 if x["ruolo"] == "D"]:
                    st.info(f"**{p['nome']}** (Indice: {p['indice']})")

            with col_c:
                st.markdown("### ⚙️ Centrocampo")
                for p in [x for x in miglior_tit_11 if x["ruolo"] == "C"]:
                    st.info(f"**{p['nome']}** (Indice: {p['indice']})")

            with col_a:
                st.markdown("### ⚽ Attacco")
                for p in [x for x in miglior_tit_11 if x["ruolo"] == "A"]:
                    st.info(f"**{p['nome']}** (Indice: {p['indice']})")

# --- TAB 2: GESTIONE ROSA & INDICI GIORNATA ---
with tab_rosa:
    st.subheader("Gestione Rosa e Indice di Schierabilità del Turno")
    st.write("Aggiorna la titolarità/forma dei tuoi calciatori o aggiungi nuovi nomi.")
    
    # Inserimento veloce nuovo giocatore
    with st.expander("➕ Aggiungi un nuovo calciatore alla Rosa"):
        col_n1, col_n2, col_n3 = st.columns(3)
        nuovo_nome = col_n1.text_input("Nome Calciatore")
        nuovo_ruolo = col_n2.selectbox("Ruolo", ["P", "D", "C", "A"])
        nuovo_idx = col_n3.number_input("Indice Forma/Partita", 1.0, 10.0, 6.0)
        if st.button("Aggiungi in Rosa"):
            if nuovo_nome:
                st.session_state.rosa.append({"nome": nuovo_nome, "ruolo": nuovo_ruolo, "indice": nuovo_idx, "disponibile": True})
                st.rerun()

    st.divider()
    
    # Tabella modifica veloce
    for i, giocatore in enumerate(st.session_state.rosa):
        c1, c2, c3, c4 = st.columns([3, 2, 3, 2])
        c1.write(f"**{giocatore['nome']}** ({giocatore['ruolo']})")
        
        # Modifica indice della settimana
        nuovo_ind = c2.number_input(f"Indice", 1.0, 10.0, float(giocatore["indice"]), key=f"idx_{i}")
        st.session_state.rosa[i]["indice"] = nuovo_ind
        
        # Checkbox disponibilità (infortuni/squalifiche)
        disp = c3.checkbox("Disponibile questa giornata", value=giocatore["disponibile"], key=f"disp_{i}")
        st.session_state.rosa[i]["disponibile"] = disp
        
        if c4.button("❌ Rimuovi", key=f"del_{i}"):
            st.session_state.rosa.pop(i)
            st.rerun()
