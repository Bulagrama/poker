import streamlit as st
import os

# Configurazione della pagina wide per occupare tutto lo schermo
st.set_page_config(page_title="Poker Range Dashboard", layout="wide", page_icon="🃏")

# --- STYLING CSS CUSTOM ---
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
# BARRA LATERALE (SIDEBAR): TUTTI I FILTRI SONO QUI
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
    sottocartella_buio = ""
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
        tua_pos_buio = st.radio("Tua Posizione sui Bui:", ["BB", "SB"], horizontal=True)
        sottocartella_buio = tua_pos_buio.upper()
        
        azione_buio = st.radio("Tua Intenzione:", ["3_Bet", "Call"])
        nome_file_principale = f"{azione_buio.lower()}.jpg"
        pos_label = f"{tua_pos_buio} -> {azione_buio}"

    elif scenario == "Iso Raise":
        cartella_scenario = "ISO RAISE"
        stile = st.radio(" Approccio Iso:", ["Conservativo", "Moderato"], horizontal=True)
        stile_label = stile
        
        # Mappatura blindata sui tuoi nomi file reali su GitHub
        if stile == "Conservativo":
            nome_file_principale = "iso_raise_conservativo.jpg"
        else:
            nome_file_principale = "iso_raise_moderato.jpg"

    elif scenario == "Over Limping":
        cartella_scenario = "OVER LIMPING"
        nome_file_principale = "over_limping.jpg"
        info_regola = "⚠️ REGOLA: Se c'è rischio Raise o Iso Raise -> NO OVER LIMP."

    elif scenario == "Over Calling":
        cartella_scenario = "OVER CALLING"
        nome_file_principale = "over_calling.jpg"

    st.markdown("---")


# -------------------------------------------------------------------------
# AREA PRINCIPALE: VISUALIZZAZIONE GIGANTE
# -------------------------------------------------------------------------

# Composizione dinamica del percorso
if scenario == "Difesa Bui":
    path_principale = os.path.join(BASE_DIR, IMAGE_DIR, cartella_scenario, sottocartella_buio, nome_file_principale)
    path_bluff = ""
elif scenario == "Iso Raise" or scenario == "Over Limping" or scenario == "Over Calling":
    # Questi scenari NON hanno le sottocartelle CONSERVATIVE/MODERATE, i file sono direttamente dentro la cartella principale dello scenario
    path_principale = os.path.join(BASE_DIR, IMAGE_DIR, cartella_scenario, nome_file_principale)
    path_bluff = ""
elif sottocartella_stile:
    path_principale = os.path.join(BASE_DIR, IMAGE_DIR, cartella_scenario, sottocartella_stile, nome_file_principale)
    path_bluff = os.path.join(BASE_DIR, IMAGE_DIR, cartella_scenario, sottocartella_stile, nome_file_bluff) if nome_file_bluff else ""
else:
    path_principale = os.path.join(BASE_DIR, IMAGE_DIR, cartella_scenario, nome_file_principale)
    path_bluff = os.path.join(BASE_DIR, IMAGE_DIR, cartella_scenario, nome_file_bluff) if nome_file_bluff else ""


# Titolo dinamico in cima
st.markdown(f"## {scenario} {stile_label} {pos_label}")

if info_regola:
    st.info(info_regola)

# Debug log visibile per capire dove sta cercando il file in tempo reale
st.caption(f"🔎 Percorso di ricerca: `{IMAGE_DIR}/{cartella_scenario}/{sottocartella_stile + '/' if sottocartella_stile else ''}{sottocartella_buio + '/' if sottocartella_buio else ''}{nome_file_principale}`")

# Rendering grafico gigante
if nome_file_bluff:
    col_cc1, col_cc2 = st.columns(2)
    with col_cc1:
        if os.path.exists(path_principale):
            st.image(path_principale, caption="Value Range", use_container_width=True)
        else:
            st.error(f"File mancante: `{IMAGE_DIR}/{cartella_scenario}/{sottocartella_stile}/{nome_file_principale}`")
    with col_cc2:
        if os.path.exists(path_bluff):
            st.image(path_bluff, caption="Bluff Range", use_container_width=True)
        else:
            st.error(f"File mancante: `{IMAGE_DIR}/{cartella_scenario}/{sottocartella_stile}/{nome_file_bluff}`")
else:
    if os.path.exists(path_principale):
        st.image(path_principale, use_container_width=True)
    else:
        st.error(f"❌ Immagine non trovata! Verifica che il file si trovi esattamente in: `{path_principale.replace(BASE_DIR, '')}`")
