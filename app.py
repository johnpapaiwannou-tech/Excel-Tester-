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
    page_title="Engel & Volkers Rental Excel Tester",
    page_icon="🏠",
    layout="wide",
)

# Clear sidebar state in localStorage (helps when sidebar remains stuck open)
components.html(
        """<script>
        try{
            Object.keys(localStorage).forEach(function(k){
                var key = k.toLowerCase();
                if(key.includes('sidebar') || key.includes('streamlit') || key.includes('collapsed')){
                    localStorage.removeItem(k);
                }
            });
            var collapsedKey = Object.keys(localStorage).find(function(k){
                return k.toLowerCase().includes('sidebar') && k.toLowerCase().includes('collapsed');
            });
            if(collapsedKey){
                localStorage.setItem(collapsedKey, 'true');
            }
        }catch(e){console && console.log(e)}
        </script>""",
        height=0,
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

.block-container {
    background: rgba(255,255,255,0.95);
    border-radius: 30px;
    border: 1px solid rgba(15,23,42,0.08);
    box-shadow: 0 30px 80px rgba(15, 23, 42, 0.08);
    padding: 32px 36px 40px;
    max-width: 1100px;
    margin: auto;
}

.stApp {
    background-image: url("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Logo_EV_RGB_%C2%A9_Engel_%26_V%C3%B6lkers.png/1280px-Logo_EV_RGB_%C2%A9_Engel_%26_V%C3%B6lkers.png");
    background-size: 180px auto;
    background-position: center 40px;
    background-repeat: no-repeat;
    background-attachment: local;
    min-height: 100vh;
    padding-top: 200px;
}

.stButton>button,
.stFileUploader>div,
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
    background: rgba(255,255,255,0.96) !important;
    border-radius: 28px !important;
    box-shadow: 0 30px 60px rgba(15, 23, 42, 0.08) !important;
}

[data-testid='stSidebar'] .css-1d391kg {
    padding: 18px 16px 24px !important;
}

[data-testid='stSidebar'] h2 {
    color: #0f172a !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <div style="background: rgba(255,255,255,0.96); border-radius: 28px; padding: 32px 34px 34px; box-shadow: 0 30px 80px rgba(15,23,42,0.08); margin-bottom: 24px;">
        <div style="display:flex; flex-wrap:wrap; justify-content:space-between; gap:24px; align-items:center;">
            <div style="max-width: 720px;">
                <h1 style="margin:0;font-size:2.6rem;color:#0f172a;">📊 Engel & Volkers Rental Excel Tester</h1>
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
  <div style="background:#ffffff;border-radius:22px;padding:20px 22px;box-shadow:0 20px 48px rgba(15,23,42,0.06);">
    <h4 style="margin:0 0 10px;color:#0f172a;">Γρήγορα βήματα</h4>
    <p style="margin:0;color:#475569;line-height:1.75;">1. Φόρτωσε CSV ή XLSX<br>2. Έλεγξε εκκρεμότητες<br>3. Δες έτοιμα deal για T-Box</p>
  </div>
  <div style="background:#ffffff;border-radius:22px;padding:20px 22px;box-shadow:0 20px 48px rgba(15,23,42,0.06);">
    <h4 style="margin:0 0 10px;color:#0f172a;">Σχετικά</h4>
    <p style="margin:0;color:#475569;line-height:1.75;">Το εργαλείο αυτό αναλύει τις στήλες του αρχείου και εμφανίζει αν υπάρχουν εκκρεμότητες ή αν το deal είναι έτοιμο για T-Box.</p>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")


# Συνάρτηση ελέγχου αν ένα κείμενο περιέχει αριθμό (οφειλή)
def extract_debt(text):
    if pd.isna(text):
        return None
    text_str = str(text).strip()
    # Ψάχνουμε αν υπάρχει αριθμός στο κείμενο (π.χ. 500, 1.488, 356,40)
    # Εξαιρούμε ημερομηνίες μορφής DD/MM/YYYY αν τυχόν υπάρχουν μέσα στο όνομα
    clean_text = re.sub(r'\b\d{2}/\d{2}/\d{4}\b', '', text_str)
    numbers = re.findall(r'\d+(?:[.,]\d+)?', clean_text)
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

                # Καθαρισμός ονομάτων για τα μηνύματα
                name_c = re.sub(r'\d+(?:[.,]\d+)?.*', '', str(col_c)).replace('-', '').strip() if not pd.isna(col_c) else ""
                name_e = re.sub(r'\d+(?:[.,]\d+)?.*', '', str(col_e)).replace('-', '').strip() if not pd.isna(col_e) else ""

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
