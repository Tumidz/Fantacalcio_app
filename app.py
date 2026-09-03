import streamlit as st

# Configurazione della pagina
st.set_page_config(page_title="FantaAlgo Free", page_icon="⚽", layout="wide")

st.title("⚽ Algo Fanta-Assistant (Versione Integrale Gratis)")
st.caption("Il tuo algoritmo gratuito per Formazioni, Ballottaggi, Scambi e Asta")

# Creazione delle schede principali
tab1, tab2, tab3 = st.tabs(["📊 Ballottaggi & Formazione", "🔄 Valutatore Scambi", "💰 Assistente Asta"])

# --- TAB 1: BALLOTTAGGI E FORMAZIONE ---
with tab1:
    st.header("Risoluzione Ballottaggi")
    st.write("Inserisci le statistiche per mettere a confronto due giocatori.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Giocatore 1")
        nome1 = st.text_input("Nome", "Giocatore A", key="n1")
        mv1 = st.number_input("Media Voto (es. 6.3)", 5.0, 10.0, 6.3, step=0.1, key="mv1")
        forma1 = st.number_input("Forma ultime 3 gare", 5.0, 10.0, 6.8, step=0.1, key="f1")
        diff1 = st.slider("Difficoltà Partita (1=Facile, 5=Difficile)", 1, 5, 2, key="d1")
        tit1 = st.slider("Titolarità stimata (%)", 0, 100, 90, key="t1") / 100.0

    with col2:
        st.subheader("Giocatore 2")
        nome2 = st.text_input("Nome", "Giocatore B", key="n2")
        mv2 = st.number_input("Media Voto (es. 7.0)", 5.0, 10.0, 7.0, step=0.1, key="mv2")
        forma2 = st.number_input("Forma ultime 3 gare", 5.0, 10.0, 6.5, step=0.1, key="f2")
        diff2 = st.slider("Difficoltà Partita (1=Facile, 5=Difficile)", 1, 5, 5, key="d2")
        tit2 = st.slider("Titolarità stimata (%)", 0, 100, 100, key="t2") / 100.0

    def calcola_indice(mv, forma, diff, tit):
        fattore_match = (6 - diff) * 1.2
        base = (mv * 0.35) + (forma * 0.35) + (fattore_match * 0.30)
        return round(base * (0.5 + (tit * 0.5)), 2)

    if st.button("🚀 Calcola chi schierare", type="primary"):
        score1 = calcola_indice(mv1, forma1, diff1, tit1)
        score2 = calcola_indice(mv2, forma2, diff2, tit2)
        
        st.divider()
        res_col1, res_col2 = st.columns(2)
        res_col1.metric(f"Indice {nome1}", score1)
        res_col2.metric(f"Indice {nome2}", score2)
        
        if score1 > score2:
            st.success(f"👉 **Consiglio:** Schiera **{nome1}**! È in vantaggio di {round(score1 - score2, 2)} punti.")
        elif score2 > score1:
            st.success(f"👉 **Consiglio:** Schiera **{nome2}**! È in vantaggio di {round(score2 - score1, 2)} punti.")
        else:
            st.info("⚖️ I giocatori si equivalgono esattamente nei calcoli.")

# --- TAB 2: VALUTATORE SCAMBI ---
with tab2:
    st.header("Analisi Convenienza Scambio")
    st.write("Confronta il valore dei calciatori che dai via con quelli che ricevi.")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.subheader("🔴 Tuoi calciatori CEDUTI")
        p_ceduti = st.number_input("Somma Medie Voto uscite", 5.0, 30.0, 12.5, step=0.1)
        f_ceduti = st.number_input("Somma Forma ultime gare uscite", 5.0, 30.0, 13.0, step=0.1)
    
    with col_s2:
        st.subheader("🟢 Calciatori che RICEVI")
        p_ricevuti = st.number_input("Somma Medie Voto entrate", 5.0, 30.0, 13.8, step=0.1)
        f_ricevuti = st.number_input("Somma Forma ultime gare entrate", 5.0, 30.0, 13.2, step=0.1)
        
    if st.button("⚖️ Valuta Scambio ora", type="primary"):
        val_ceduti = (p_ceduti * 0.6) + (f_ceduti * 0.4)
        val_ricevuti = (p_ricevuti * 0.6) + (f_ricevuti * 0.4)
        diff = round(val_ricevuti - val_ceduti, 2)
        
        st.divider()
        if diff > 0.4:
            st.success(f"✅ **SCAMBIO CONVENIENTE!** Guadagni +{diff} punti di struttura rosa.")
        elif diff < -0.4:
            st.error(f"❌ **SCAMBIO SCONVENIENTE!** Perdi {abs(diff)} punti di struttura rosa.")
        else:
            st.warning("⚠️ **SCAMBIO EQUILIBRATO.** L'impatto complessivo sulla rosa è neutro.")

# --- TAB 3: ASSISTENTE ASTA ---
with tab3:
    st.header("Scout d'Asta & Budget Strategico")
    budget = st.number_input("Inserisci il tuo Budget totale crediti (es. 500)", 100, 2000, 500, step=50)
    
    st.subheader("Budget Massimo Consigliato per Slot")
    col_a1, col_a2, col_a3, col_a4 = st.columns(4)
    
    with col_a1:
        st.metric("1° Top Attacco", f"{int(budget * 0.32)} cr")
        st.caption("Max 32% del budget")
    with col_a2:
        st.metric("2° Slot Attacco", f"{int(budget * 0.18)} cr")
        st.caption("Max 18% del budget")
    with col_a3:
        st.metric("Top Centrocampo", f"{int(budget * 0.12)} cr")
        st.caption("Max 12% del budget")
    with col_a4:
        st.metric("Top Difesa", f"{int(budget * 0.07)} cr")
        st.caption("Max 7% del budget")
