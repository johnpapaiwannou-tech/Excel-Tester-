import streamlit as st
import pandas as pd
import re
from calculator import render_calculator

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

# Render the sidebar calculator from calculator.py
render_calculator()

# Modern app design and background styling
st.markdown("""
<style>
body, .stApp, .main, .block-container {
    background: #f4f6fa;
    color: #111827;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

.block-container {
    padding: 30px 36px 36px;
    max-width: 1080px;
    margin: auto;
}

.stApp {
    background-image: url("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Logo_EV_RGB_%C2%A9_Engel_%26_V%C3%B6lkers.png/1280px-Logo_EV_RGB_%C2%A9_Engel_%26_V%C3%B6lkers.png");
    background-size: 160px auto;
    background-position: center 36px;
    background-repeat: no-repeat;
    background-attachment: fixed;
    min-height: 100vh;
    padding-top: 220px;
}

.stButton>button,
.stFileUploader>div,
.stTextInput>div>div>input,
.stSelectbox>div>div>div {
    border-radius: 16px !important;
    border: 1px solid rgba(15, 23, 42, 0.12) !important;
    box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
}

.stButton>button {
    background: linear-gradient(135deg, #0f172a, #334155) !important;
    color: white !important;
    border: none !important;
    padding: 0.9rem 1.4rem !important;
}

.stButton>button:hover {
    transform: translateY(-1px);
    box-shadow: 0 18px 35px rgba(15, 23, 42, 0.16);
}

.stAlert, .stInfo, .stWarning, .stSuccess {
    border-radius: 22px;
    border: none;
    padding: 22px 24px;
    box-shadow: 0 18px 46px rgba(15, 23, 42, 0.08);
}

.css-1d391kg {
    background: rgba(255, 255, 255, 0.95) !important;
}

h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    font-weight: 700;
}

.stMarkdown p {
    color: #475569;
    line-height: 1.8;
}

.css-1z5f7gv {
    background: rgba(255,255,255,0.98);
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 24px 50px rgba(15, 23, 42, 0.08);
}
</style>
""", unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📊 Engel & Volkers Rental Excel Tester")
        st.markdown("Ανεβάστε το αρχείο σας (CSV ή Excel) για να ελέγξετε ποια deal είναι έτοιμα για το T-Box.")
    with col2:
        st.markdown(
            """
            <div style='background:#ffffffdd;border-radius:18px;padding:20px 22px;box-shadow:0 20px 45px rgba(15,23,42,0.08);'>
                <h3 style='margin:0 0 12px;color:#0f172a;'>Γρήγορα βήματα</h3>
                <p style='margin:0;color:#475569;'>1. Φόρτωσε αρχείο CSV ή XLSX<br>2. Έλεγξε τις εκκρεμότητες<br>3. Δες ποια deal είναι έτοιμα για T-Box</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


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
