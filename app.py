import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import time

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Training Portal", page_icon="🏢", layout="wide")

# --- 2. LUXURY CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    .stApp {
        background: linear-gradient(rgba(0, 31, 100, 0.8), rgba(0, 31, 100, 0.8)), 
                    url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ad?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80');
        background-size: cover; background-attachment: fixed; font-family: 'Inter', sans-serif;
    }
    header, footer, .stDeployButton, [data-testid="stHeader"] {visibility: hidden !important;}
    div[data-testid="stVerticalBlock"] > div:has(div.login-card-anchor) {
        background: white; padding: 40px 60px !important; border-radius: 20px !important;
        box-shadow: 0 40px 100px rgba(0, 0, 0, 0.6) !important;
        width: 100%; max-width: 550px; margin: auto;
    }
    .main-head { color: #00227a !important; font-weight: 700; text-align: center; font-size: 30px !important; text-transform: uppercase; margin-bottom: 25px; }
    .stButton>button { background: #00227a !important; color: white !important; width: 100%; border-radius: 10px !important; font-weight: 600; padding: 12px; border: none !important; }
    .stButton>button:hover { background: #ffb800 !important; color: #00227a !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. GSPREAD DATABASE CONNECTION ---
def get_gsheet():
    # Use the gsheets section from Secrets
    info = st.secrets["gsheets"]
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(info, scopes=scopes)
    client = gspread.authorize(creds)
    # Open by the URL in your secrets
    sheet = client.open_by_url(info["spreadsheet_url"]).sheet1
    return sheet

# --- 4. SESSION STATE ---
if 'view' not in st.session_state: st.session_state.view = 'login'
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

# --- 5. TOP NAV ---
st.markdown('<div style="position:fixed;top:0;left:0;width:100%;padding:15px 50px;background:rgba(255,255,255,0.05);backdrop-filter:blur(10px);z-index:1000;color:white;font-weight:700;">MEGAWORLD INTERNATIONAL</div>', unsafe_allow_html=True)

# --- 6. UI ---
if not st.session_state.logged_in:
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
    _, col_mid, _ = st.columns([1, 2, 1])

    with col_mid:
        st.markdown('<div class="login-card-anchor"></div>', unsafe_allow_html=True)

        if st.session_state.view == 'login':
            st.markdown('<div class="main-head">Training Portal</div>', unsafe_allow_html=True)
            email = st.text_input("Email", placeholder="Enter Email", label_visibility="collapsed")
            pw = st.text_input("Password", type="password", placeholder="Enter Password", label_visibility="collapsed")
            
            if st.button("ACCESS PORTAL"):
                if email == "admin@megaworld-marketing.com" and pw == "supremo2024":
                    st.session_state.logged_in = True
                    st.session_state.is_admin = True
                    st.rerun()
                else:
                    sheet = get_gsheet()
                    data = sheet.get_all_records()
                    df = pd.DataFrame(data)
                    user = df[(df['Email'] == email) & (df['Password'].astype(str) == str(pw))]
                    
                    if not user.empty:
                        if user.iloc[0]['Status'] == 'Approved':
                            st.session_state.logged_in = True
                            st.rerun()
                        else:
                            st.warning("⏳ Access Pending Approval.")
                    else:
                        st.error("Invalid Credentials.")

            if st.button("Register New Account"):
                st.session_state.view = 'register'
                st.rerun()

        else:
            st.markdown('<div class="main-head">Registration</div>', unsafe_allow_html=True)
            name = st.text_input("Full Name")
            email_reg = st.text_input("Email")
            pass_reg = st.text_input("Create Password", type="password")
            
            if st.button("SUBMIT REGISTRATION"):
                sheet = get_gsheet()
                # Appends a row directly to the bottom of the sheet
                sheet.append_row([name, email_reg, pass_reg, "Pending"])
                st.success("Successfully Registered! Awaiting Approval.")
                time.sleep(2)
                st.session_state.view = 'login'
                st.rerun()
            
            if st.button("Back to Login"):
                st.session_state.view = 'login'
                st.rerun()

# --- 7. ADMIN AREA ---
else:
    if st.session_state.is_admin:
        st.title("🛡️ Admin Approval Suite")
        sheet = get_gsheet()
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        
        # We need to find the rows where status is Pending
        # In gspread, rows are 1-indexed and header is row 1, so data starts at row 2
        for i, row in df.iterrows():
            if row['Status'] == 'Pending':
                c1, c2 = st.columns([4, 1])
                c1.write(f"👤 {row['Full_Name']} ({row['Email']})")
                if c2.button("Approve", key=f"app_{i}"):
                    # Update cell in the 'Status' column (Column 4 usually)
                    sheet.update_cell(i + 2, 4, "Approved")
                    st.success("Approved!")
                    st.rerun()
    else:
        st.title("🏠 Training Dashboard")
        st.write("Welcome, Agent!")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()