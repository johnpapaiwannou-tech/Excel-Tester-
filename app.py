import streamlit as st
import pandas as pd
import re
import datetime

# Ρύθμιση σελίδας
st.set_page_config(page_title="Engel & Volkers Rental Excel Tester", page_icon="🏠", layout="wide")

# Background logo Engel & Volkers από το web
st.markdown("""
<style>
.stApp {
    background-image: url("");
    background-size: 100%;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Engel & Volkers Rental Excel Tester")
st.write("Ανεβάστε το αρχείο σας (CSV ή Excel) για να ελέγξετε ποια deal είναι έτοιμα για το T-Box.")

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
        return numbers[-1] # Επιστρέφει τον τελευταίο αριθμό που βρήκε ως οφειλή
    return None

# Upload Αρχείου
uploaded_file = st.file_uploader("Επιλέξτε αρχείο", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Αναγνώριση τύπου αρχείου και φόρτωση
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
       
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
                col_b = str(row.iloc[1]).strip() # Κωδικός Deal
                col_c = row.iloc[2]              # Στοιχεία Συναλλαγής 1
                col_d = row.iloc[3]              # Ποσό
                col_e = row.iloc[4]              # MATCH WITH
                col_f = str(row.iloc[5]).strip() # Σχόλια / Ημερομηνία Πληρωμής
               
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
                # Κριτήρια: Όχι οφειλή στο C, Όχι οφειλή στο E, Ύπαρξη ποσού στο D, Ύπαρξη ημερομηνίας/κειμένου στο F (όχι κενό/NaN)
                has_amount_d = not pd.isna(col_d) and str(col_d).strip() != ""
                has_date_f = pd.notna(row.iloc[5]) and col_f != "" and col_f.lower() != "nan"
                print(repr(row.iloc[5]))
                # Έλεγχος αν το F περιέχει έγκυρη ημερομηνία (π.χ. μορφή με / ή -)
                contains_date = bool(re.search(r'\d{2}[/-]\d{2}[/-]\d{4}', col_f))
                if not row_has_debt and has_amount_d and has_date_f:
                    ready_deals.append(f"🟢 Είναι έτοιμο το deal (**{col_b}**) να μπεί T-Box, έχουν πληρώσει και οι δύο πλευρές")
                elif not row_has_debt:
                    # Αν δεν έχει οφειλή αλλά λείπει η ημερομηνία
                    if not contains_date:
                        pending_messages.append(f"⚠️ **Deal {col_b}**: Δεν υπάρχει έγκυρη ημερομηνία πληρωμής στη στήλη F (Σχόλια).")

            # --- ΕΜΦΑΝΙΣΗ ΑΠΟΤΕΛΕΣΜΑΤΩΝ ---
            st.markdown("---")
           
            # Στήλη Έτοιμων Deals
            st.subheader("🟢 Έτοιμα για T-Box")
            if ready_deals:
                for deal in ready_deals:
                    st.info(deal)
            else:
                st.warning("Κανένα deal δεν είναι έτοιμο για T-Box αυτή τη στιγμή.")
               
            # Στήλη Εκκρεμοτήτων
            st.markdown("---")
            st.subheader("❌ Εκκρεμότητες & Οφειλές")
            if pending_messages:
                for msg in pending_messages:
                    st.write(msg)
            else:
                st.success("Δεν βρέθηκαν εκκρεμότητες!")
               
    except Exception as e:
        st.error(f"Προέκυψε σφάλμα κατά την επεξεργασία: {e}")
