import streamlit as st
import os

# Configurazione della pagina wide per occupare tutto lo schermo
st.set_page_config(page_title="Poker Range Dashboard", layout="wide", page_icon="🃏")

# --- STYLING CSS CUSTOM ---
# Questo blocco nasconde i menu di Streamlit e centra/ingrandisce l'immagine
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stSidebar"] {
            background-color: #f0f2f6;
        }
        [data-testid="stImage"] {
            display: flex;
            justify-content: center;
        }
        [data-testid="stImage"] img {
            max-width: 90% !important;
            height: auto;
            border: 2px solid #31333F;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

IMAGE_DIR = "immagini_poker"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -------------------------------------------------------------------------
# BARRA LATERALE (SIDEBAR): TUTTI I FILTRI SONO QUI ORA
# -------------------------------------------------------------------------
with st.sidebar:
    st.header("🎮 Controlli Sessione")
    st.markdown("---")
    
    # 1. SCENARIO PRINCIPALE
    scenario = st.radio(
        "🔥 Scegli l'Azione:",
        ["RFI", "3 Betting", "Cold Calling", "Difesa Bui", "Iso Raise", "Over Limping", "Over Calling"],
        index=0
    )
    st.markdown("---")
    
    # Inizializziamo le variabili per il calcolo del percorso
    cartella_scenario = ""
    sottocartella_stile = ""
    nome_file_principale = ""
    nome_file_bluff = ""
    info_regola = ""
    stile_label = ""
    pos_label = ""

    # Logica dei sotto-filtri all'interno della sidebar
    if scenario == "RFI":
        cartella_scenario = "RFI"
        stile = st.radio("🛡️ Approccio:", ["Conservative", "Moderate"], horizontal=True)
        sottocartella_stile = stile.upper()
        stile_label = stile
        pos = st.radio(" Tua Posizione:", ["UTG", "MP", "CO", "BTN", "SB"])
        nome_file_principale = f"{pos.lower()}.jpg"
        pos_label = pos

    elif scenario == "3 Betting":
        cartella_scenario = "3 BETTING"
        stile = st.radio("⚔️ Approccio:", ["Conservative", "Moderate"], horizontal=True)
        sottocartella_stile = stile.upper()
        stile_label = stile
        or_pos = st.radio("Oppo openraise da:", ["UTG", "MP", "CO", "BTN", "SB"])
        nome_file_principale = f"vs_{or_pos.lower()}.jpg"
        nome_file_bluff = "3_bet_bluff.jpg"
        pos_label = or_pos

    elif scenario == "Cold Calling":
        cartella_scenario = "COLD CALLING"
        stile = st.radio("🔹 Approccio:", ["Conservative", "Moderate"], horizontal=True)
        sottocartella_stile = stile.upper()
        stile_label = stile
        vs_pos = st.radio("Oppo openraise da:", ["UTG", "MP", "CO"])
        nome_file_principale = f"vs_{vs_pos.lower()}.jpg"
        pos_label = vs_pos

    elif scenario == "Difesa Bui":
        cartella_scenario = "DIFESA BUI"
        azione_buio = st.radio("Tua Intenzione:", ["3_Bet", "Call"])
        nome_file_principale = f"{azione_buio.lower()}.jpg"
        pos_label = azione_buio

    elif scenario == "Iso Raise":
        cartella_scenario = "ISO RAISE"
        stile = st.radio(" Approccio:", ["Conservativo", "Moderato"], horizontal=True)
        nome_file_principale = f"iso_raise_{stile.lower()}.jpg"
        stile_label = stile

    elif scenario == "Over Limping":
        cartella_scenario = "OVER LIMPING"
        nome_file_principale = "over_limping.jpg"
        info_regola = "⚠️ REGOLA: Se c'è rischio Raise o Iso Raise -> NO OVER LIMP."

    elif scenario == "Over Calling":
        cartella_scenario = "OVER CALLING"
        nome_file_principale = "over_calling.jpg"

    st.markdown("---")
    st.image("https://poker-ranges.com/img/poker-icon.png", width=50)


# -------------------------------------------------------------------------
# AREA PRINCIPALE: VISUALIZZAZIONE GIGANTE
# -------------------------------------------------------------------------

# Calcolo del percorso
if sottocartella_stile:
    path_principale = os.path.join(BASE_DIR, IMAGE_DIR, cartella_scenario, sottocartella_stile, nome_file_principale)
    path_bluff = os.path.join(BASE_DIR, IMAGE_DIR, cartella_scenario, sottocartella_stile, nome_file_bluff) if nome_file_bluff else ""
else:
    path_principale = os.path.join(BASE_DIR, IMAGE_DIR, cartella_scenario, nome_file_principale)
    path_bluff = os.path.join(BASE_DIR, IMAGE_DIR, cartella_scenario, nome_file_bluff) if nome_file_bluff else ""


# Titolo dinamico in cima per ricordare cosa stai guardando
st.markdown(f"## {scenario} {stile_label} - {pos_label}")

if info_regola:
    st.info(info_regola)

# Rendering grafico gigante
if nome_file_bluff:
    col_cc1, col_cc2 = st.columns(2)
    with col_cc1:
        if os.path.exists(path_principale):
            st.image(path_principale, caption="Value Range", use_column_width=True)
        else:
            st.error(f"File mancante: `{IMAGE_DIR}/{cartella_scenario}/{sottocartella_stile}/{nome_file_principale}`")
    with col_cc2:
        if os.path.exists(path_bluff):
            st.image(path_bluff, caption="Bluff Range", use_column_width=True)
        else:
            st.error(f"File mancante: `{IMAGE_DIR}/{cartella_scenario}/{sottocartella_stile}/{nome_file_bluff}`")
else:
    if os.path.exists(path_principale):
        # use_column_width=True rende l'immagine enorme nella colonna principale
        st.image(path_principale, use_column_width=True)
    else:
        st.error(f"❌ Immagine non trovata! Controlla percorso e case-sensitive.")
