import streamlit as st

# Configurazione della pagina per smartphone
st.set_page_config(page_title="FantaIA v0.0.1", page_icon="⚽", layout="centered")

# Intestazione della v0.0.1
st.title("⚽ Fantacalcio AI")
st.caption("Versione 0.0.1 - Base Operativa")

st.success("App creata con successo!")
st.write("Benvenuto nel tuo assistente personale. Questa schermata conferma che l'infrastruttura è attiva e pronta per i moduli IA.")

# Menu navigazione di prova per la v0.0.1
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "🔨 Asta", "📋 Formazione", "🔄 Scambi"])

with tab1:
    st.subheader("Stato del Sistema")
    st.write("Nessun dato caricato. In attesa degli aggiornamenti.")

with tab2:
    st.subheader("Modulo Asta")
    st.info("In arrivo nella versione 0.1.0")

with tab3:
    st.subheader("Assistente Schieramento")
    st.info("In arrivo nella versione 0.2.0")

with tab4:
    st.subheader("Radar Scambi")
    st.info("In arrivo nella versione 0.3.0")
