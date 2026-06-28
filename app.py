import streamlit as st
import os

st.set_page_config(page_title="Poker Range Elite Dashboard", layout="wide", page_icon="🃏")

st.title("🃏 Texas Hold'em Professional Range Dashboard")
st.write("Sincronizzato al 100% con la tua struttura di file .jpg")

IMAGE_DIR = "immagini_poker"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. BARRA LATERALE: APPROCCIO GENERALE
st.sidebar.header("🛡️ / ⚔️ Approccio al Tavolo")
atteggiamento = st.sidebar.radio(
    "Seleziona lo Stile:",
    ["Conservative", "Moderate"],
    index=0
)
cartella_stile = atteggiamento.lower()

# 2. SELEZIONE DELLO SCENARIO
st.write("### 1. Seleziona lo Scenario Pre-Flop")
scenario = st.radio(
    "Scenario Attuale:",
    ["RFI", "3 Betting", "Cold Calling", "Difesa Bui", "Iso Raise", "Over Limping", "Over Calling"],
    horizontal=True
)

st.write("---")

nome_file_principale = ""
nome_file_bluff = ""
info_regola = ""

# 3. ASSOCIAZIONE NOMI FILE SECONDO LE TUE IMMAGINI
if scenario == "RFI":
    st.write("### 2. Tua Posizione:")
    pos = st.radio("Posizione:", ["UTG", "MP", "CO", "BTN", "SB"], horizontal=True)
    nome_file_principale = f"{pos.lower()}.jpg"

elif scenario == "3 Betting":
    st.write("### 2. Posizione dell'Original Raiser:")
    or_pos = st.radio("Oppo openraise da:", ["UTG", "MP", "CO", "BTN", "SB"], horizontal=True)
    nome_file_principale = f"vs_{or_pos.lower()}.jpg"
    nome_file_bluff = "3_bet_bluff.jpg"  # Mostrato sempre affiancato

elif scenario == "Cold Calling":
    st.write("### 2. Posizione dell'Original Raiser:")
    vs_pos = st.radio("Oppo openraise da:", ["UTG", "MP", "CO"], horizontal=True)
    nome_file_principale = f"vs_{vs_pos.lower()}.jpg"

elif scenario == "Difesa Bui":
    st.write("### 2. In che posizione sei?")
    tua_pos = st.radio("Tuo Buio:", ["SB", "BB"], horizontal=True)
    st.write("### 3. Che azione valuti?")
    tua_azione = st.radio("Azione:", ["3_Bet", "Call"], horizontal=True)
    nome_file_principale = f"{tua_pos.lower()}_{tua_azione.lower()}.jpg"

elif scenario == "Iso Raise":
    # Carica la variante corretta in base al toggle laterale
    nome_file_principale = f"iso_raise_{cartella_stile}.jpg"

elif scenario == "Over Limping":
    nome_file_principale = "over_limping.jpg"
    info_regola = "⚠️ **REGOLA:** Se dopo di noi c'è un giocatore AGGRESSIVO con rischio Raise o Iso Raise -> NO OVER LIMP, ma fai solo ISO RAISE."

elif scenario == "Over Calling":
    nome_file_principale = "over_calling.jpg"

# 4. CARICAMENTO E RENDERING VISIVO
if info_regola:
    st.warning(info_regola)

path_principale = os.path.join(BASE_DIR, IMAGE_DIR, cartella_stile, nome_file_principale)

if nome_file_bluff:
    path_bluff = os.path.join(BASE_DIR, IMAGE_DIR, cartella_stile, nome_file_bluff)
    col1, col2 = st.columns(2)
    
    with col1:
        if os.path.exists(path_principale):
            st.image(path_principale, caption=f"3-Bet Value vs {or_pos}", width=460)
        else:
            st.error(f"Manca file: `immagini_poker/{cartella_stile}/{nome_file_principale}`")
    with col2:
        if os.path.exists(path_bluff):
            st.image(path_bluff, caption="Schema 3-Bet Bluff (Sempre visibile)", width=460)
        else:
            st.error(f"Manca file: `immagini_poker/{cartella_stile}/{nome_file_bluff}`")
else:
    if os.path.exists(path_principale):
        st.image(path_principale, caption=f"{scenario} ({atteggiamento})", width=520)
    else:
        st.error(f"❌ Immagine non trovata nel percorso: `immagini_poker/{cartella_stile}/{nome_file_principale}`")
