import streamlit as st
import pandas as pd
import re
from calculator import render_calculator
import streamlit.components.v1 as components

try:
    import openpyxl  # noqa: F401
    excel_support = True
except ImportError:
    excel_support = False

st.set_page_config(
    page_title="Engel & Völkers Rental Excel Tester",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# Render the sidebar calculator from calculator.py
render_calculator()

# Modern app design and background styling
st.markdown("""
<style>
body, .stApp, .main, .block-container {
    background: linear-gradient(180deg, #eef2ff 0%, #f8fafc 55%, #ffffff 100%);
    color: #0f172a;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

div[data-testid='stAppViewContainer'] > div:first-child {
    padding-top: 1.5rem;
}

section.main {
    background: transparent;
}

.css-18e3th9 {
    padding: 0 !important;
}

.block-container { background: rgba(0,0,0,0.45); 
    border-radius: 30px; 
    border: 1px solid rgba(15,23,42,0.08); 
    box-shadow: 0 30px 80px rgba(15, 23, 42, 0.08); 
    padding: 32px 36px 40px; 
    max-width: 1100px; 
    margin: auto; 
}

.stApp {
    background-image:
        linear-gradient(rgba(0,0,0,0.35), rgba(0,0,0,0.35)),
        url("https://images.unsplash.com/photo-1600585154340-be6161a56a0c");

    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;

    min-height: 100vh;
}
.stButton>button,
.stTextInput>div>div>input,
.stSelectbox>div>div>div {
    border-radius: 16px !important;
    border: 1px solid rgba(15, 23, 42, 0.12) !important;
    box-shadow: 0 14px 30px rgba(15, 23, 42, 0.08);
}

.stButton>button {
    background: linear-gradient(135deg, #0f172a, #334155) !important;
    color: #ffffff !important;
    border: none !important;
    padding: 0.95rem 1.6rem !important;
}

.stButton>button:hover {
    transform: translateY(-1px);
    box-shadow: 0 20px 40px rgba(15, 23, 42, 0.18);
}

.stAlert, .stInfo, .stWarning, .stSuccess {
    border-radius: 22px !important;
    border: none !important;
    padding: 22px 24px !important;
    box-shadow: 0 22px 50px rgba(15, 23, 42, 0.08) !important;
}

.stMarkdown p {
    color: #475569;
    line-height: 1.8;
}

.stInfo {
    background: rgba(14, 165, 233, 0.08) !important;
}

.stWarning {
    background: rgba(251, 146, 60, 0.08) !important;
}

.stSuccess {
    background: rgba(22, 163, 74, 0.08) !important;
}

[data-testid='stSidebar'] {
    background: rgba(255,255,255,0.15) !important;
    border-radius: 28px !important;
    box-shadow: 0 30px 60px rgba(15, 23, 42, 0.08) !important;
}

[data-testid='stSidebar'] .css-1d391kg {
    padding: 18px 16px 24px !important;
}

[data-testid='stSidebar'] h2 {
    color: #d4af37 !important;
}
/* Modern typography */
h1, h2, h3, h4, h5, h6 {

    color: #ffffff !important;

    font-family:
        "Inter",
        "Segoe UI",
        sans-serif !important;

    font-weight: 700 !important;

    letter-spacing: 0.4px;

    text-shadow:
        0 3px 12px rgba(0,0,0,0.85);

}


p, label, li {

    color: rgba(255,255,255,0.90) !important;

    font-family:
        "Inter",
        "Segoe UI",
        sans-serif !important;

    font-weight: 500 !important;

    letter-spacing: 0.2px;

    line-height: 1.7;

    text-shadow:
        0 2px 8px rgba(0,0,0,0.8);
}
/* Sidebar button */ [data-testid="stSidebarCollapseButton"] { 
            background: rgba(0,0,0,0.45) !important; 
            border-radius: 50% !important;
             width:42px !important;
             height:42px !important;
             backdrop-filter:blur(10px); 
}


/* Icon */

[data-testid="stSidebarCollapseButton"] span {

    color:#f5d58b !important;

    font-size:28px !important;

    font-weight:900 !important;

    text-shadow:
    0 2px 8px black;

}

/* ==========================================
   TRANSPARENT HEADER / TOOLBAR
========================================== */

header,
[data-testid="stHeader"],
[data-testid="stToolbar"] {

    background: transparent !important;

    background-color: transparent !important;

    box-shadow: none !important;

    border: none !important;
}

/* ==========================================
   FILE UPLOADER
========================================== */

[data-testid="stFileUploader"] {

    background: transparent !important;

}

[data-testid="stFileUploaderDropzone"] {

    background: rgba(255,255,255,0.05) !important;

    border: 1px solid rgba(255,255,255,0.30) !important;

    border-radius: 22px !important;

    backdrop-filter: blur(15px);

    -webkit-backdrop-filter: blur(15px);

    box-shadow: none !important;

    transition: .25s;
}

[data-testid="stFileUploaderDropzone"]:hover {

    background: rgba(255,255,255,0.10) !important;

    border: 1px solid rgba(255,255,255,0.50) !important;
}

[data-testid="stFileUploaderDropzone"] * {

    color: white !important;
}

/* ==========================================
   UPLOAD BUTTON
========================================== */

[data-testid="stFileUploader"] button,
[data-testid="stFileUploaderDropzone"] button {

    background: rgba(255,255,255,0.08) !important;

    color: white !important;

    border: 1px solid rgba(255,255,255,0.35) !important;

    border-radius: 14px !important;

    box-shadow: none !important;

    font-weight: 700 !important;
}

[data-testid="stFileUploader"] button:hover,
[data-testid="stFileUploaderDropzone"] button:hover {

    background: rgba(255,255,255,0.16) !important;

    color: white !important;

    border: 1px solid rgba(255,255,255,0.60) !important;
}

/* Active */

[data-testid="stFileUploaderDropzone"] button:active {

    background: rgba(255,255,255,0.22) !important;
}


/* Focus */

[data-testid="stFileUploaderDropzone"] button:focus {

    outline: none !important;

    box-shadow: 0 0 0 2px rgba(255,255,255,0.25) !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <div style="background: rgba(255,255,255,0.10);border-radius: 28px; padding: 32px 34px 34px; box-shadow: 0 30px 80px rgba(15,23,42,0.08); margin-bottom: 24px;">
        <div style="display:flex; flex-direction:column; flex-wrap:wrap; align-items:center; gap:24px; text-align:center;">
            <div style="max-width: 720px;">
                <h1 style="margin:0;font-size:2.6rem;color:#0f172a;"> Engel & Völkers Rental Excel Tester</h1>
                <p style="margin:18px 0 0;font-size:1.05rem;line-height:1.75;color:#475569;">Ανεβάστε το αρχείο σας (CSV ή Excel) για να ελέγξετε ποια deal είναι έτοιμα για το T-Box.</p>
            </div>
            <div style="display:flex;align-items:center;justify-content:center;min-width:140px;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Logo_EV_RGB_%C2%A9_Engel_%26_V%C3%B6lkers.png/1280px-Logo_EV_RGB_%C2%A9_Engel_%26_V%C3%B6lkers.png" style="height:100px;object-fit:contain;opacity:0.96;border-radius:18px;" />
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("""
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px;margin-bottom:32px;">
  <div style="background:rgba(255,255,255,0.18);;border-radius:22px;padding:20px 22px;box-shadow:0 20px 48px rgba(15,23,42,0.06);">
    <h4 style="margin:0 0 10px;color:#0f172a;">Γρήγορα βήματα</h4>
    <p style="margin:0;color:#475569;line-height:1.75;">1. Φόρτωστε CSV ή XLSX<br>2. Ελέγξτε εκκρεμότητες<br>3. Δείτε έτοιμα deal για T-Box</p>
  </div>
  <div style="background:rgba(255,255,255,0.18);;border-radius:22px;padding:20px 22px;box-shadow:0 20px 48px rgba(15,23,42,0.06);">
    <h4 style="margin:0 0 10px;color:#0f172a;">Σχετικά</h4>
    <p style="margin:0;color:#475569;line-height:1.75;">Το εργαλείο αυτό αναλύει τις στήλες του αρχείου και εμφανίζει αν υπάρχουν εκκρεμότητες ή αν το deal είναι έτοιμο για T-Box.</p>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")


# Pattern που αναγνωρίζει ποσά σε ευρωπαϊκό (1.488,00) ή αμερικανικό (1,488.00)
# format, αλλά και απλούς ακέραιους (π.χ. 500 ή 12345) χωρίς να τα σπάει.
AMOUNT_PATTERN = (
    r'\d{4,}(?:[.,]\d+)?'                      # ακέραιοι > 999 (π.χ. 12345)
    r'|\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{1,2})?'  # 1.488,00 / 1,488.00 / 500
    r'|\d+(?:[.,]\d+)?'                        # εφεδρικό (π.χ. 12.5)
)


# Συνάρτηση ελέγχου αν ένα κείμενο περιέχει αριθμό (οφειλή)
def extract_debt(text):
    if pd.isna(text):
        return None
    text_str = str(text).strip()
    # Εξαιρούμε ημερομηνίες μορφής DD/MM/YYYY αν τυχόν υπάρχουν μέσα στο όνομα
    clean_text = re.sub(r'\b\d{2}/\d{2}/\d{4}\b', '', text_str)
    # Προτίμηση: αριθμός αμέσως μετά το € (π.χ. "€1.488,00")
    euro_matches = re.findall(r'€\s*(' + AMOUNT_PATTERN + r')', clean_text)
    if euro_matches:
        return euro_matches[-1]
    numbers = re.findall(AMOUNT_PATTERN, clean_text)
    if numbers:
        return numbers[-1]  # Επιστρέφει τον τελευταίο αριθμό που βρήκε ως οφειλή
    return None


# Upload Αρχείου
uploaded_file = st.file_uploader("Επιλέξτε αρχείο", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Αναγνώριση τύπου αρχείου και φόρτωση
        filename = uploaded_file.name.lower()
        if filename.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif filename.endswith('.xlsx'):
            if not excel_support:
                raise RuntimeError(
                    "Για να διαβάσετε .xlsx αρχείο χρειάζεται να εγκαταστήσετε το openpyxl: pip install openpyxl"
                )
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        else:
            raise ValueError("Μη υποστηριζόμενος τύπος αρχείου. Επιλέξτε csv ή xlsx.")

        st.success("Το αρχείο ανέβηκε επιτυχώς!")

        # Προβολή των πρώτων γραμμών για επιβεβαίωση
        with st.expander("👁️ Δείτε τα δεδομένα του αρχείου"):
            st.dataframe(df)

        # Έλεγχος αν υπάρχουν τουλάχιστον 6 στήλες (Α έως F)
        if df.shape[1] < 6:
            st.error("Το αρχείο πρέπει να έχει τουλάχιστον 6 στήλες (Ημερομηνία, Κωδικός, Στήλη C, Ποσό, Στήλη E, Σχόλια/Ημερομηνία F).")
        else:
            ready_deals = []
            pending_messages = []

            for index, row in df.iterrows():
                # On-the-fly χαρτογράφηση στηλών με βάση τη θέση τους (0=A, 1=B, 2=C, 3=D, 4=E, 5=F)
                col_b = str(row.iloc[1]).strip()  # Κωδικός Deal
                col_c = row.iloc[2]               # Στοιχεία Συναλλαγής 1
                col_d = row.iloc[3]               # Ποσό
                col_e = row.iloc[4]               # MATCH WITH
                col_f = str(row.iloc[5]).strip()  # Σχόλια / Ημερομηνία Πληρωμής

                # Έλεγχος για οφειλές (ύπαρξη αριθμού)
                debt_c = extract_debt(col_c)
                debt_e = extract_debt(col_e)

                # Καθαρισμός ονομάτων για τα μηνύματα (αφαιρούμε ολόκληρο το ποσό + €)
                name_c = re.sub(r'€?\s*(?:' + AMOUNT_PATTERN + r').*', '', str(col_c)).replace('-', '').strip() if not pd.isna(col_c) else ""
                name_e = re.sub(r'€?\s*(?:' + AMOUNT_PATTERN + r').*', '', str(col_e)).replace('-', '').strip() if not pd.isna(col_e) else ""

                row_has_debt = False

                # 1. Έλεγχος ξεχωριστά για οφειλές
                if debt_c:
                    pending_messages.append(f"🔴 **Deal {col_b}**: Ο πελάτης {name_c} οφείλει το ποσό {debt_c} €")
                    row_has_debt = True
                if debt_e:
                    pending_messages.append(f"🔴 **Deal {col_b}**: Ο πελάτης {name_e} οφείλει το ποσό {debt_e} €")
                    row_has_debt = True

                # 2. Έλεγχος αν είναι έτοιμο για T-Box
                has_amount_d = not pd.isna(col_d) and str(col_d).strip() != ""
                has_date_f = pd.notna(row.iloc[5]) and col_f != "" and col_f.lower() != "nan"
                contains_date = bool(re.search(r'\d{2}[/-]\d{2}[/-]\d{4}', col_f))
                if not row_has_debt and has_amount_d and has_date_f:
                    ready_deals.append(f"🟢 Είναι έτοιμο το deal (**{col_b}**) να μπεί T-Box, έχουν πληρώσει και οι δύο πλευρές")
                elif not row_has_debt:
                    if not contains_date:
                        pending_messages.append(f"⚠️ **Deal {col_b}**: Δεν υπάρχει έγκυρη ημερομηνία πληρωμής στη στήλη F (Σχόλια).")

            # --- ΕΜΦΑΝΙΣΗ ΑΠΟΤΕΛΕΣΜΑΤΩΝ ---
            st.markdown("---")

            st.subheader("🟢 Έτοιμα για T-Box")
            if ready_deals:
                for deal in ready_deals:
                    st.info(deal)
            else:
                st.warning("Κανένα deal δεν είναι έτοιμο για T-Box αυτή τη στιγμή.")

            st.markdown("---")
            st.subheader("❌ Εκκρεμότητες & Οφειλές")
            if pending_messages:
                for msg in pending_messages:
                    st.write(msg)
            else:
                st.success("Δεν βρέθηκαν εκκρεμότητες!")

    except Exception as e:
        st.error(f"Προέκυψε σφάλμα κατά την επεξεργασία: {e}")
