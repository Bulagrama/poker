import streamlit as st
import os

st.set_page_config(page_title="Poker Range Elite Dashboard", layout="wide", page_icon="🃏")

st.title("🃏 Texas Hold'em Professional Range Dashboard")
st.write("Sincronizzato dinamicamente con la struttura delle cartelle di GitHub.")

IMAGE_DIR = "immagini_poker"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. SELEZIONE DELLO SCENARIO PRINCIPALE (Combacia con i nomi delle tue cartelle)
st.write("### 1. Seleziona lo Scenario Pre-Flop")
scenario = st.radio(
    "Scenario Attuale:",
    ["RFI", "3 Betting", "Cold Calling", "Difesa Bui", "Iso Raise", "Over Limping", "Over Calling"],
    horizontal=True
)

st.write("---")

# Variabili per calcolare il percorso finale del file
cartella_scenario = ""
sottocartella_stile = ""
nome_file_principale = ""
nome_file_bluff = ""
info_regola = ""

# Mappiamo i selettori in base alle tue cartelle reali
if scenario == "RFI":
    cartella_scenario = "rfi"
    st.write("### 2. Seleziona lo Stile di Gioco:")
    stile = st.radio("Approccio:", ["Conservative", "Moderate"], horizontal=True)
    sottocartella_stile = stile.lower()
    
    st.write("### 3. Tua Posizione:")
    pos = st.radio("Posizione:", ["UTG", "MP", "CO", "BTN", "SB"], horizontal=True)
    nome_file_principale = f"{pos.lower()}.jpg"

elif scenario == "3 Betting":
    cartella_scenario = "3 betting"
    st.write("### 2. Seleziona lo Stile di Gioco:")
    stile = st.radio("Approccio:", ["Conservative", "Moderate"], horizontal=True)
    sottocartella_stile = stile.lower()
    
    st.write("### 3. Posizione dell'Original Raiser:")
    or_pos = st.radio("Oppo openraise da:", ["UTG", "MP", "CO", "BTN", "SB"], horizontal=True)
    nome_file_principale = f"vs_{or_pos.lower()}.jpg"
    nome_file_bluff = "3_bet_bluff.jpg"  # Affiancato automaticamente

elif scenario == "Cold Calling":
    cartella_scenario = "cold calling"
    st.write("### 2. Seleziona lo Stile di Gioco:")
    stile = st.radio("Approccio:", ["Conservative", "Moderate"], horizontal=True)
    sottocartella_stile = stile.lower()
    
    st.write("### 3. Posizione dell'Original Raiser:")
    vs_pos = st.radio("Oppo openraise da:", ["UTG", "MP", "CO"], horizontal=True)
    nome_file_principale = f"vs_{vs_pos.lower()}.jpg"

elif scenario == "Difesa Bui":
    cartella_scenario = "difesa bui"
    # NON impostiamo sottocartella_stile perché come hai detto qui NON c'è conservative/moderate
    st.write("### 2. Che azione vuoi fare dal buio?")
    azione_buio = st.radio("Tua Azione:", ["3_Bet", "Call"], horizontal=True)
    nome_file_principale = f"{azione_buio.lower()}.jpg"

elif scenario == "Iso Raise":
    cartella_scenario = "iso raise"
    # Qui carichi direttamente il file specifico (es. iso_raise_conservativo.jpg) alla radice o dove si trova
    st.write("### 2. Seleziona lo Stile di Gioco:")
    stile = st.radio("Approccio:", ["Conservativo", "Moderato"], horizontal=True)
    nome_file_principale = f"iso_raise_{stile.lower()}.jpg"

elif scenario == "Over Limping":
    cartella_scenario = "over limping"
    nome_file_principale = "over_limping.jpg"
    info_regola = "⚠️ **REGOLA:** Se dopo di noi c'è un giocatore AGGRESSIVO con rischio Raise o Iso Raise -> NO OVER LIMP, ma fai solo ISO RAISE."

elif scenario == "Over Calling":
    cartella_scenario = "over calling"
    nome_file_principale = "over_calling.jpg"

# -------------------------------------------------------------------------
# COMPOSIZIONE DINAMICA DEL PERCORSO (Senza errori di cartelle vuote)
# -------------------------------------------------------------------------
if sottocartella_stile:
    path_principale = os.path.join(BASE_DIR, IMAGE_DIR, cartella_scenario, sottocartella_stile, nome_file_principale)
    path_bluff = os.path.join(BASE_DIR, IMAGE_DIR, cartella_scenario, sottocartella_stile, nome_file_bluff) if nome_file_bluff else ""
else:
    path_principale = os.path.join(BASE_DIR, IMAGE_DIR, cartella_scenario, nome_file_principale)
    path_bluff = os.path.join(BASE_DIR, IMAGE_DIR, cartella_scenario, nome_file_bluff) if nome_file_bluff else ""

# Rendering grafico
if info_regola:
    st.warning(info_regola)

# Debug log per aiutarti a vedere dove l'app sta cercando il file
st.caption(f"🔎 Controllo percorso: `{path_principale.replace(BASE_DIR, '')}`")

if nome_file_bluff:
    col1, col2 = st.columns(2)
    with col1:
        if os.path.exists(path_principale):
            st.image(path_principale, caption=f"Value Range ({stile})", width=460)
        else:
            st.error(f"File mancante in: `{cartella_scenario}/{sottocartella_stile}/{nome_file_principale}`")
    with col2:
        if os.path.exists(path_bluff):
            st.image(path_bluff, caption="3-Bet Bluff Range", width=460)
        else:
            st.error(f"File mancante in: `{cartella_scenario}/{sottocartella_stile}/{nome_file_bluff}`")
else:
    if os.path.exists(path_principale):
        st.image(path_principale, caption=f"Range: {scenario}", width=520)
    else:
        st.error(f"❌ Immagine non trovata! Controlla di averla posizionata nel percorso corretto.")
