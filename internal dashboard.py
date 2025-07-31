import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- GOOGLE SHEETS CONFIG ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(
    r"C:\Users\bless\Downloads\google_service_account.json", scopes=scope
)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Md_LKhrhsH9KJ1xayBQbkgb1NL9lZhkzboyGfmqYdSs/edit").sheet1
data = sheet.get_all_records()
df = pd.DataFrame(data)

# --- CLEAN COLUMN NAMES ---
df.columns = [str(col).strip() for col in df.columns]  # Fixed here to avoid outputting False

# --- STREAMLIT PAGE CONFIG ---
st.set_page_config(page_title="E-Business Complaints Dashboard", page_icon="🛠️", layout="wide")
st.title("🛠️ Internal Complaints Dashboard")
st.markdown("<hr>", unsafe_allow_html=True)

# --- DATE FILTERING ---
if not df.empty and "Date Submitted" in df.columns:
    df["Date Submitted"] = pd.to_datetime(df["Date Submitted"], errors='coerce')

    st.subheader("📅 Filter by Submission Date")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=df["Date Submitted"].min().date())
    with col2:
        end_date = st.date_input("End Date", value=df["Date Submitted"].max().date())

    df = df[
        (df["Date Submitted"].dt.date >= start_date) &
        (df["Date Submitted"].dt.date <= end_date)
    ]

# --- FILTER BY COMPLAINT TYPE ---
if "Complaint Type" in df.columns:
    st.subheader("📂 Filter by Complaint Type")
    complaint_options = ["All"] + sorted(df["Complaint Type"].dropna().unique().tolist())
    filter_type = st.selectbox("Select Complaint Type", complaint_options)

    if filter_type != "All":
        df = df[df["Complaint Type"] == filter_type]
else:
    st.warning("⚠️ 'Complaint Type' column not found in the dataset.")

# --- DISPLAY TABLE ---
st.subheader(f"📋 {len(df)} Complaints Displayed")
st.dataframe(df)

# --- DOWNLOAD BUTTON ---
st.download_button("⬇️ Download Complaints", data=df.to_csv(index=False),
                   file_name="filtered_complaints_log.csv", mime="text/csv")

# --- OPTIONAL: Clear stray output like 'False'
st.write("")
