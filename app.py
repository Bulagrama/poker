import streamlit as st
import os

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Poker Range Dashboard", layout="wide", page_icon="🃏")

st.title("🃏 Texas Hold'em Interactive Range Viewer")
st.write("Seleziona lo scenario e la posizione per visualizzare istantaneamente il range pre-flop corretto.")

# Definiamo la cartella dove salverai le immagini
IMAGE_DIR = "immagini_poker"

# 1. BARRA LATERALE: SELEZIONE DELLO SCENARIO PRINCIPALE
st.sidebar.header("🕹️ Tipo di Azione / Scenario")
scenario = st.sidebar.selectbox(
    "Scegli la situazione pre-flop:",
    [
        "Opening Raises (RFI)",
        "3-Bet Ranges",
        "3-Bet Cold Calling Ranges",
        "Iso Over Limp Ranges",
        "Over Limping (Griglia Singola)",
        "Over Calling (Griglia Singola)"
    ]
)

# Inizializziamo le variabili per il file e la nota
nome_file = ""
nota_informativa = ""

# 2. LOGICA DINAMICA IN BASE ALLO SCENARIO SELEZIONATO
if scenario == "Opening Raises (RFI)":
    nome_file = "OPENING RAISES RANGES MICRO CRUSH.png"
    st.sidebar.subheader("Posizione di Apertura")
    pos_rfi = st.sidebar.radio("Vedi posizione specifica all'interno della griglia:", ["Tutte", "UTG", "MP", "CO", "BTN", "SB"])
    nota_informativa = f"Visualizzazione globale dei range di Open Raise. Fai riferimento alla griglia **{pos_rfi}** nell'immagine."

elif scenario == "3-Bet Ranges":
    nome_file = "3-BET RANGES.jpg"
    st.sidebar.subheader("Posizione del 3-Bettor")
    pos_3b = st.sidebar.radio("Seleziona scenario:", ["Tutte", "UTG 9.8%", "MP 12.50%", "CO/BTN 22/35%", "SB 22%", "3-BET BLUFF RANGE"])
    nota_informativa = f"Mappa delle 3-Bet. Guarda il quadrante relativo a: **{pos_3b}**."

elif scenario == "3-Bet Cold Calling Ranges":
    nome_file = "3-BET COLD CALLING RANGES.jpg"
    st.sidebar.subheader("Versus Posizione")
    vs_pos = st.sidebar.radio("Seleziona l'avversario che ha aperto:", ["Tutte", "VS UTG 10%", "VS MP 13%", "VS CO 23%"])
    nota_informativa = f"Range di Cold Call / 3-Bet contro openraise. Legenda: Azzurro = Bluff, Verde = Opzionale, Rosso = 3-Bet di Valore. Focus su: **{vs_pos}**."

elif scenario == "Iso Over Limp Ranges":
    nome_file = "ISO OVER LIMP RANGES.jpg"
    st.sidebar.subheader("Tipo di Limper")
    tipo_limp = st.sidebar.radio("Seleziona il profilo dell'avversario:", ["Default Iso-Raising", "Weak-Tight Limper (15/6)", "Weak-Loose Limper (50/8)"])
    nota_informativa = f"Strategia di Isolamento vs Limper. Focus sulla tabella: **{tipo_limp}**."

elif scenario == "Over Limping (Griglia Singola)":
    nome_file = "OVER LIMPING.png"
    nota_informativa = "⚠️ **REGOLA CRUCIALE:** Se dopo di noi c'è un giocatore aggressivo con rischio Raise o Iso Raise -> **NO OVER LIMP**, ma fai solo ISO RAISE."

elif scenario == "Over Calling (Griglia Singola)":
    nome_file = "OVER CALLING.png"
    nota_informativa = "Grigio scuro = Over-Calling Hands | Kaki/Beige = Potential 3-Betting Hands."

# 3. VISUALIZZAZIONE DEL RANGE
percorso_completo = os.path.join(IMAGE_DIR, nome_file)

st.write("---")
if nota_informativa:
    st.info(nota_informativa)

if os.path.exists(percorso_completo):
    # Mostra l'immagine a schermo intero o adattata
    st.image(percorso_completo, caption=f"File caricato: {nome_file}", use_container_width=True)
else:
    st.error(f"❌ File non trovato: Assicurati di aver salvato l'immagine come `{nome_file}` dentro la cartella `{IMAGE_DIR}/`")
    st.info("""
    **Istruzioni per far funzionare l'app sul tuo computer:**
    1. Crea una cartella sul PC (es. `poker_app`).
    2. Salva questo codice in un file chiamato `app.py` in quella cartella.
    3. Crea una sotto-cartella chiamata `immagini_poker`.
    4. Inserisci le tue 6 immagini all'interno di `immagini_poker` rinominandole esattamente così:
       - `OPENING RAISES RANGES MICRO CRUSH.jpg`
       - `3-BET RANGES.jpg`
       - `3-BET COLD CALLING RANGES.jpg`
       - `ISO OVER LIMP RANGES.jpg`
       - `OVER LIMPING.png`
       - `OVER CALLING.png`
    5. Apri il terminale, posizionati nella cartella e lancia il comando: `streamlit run app.py`
    """)
