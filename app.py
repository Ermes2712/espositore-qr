import io
import qrcode
import streamlit as st
from fpdf import FPDF

# ==========================================
# 1. CONFIGURAZIONE PAGINA STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Generatore Espositore QR Recensioni",
    page_icon="⭐",
    layout="centered"
)

# Titolo e descrizione principale
st.title("⭐ Generatore Espositore Recensioni")
st.markdown("Crea e scarica istantaneamente il PDF per il tuo espositore da banco con QR Code integrato.")

st.divider()

# ==========================================
# 2. MODULO INSERIMENTO DATI UTENTE
# ==========================================
st.subheader("1. Inserisci i dettagli dell'attività")

nome_attivita = st.text_input(
    label="Nome dell'Attività / Locale",
    value="Ristorante Bella Vista",
    help="Questo nome apparirà in grande in alto sull'espositore."
)

link_google = st.text_input(
    label="Link diretto alle Recensioni Google",
    value="https://g.page/r/example",
    help="Incolla qui il link della tua scheda Google o di qualsiasi altro social/piattaforma."
)

stile_scelto = st.selectbox(
    label="Scegli lo stile grafico",
    options=["Classico Blu", "Elegante Nero", "Smeraldo Verde"]
)

# Mappatura colori RGB in base allo stile scelto
COLORI = {
    "Classico Blu": (26, 115, 232),   # Blu Google
    "Elegante Nero": (30, 30, 30),     # Nero Antracite
    "Smeraldo Verde": (15, 128, 68)   # Verde Smeraldo
}

color_rgb = COLORI[stile_scelto]

# ==========================================
# 3. FUNZIONE PER GENERARE IL PDF A5
# ==========================================
def genera_pdf_espositore(nome, link, rgb):
    # 1. Genera l'immagine del QR Code in memoria (senza salvarla su disco)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(link)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black", back_color="white")
    
    # Salva il QR code in un buffer di memoria RAM
    qr_buffer = io.BytesIO()
    img_qr.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)
    
    # 2. Crea la struttura del PDF in formato A5 (148 x 210 mm)
    pdf = FPDF(orientation='P', unit='mm', format='A5')
    pdf.add_page()
    pdf.set_auto_page_break(auto=False)
    
    # Bordo / Cornice decorativa dell'espositore
    pdf.set_draw_color(*rgb)
    pdf.set_line_width(1.5)
    pdf.rect(5, 5, 138, 200)
    
    # Intestazione superiore con colore personalizzato
    pdf.set_fill_color(*rgb)
    pdf.rect(5, 5, 138, 30, style='F')
    
    # Testo nell'intestazione (Bianco)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", style='B', size=16)
    pdf.set_xy(5, 12)
    pdf.cell(138, 10, "LASCIA UNA RECENSIONE", align='C', ln=True)
    
    # Nome dell'attività
    pdf.set_text_color(40, 40, 40)
    pdf.set_font("Helvetica", style='B', size=18)
    pdf.set_xy(10, 45)
    pdf.multi_cell(128, 8, nome, align='C')
    
    # Sottotitolo / Invito all'azione
    pdf.set_font("Helvetica", size=11)
    pdf.set_text_color(100, 100, 100)
    pdf.set_xy(10, 65)
    pdf.cell(128, 6, "Inquadra il QR Code con la fotocamera del tuo telefono", align='C', ln=True)
    
    # Inserimento del QR Code al centro del foglio
    pdf.image(qr_buffer, x=34, y=75, w=80)
    
    # Testo inferiore / Ringraziamento
    pdf.set_font("Helvetica", style='B', size=13)
    pdf.set_text_color(*rgb)
    pdf.set_xy(10, 165)
    pdf.cell(128, 8, "IL TUO PARERE È FONDAMENTALE!", align='C', ln=True)
    
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(128, 6, "Grazie per il tuo supporto", align='C', ln=True)
    
    # Ritorna i byte del PDF generato
    return bytes(pdf.output())

# ==========================================
# 4. ANTEPRIMA E TASTO DOWNLOAD
# ==========================================
st.divider()
st.subheader("2. Genera e scarica il tuo file")

if st.button("🚀 Genera Espositore PDF", use_container_width=True):
    if not link_google.strip():
        st.error("⚠️ Per favore, inserisci un link valido prima di procedere.")
    else:
        with st.spinner("Generazione del PDF in corso..."):
            pdf_data = genera_pdf_espositore(nome_attivita, link_google, color_rgb)
            
            st.success("✅ Il tuo PDF è pronto per la stampa!")
            
            # Pulsante effettivo di download del PDF
            st.download_button(
                label="📥 Scarica PDF Pronto per la Stampa (A5)",
                data=pdf_data,
                file_name=f"Espositore_QR_{nome_attivita.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
