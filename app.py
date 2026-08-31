import streamlit as st
import pandas as pd

# 1. Configurazione della pagina
st.set_page_config(
    page_title="FantaIA Assistant v0.1.0",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Immagini per lo sfondo e il martello 3D
URL_SFONDO_STADIO = "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?q=80&w=1920&auto=format&fit=crop"
URL_MARTELLO_ASTA = "https://cdn3d.iconscout.com/3d/premium/thumb/auction-gavel-4721151-3927976.png"

# 2. INIZIALIZZAZIONE "QUADERNO DI MEMORIA" (Session State)
if "budget_iniziale" not in st.session_state:
    st.session_state.budget_iniziale = 500

if "rosa" not in st.session_state:
    # Struttura di ogni calciatore: {"nome": str, "squadra": str, "ruolo": str, "prezzo": int}
    st.session_state.rosa = []

# Slot standard Fantacalcio
SLOT_MAX = {"P": 3, "D": 8, "C": 8, "A": 6}

# 3. CSS Avanzato (Unione Grafica v0.0.4 + Stile Input Form)
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

    /* Pulsanti di navigazione */
    div[data-baseweb="tab-list"] {{
        justify-content: center !important;
        gap: 10px !important;
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
        padding: 8px 16px !important;
        transition: all 0.25s ease-in-out !important;
    }}

    button[data-baseweb="tab"] p {{
        color: #d1d5db !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
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

    /* Card Generali */
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
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 4. Header Visivo
st.markdown("""
<div class="header-container">
    <h1 style="margin:0; font-size:1.8rem; color:#ffffff;">⚽ FantaIA Assistant</h1>
    <span class="version-badge">v0.1.0 - Modulo Asta Attivo</span>
</div>
""", unsafe_allow_html=True)

# 5. Navigazione a Schede
tab_home, tab_asta, tab_formazione, tab_scambi = st.tabs([
    "🏠 Home", 
    "🔨 Asta", 
    "📋 Formazione", 
    "🔄 Scambi"
])

# --- CALCOLI DINAMICI BUDGET & SLOT ---
crediti_spesi = sum(p["prezzo"] for p in st.session_state.rosa)
crediti_rimasti = st.session_state.budget_iniziale - crediti_spesi

# Conteggio giocatori per ruolo
conteggio_ruoli = {"P": 0, "D": 0, "C": 0, "A": 0}
for p in st.session_state.rosa:
    if p["ruolo"] in conteggio_ruoli:
        conteggio_ruoli[p["ruolo"]] += 1

totale_giocatori = len(st.session_state.rosa)
slot_mancanti_totali = 25 - totale_giocatori

# --- CONTENUTO SCHEDE ---

with tab_home:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">📊 Riepilogo Generato dall'IA</div>
        <p style="color:#cbd5e0; font-size:0.9rem;">
            Ecco lo stato attuale della tua squadra durante l'asta:
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Crediti Iniziali", value=f"{st.session_state.budget_iniziale} FM")
    with col2:
        st.metric(label="Crediti Spesi", value=f"{crediti_spesi} FM")
    with col3:
        st.metric(label="Crediti Rimasti", value=f"{crediti_rimasti} FM")

    st.markdown("<br/>", unsafe_allow_html=True)
    st.subheader("📋 Composizione Rosa")
    col_p, col_d, col_c, col_a = st.columns(4)
    with col_p:
        st.metric(label="Portieri", value=f"{conteggio_ruoli['P']} / 3")
    with col_d:
        st.metric(label="Difensori", value=f"{conteggio_ruoli['D']} / 8")
    with col_c:
        st.metric(label="Centrocampisti", value=f"{conteggio_ruoli['C']} / 8")
    with col_a:
        st.metric(label="Attaccanti", value=f"{conteggio_ruoli['A']} / 6")


with tab_asta:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">🔨 Centro Operativo Asta Live</div>
        <p style="color:#cbd5e0; font-size:0.9rem; margin-bottom:0;">
            Imposta il budget iniziale, registra ogni acquisto e segui i suggerimenti dell'IA.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Impostazione Budget Iniziale
    with st.expander("⚙️ Configurazione Budget Asta", expanded=False):
        nuovo_budget = st.number_input(
            "Budget Iniziale (Crediti Totali):", 
            min_value=100, 
            max_value=2000, 
            value=st.session_state.budget_iniziale, 
            step=50
        )
        if st.button("Aggiorna Budget Iniziale"):
            st.session_state.budget_iniziale = nuovo_budget
            st.rerun()

    # Form Registrazione Rapida Giocatore
    st.markdown("### 🛒 Registra un Acquisto")
    with st.form("form_acquisto", clear_on_submit=True):
        col_nome, col_squadra = st.columns([2, 1])
        with col_nome:
            nome_giocatore = st.text_input("Nome Calciatore", placeholder="es. Lautaro Martinez")
        with col_squadra:
            squadra_serie_a = st.text_input("Squadra", placeholder="es. Inter")

        col_ruolo, col_prezzo = st.columns([1, 1])
        with col_ruolo:
            ruolo = st.selectbox("Ruolo", options=["P", "D", "C", "A"])
        with col_prezzo:
            prezzo = st.number_input("Prezzo d'Asta (FM)", min_value=1, max_value=crediti_rimasti if crediti_rimasti > 0 else 1, value=1)

        submit_btn = st.form_submit_button("✅ Aggiungi alla Tua Rosa")

        if submit_btn:
            if nome_giocatore.strip() == "":
                st.error("Inserisci il nome del calciatore!")
            elif conteggio_ruoli[ruolo] >= SLOT_MAX[ruolo]:
                st.warning(f"Hai già raggiunto il limite massimo di {SLOT_MAX[ruolo]} per il ruolo {ruolo}!")
            else:
                # Salva nel quaderno di memoria
                st.session_state.rosa.append({
                    "nome": nome_giocatore.strip(),
                    "squadra": squadra_serie_a.strip().upper(),
                    "ruolo": ruolo,
                    "prezzo": int(prezzo)
                })
                st.success(f"{nome_giocatore} aggiunto con successo per {prezzo} FM!")
                st.rerun()

    st.markdown("---")

    # Consigliere IA di Spesa
    st.markdown("### 💡 Consigliere IA Budget Massimo")
    if slot_mancanti_totali > 0:
        # Riserva minima 1 FM per ogni slot rimasto da coprire
        riserva_altri_slot = slot_mancanti_totali - 1
        max_spendibile_singolo = max(1, crediti_rimasti - riserva_altri_slot)
        
        st.info(f"💰 **Crediti Rimasti:** `{crediti_rimasti} FM` | **Slot da completare:** `{slot_mancanti_totali}`\n\n"
                f"⚠️ **Prezzo Max Consigliato per 1 top player:** `{max_spendibile_singolo} FM` *(ti permetterà di comprare tutti i restanti calciatori a 1 FM)*.")
    else:
        st.success("🎉 Complimenti! Hai completato la tua rosa di 25 giocatori!")

    st.markdown("---")

    # Lista e Gestione della Rosa Acquistata
    st.markdown("### 📋 La Tua Rosa Acquistata")
    if len(st.session_state.rosa) == 0:
        st.write("Nessun calciatore acquistato finora. Compila il modulo in alto per iniziare!")
    else:
        # Visualizzazione calciatori per ruolo
        for r_code, r_name in [("P", "Portieri"), ("D", "Difensori"), ("C", "Centrocampisti"), ("A", "Attaccanti")]:
            giocatori_ruolo = [p for p in st.session_state.rosa if p["ruolo"] == r_code]
            if giocatori_ruolo:
                st.markdown(f"#### <span class='role-badge badge-{r_code.lower()}'>{r_code}</span> {r_name} ({len(giocatori_ruolo)}/{SLOT_MAX[r_code]})", unsafe_allow_html=True)
                for idx, player in enumerate(st.session_state.rosa):
                    if player["ruolo"] == r_code:
                        col_info, col_del = st.columns([4, 1])
                        with col_info:
                            st.write(f"• **{player['nome']}** ({player['squadra']}) — **{player['prezzo']} FM**")
                        with col_del:
                            if st.button("❌", key=f"del_{idx}"):
                                st.session_state.rosa.pop(idx)
                                st.rerun()

        # Pulsante Reset Totale
        st.markdown("<br/>", unsafe_allow_html=True)
        if st.button("🗑️ Svuota Rosa e Ricomincia Asta"):
            st.session_state.rosa = []
            st.rerun()


with tab_formazione:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">📋 Assistente Schieramento (In arrivo nella v0.2.0)</div>
        <p style="color:#cbd5e0; font-size:0.9rem;">
            Nella versione 0.2.0, l'IA analizzerà i giocatori acquistati nella rosa sopra e ti dirà chi schierare titolare giornata per giornata!
        </p>
    </div>
    """, unsafe_allow_html=True)

with tab_scambi:
    st.markdown("""
    <div class="fanta-card">
        <div class="fanta-card-title">🔄 Area Scambi (In arrivo nella v0.3.0)</div>
        <p style="color:#cbd5e0; font-size:0.9rem;">Sezione riservata al calcolatore convenienza trade.</p>
    </div>
    """, unsafe_allow_html=True)
