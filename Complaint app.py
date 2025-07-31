!pip install gspread oauth2client google-auth
import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Customer Complaint Form", page_icon="📨")

# --- GOOGLE SHEETS SETUP ---
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(r"C:\Users\bless\Downloads\google_service_account.json", scopes=scope)

client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Md_LKhrhsH9KJ1xayBQbkgb1NL9lZhkzboyGfmqYdSs/edit")
worksheet = sheet.sheet1

# --- FORM UI ---
st.title("📨 Submit a Customer Complaint")
st.markdown("Please fill out the form below to submit your complaint.")

with st.form("complaint_form", clear_on_submit=True):
    full_name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    transaction_date = st.date_input("Transaction Date")
    transaction_amount = st.number_input("Transaction Amount", min_value=0.0, format="%.2f")
    complaint_type = st.selectbox("Complaint Type", ["Failed Transaction", "Double Debit", "Delay in Reversal", "Others"])
    description = st.text_area("Complaint Description")

    submitted = st.form_submit_button("Submit Complaint")

    if submitted:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        worksheet.append_row([now, full_name, email, phone, str(transaction_date), transaction_amount, complaint_type, description, "Pending"])
        st.success("✅ Complaint submitted successfully!")
