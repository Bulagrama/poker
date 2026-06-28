import streamlit as st
import os
from PIL import Image

st.set_page_config(page_title="Poker Range Dashboard", layout="wide", page_icon="🃏")

st.title("🃏 Texas Hold'em Instant Range Viewer")
st.write("Seleziona la tua situazione al tavolo. L'app isolerà e ingrandirà solo il range che ti interessa.")

IMAGE_DIR = "immagini_poker"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. INTERFACCIA DI SELEZIONE RAPIDA
col1, col2 = st.columns(2)

with col1:
    scenario = st.selectbox(
        "1. Che tipo di azione/scenario?",
        [
            "Opening Raises (RFI)",
            "3-Bet Ranges",
            "3-Bet Cold Calling",
            "Iso Over Limp",
            "Over Limping",
            "Over Calling"
        ]
    )

with col2:
    if scenario == "Opening Raises (RFI)":
        sotto_opzione = st.selectbox("2. In che posizione sei?", ["UTG", "MP", "CO", "BTN", "SB"])
    elif scenario == "3-Bet Ranges":
        sotto_opzione = st.selectbox("2. In che posizione sei (o tipo di 3-bet)?", ["UTG 9.8%", "MP 12.50%", "CO/BTN 22/35%", "SB 22%", "3-BET BLUFF RANGE"])
    elif scenario == "3-Bet Cold Calling":
        sotto_opzione = st.selectbox("2. Contro quale posizione stai giocando?", ["VS UTG 10%", "VS MP 13%", "VS CO 23%"])
    elif scenario == "Iso Over Limp":
        sotto_opzione = st.selectbox("2. Che tipo di Limper è?", ["Default Iso-Raising", "Weak-Tight Limper: 15/6 Range", "Weak-Loose Limper: 50/8 Range"])
    else:
        sotto_opzione = "Unica"

# 2. LOGICA DI RITAGLIO COORDINATE
box = None
nome_file = ""

if scenario == "Opening Raises (RFI)":
    nome_file = "OPENING RAISES RANGES MICRO CRUSH.png"
    coordinate_rfi = {
        "UTG": (0, 0, 310, 340),
        "MP": (310, 0, 620, 340),
        "CO": (620, 0, 940, 340),
        "BTN": (0, 340, 310, 700),
        "SB": (310, 340, 620, 700)
    }
    box = coordinate_rfi.get(sotto_opzione)

elif scenario == "3-Bet Ranges":
    nome_file = "3-BET RANGES.jpg"
    coordinate_3b = {
        "UTG 9.8%": (0, 0, 300, 330),
        "MP 12.50%": (300, 0, 600, 330),
        "CO/BTN 22/35%": (0, 430, 300, 760),
        "SB 22%": (300, 430, 600, 760),
        "3-BET BLUFF RANGE": (600, 230, 950, 650)
    }
    box = coordinate_3b.get(sotto_opzione)

elif scenario == "3-Bet Cold Calling":
    nome_file = "3-BET COLD CALLING RANGES.jpg"
    coordinate_cc = {
        "VS UTG 10%": (0, 0, 330, 380),
        "VS MP 13%": (330, 0, 660, 380),
        "VS CO 23%": (660, 0, 1000, 380)
    }
    box = coordinate_cc.get(sotto_opzione)

elif scenario == "Iso Over Limp":
    nome_file = "ISO OVER LIMP RANGES.jpg"
    coordinate_iso = {
        "Default Iso-Raising": (0, 0, 450, 400),
        "Weak-Tight Limper: 15/6 Range": (0, 440, 480, 850),
        "Weak-Loose Limper: 50/8 Range": (480, 440, 1000, 850)
    }
    box = coordinate_iso.get(sotto_opzione)

elif scenario == "Over Limping":
    nome_file = "OVER LIMPING.png"

elif scenario == "Over Calling":
    nome_file = "OVER CALLING.png"

# 3. CARICAMENTO ED ELABORAZIONE IMMAGINE
percorso_completo = os.path.join(BASE_DIR, IMAGE_DIR, nome_file)

st.write("---")

if os.path.exists(percorso_completo):
    img = Image.open(percorso_completo)
    
    if box:
        try:
            img_ritagliata = img.crop(box)
            st.image(img_ritagliata, caption=f"Range Isolato: {sotto_opzione}", width=500)
        except Exception as e:
            st.error("Errore durante il ritaglio. Mostro l'immagine intera.")
            st.image(img, use_container_width=True)
    else:
        st.image(img, width=500)
else:
    st.error(f"❌ Immagine non trovata in: `{percorso_completo}`")
