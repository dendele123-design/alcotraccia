import streamlit as st
import time

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="Alco-Traccia", page_icon="🍺")

st.title("🍺 Alco-Traccia")
st.write("Calcolatore Tasso Alcolemico (Stima Widmark)")

# Avviso fisso
st.warning("⚠️ ATTENZIONE: Questa è una STIMA matematica. I valori reali variano per metabolismo, genetica e salute. NON usare questo risultato per decidere se guidare. Se bevi, non guidare.")

st.divider()

# --- INPUT DATI ---
col1, col2 = st.columns(2)
with col1:
    sesso = st.radio("Sesso", ["Uomo", "Donna"], horizontal=True)
    peso = st.number_input("Peso (kg)", min_value=40, max_value=150, value=75, step=1)
with col2:
    stomaco = st.radio("Stomaco", ["Vuoto", "Pieno"], horizontal=True)
    st.caption("A stomaco pieno il picco alcolemico è solitamente più basso.")

st.divider()

# --- INPUT DRINK ---
st.subheader("Cosa hai bevuto?")

tipi_drink = {
    "Birra Piccola": [330, 5.0],
    "Birra Media": [500, 5.0],
    "Vino (Bicchiere)": [125, 12.0],
    "Amaro": [40, 30.0],
    "Superalcolico (Shot)": [40, 40.0],
    "Cocktail (Standard)": [150, 15.0],
    "Personalizzato": [0, 0.0]
}

scelta = st.selectbox("Seleziona bevanda:", list(tipi_drink.keys()))
vol_std, grad_std = tipi_drink[scelta]

c1, c2, c3 = st.columns(3)
with c1:
    quantita = st.number_input("Quantità (ml)", value=vol_std, key=f"ml_{scelta}")
with c2:
    gradi = st.number_input("Gradi (%)", value=grad_std, key=f"gr_{scelta}")
with c3:
    n_bicchieri = st.number_input("Bicchieri", min_value=1, value=1, step=1, key=f"n_{scelta}")

# --- IL CALCOLO ---
# Aggiungiamo un bottone per avviare il calcolo
if st.button("CALCOLA IL TASSO 🧮", type="primary"):
    
    # 1. Calcolo Grammi di Alcol
    grammi_alcol = quantita * (gradi / 100) * 0.8 * n_bicchieri
    
    # 2. Scelta Fattore Widmark (r)
    if sesso == "Uomo":
        fattore_r = 0.68
    else:
        fattore_r = 0.55
        
    # 3. Formula Base: Grammi / (Peso * r)
    tasso_stimato = grammi_alcol / (peso * fattore_r)
    
    # 4. Correzione Stomaco Pieno
    # Se lo stomaco è pieno, il picco è ridotto (assorbimento più lento e incompleto)
    if stomaco == "Pieno":
        tasso_stimato = tasso_stimato * 0.8  # Riduciamo del 20% circa
    
    # 5. Calcolo smaltimento (circa 0.15 g/l all'ora)
    ore_per_smaltire = tasso_stimato / 0.15

    # --- VISUALIZZAZIONE RISULTATI ---
    st.divider()
    st.subheader("Risultato Stima")
    
    # Creiamo un "semaforo" visivo
    if tasso_stimato > 0.5:
        colore_box = "error" # Rosso in Streamlit
        messaggio = "⛔ SOPRA IL LIMITE LEGALE (0.5 g/l)"
        consiglio = "NON GUIDARE. Chiama un taxi o aspetta."
    else:
        colore_box = "success" # Verde in Streamlit
        messaggio = "✅ Entro i limiti (ma prudenza!)"
        consiglio = "Sei sotto il limite legale, ma i riflessi potrebbero essere comunque rallentati."

    # Mostriamo il box colorato
    if tasso_stimato > 0.5:
        st.error(f"{messaggio}")
    else:
        st.success(f"{messaggio}")

    # Le metriche grandi
    m1, m2 = st.columns(2)
    m1.metric("Tasso Alcolemico", f"{tasso_stimato:.2f} g/l")
    m2.metric("Tempo per tornare a 0.0", f"{ore_per_smaltire:.1f} Ore")
    
    st.info(f"💡 {consiglio}")
    st.write(f"Hai assunto circa **{grammi_alcol:.1f}g** di alcol puro.")