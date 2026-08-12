import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import time

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Training Portal", page_icon="🏢", layout="wide")

# --- 2. PREMIUM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    .stApp {
        background: linear-gradient(rgba(0, 31, 100, 0.8), rgba(0, 31, 100, 0.8)), 
                    url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80');
        background-size: cover; background-attachment: fixed; font-family: 'Inter', sans-serif;
    }
    header, footer, .stDeployButton, [data-testid="stHeader"] {visibility: hidden !important;}

    div[data-testid="stVerticalBlock"] > div:has(div.login-card-anchor) {
        background: white; padding: 40px 60px !important; border-radius: 20px !important;
        box-shadow: 0 40px 100px rgba(0, 0, 0, 0.6) !important;
        width: 100%; max-width: 550px; margin: auto;
    }
    .main-head { color: #00227a !important; font-weight: 700; text-align: center; font-size: 28px !important; text-transform: uppercase; margin-bottom: 25px; }
    .stButton>button { background: #00227a !important; color: white !important; width: 100%; border-radius: 10px !important; font-weight: 600; padding: 12px; border: none !important; }
    .stButton>button:hover { background: #ffb800 !important; color: #00227a !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE CONNECTION ---
def load_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=0)
        return df, conn
    except Exception as e:
        st.error(f"Connection error. Please verify Service Account Secrets.")
        return None, None

# --- 4. UI LOGIC ---
if 'view' not in st.session_state: st.session_state.view = 'login'
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

st.markdown('<div style="position:fixed;top:0;left:0;width:100%;padding:15px 50px;background:rgba(255,255,255,0.05);backdrop-filter:blur(10px);z-index:1000;color:white;font-weight:700;">LOREM IPSUM</div>', unsafe_allow_html=True)

if not st.session_state.logged_in:
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
    _, col_mid, _ = st.columns([1, 2, 1])

    with col_mid:
        st.markdown('<div class="login-card-anchor"></div>', unsafe_allow_html=True)

        if st.session_state.view == 'login':
            st.markdown('<div class="main-head">Training Portal</div>', unsafe_allow_html=True)
            email = st.text_input("Email", placeholder="Email", label_visibility="collapsed")
            pw = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
            
            if st.button("ACCESS PORTAL"):
                if email == "admin@megaworld-marketing.com" and pw == "supremo2024":
                    st.session_state.logged_in = True
                    st.session_state.is_admin = True
                    st.rerun()
                else:
                    df, conn = load_data()
                    if df is not None:
                        user = df[(df['Email'] == email) & (df['Password'].astype(str) == str(pw))]
                        if not user.empty:
                            if user.iloc[0]['Status'] == 'Approved':
                                st.session_state.logged_in = True
                                st.rerun()
                            else:
                                st.warning("⏳ Pending Approval.")
                        else:
                            st.error("Invalid Credentials.")

            if st.button("Register Account"):
                st.session_state.view = 'register'
                st.rerun()

        else:
            st.markdown('<div class="main-head">Registration</div>', unsafe_allow_html=True)
            name = st.text_input("Full Name")
            email_reg = st.text_input("Email Address")
            pass_reg = st.text_input("Password", type="password")
            
            if st.button("SUBMIT REGISTRATION"):
                df, conn = load_data()
                if df is not None:
                    # Explicitly convert sheet to list of dicts or append row
                    new_row = pd.DataFrame([{"Full_Name": name, "Email": email_reg, "Password": pass_reg, "Status": "Pending"}])
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    conn.update(data=updated_df)
                    st.success("Submitted! Awaiting approval.")
                    time.sleep(2)
                    st.session_state.view = 'login'
                    st.rerun()
            
            if st.button("Back to Login"):
                st.session_state.view = 'login'
                st.rerun()

else:
    # --- LOGGED IN CONTENT ---
    if st.session_state.is_admin:
        st.title("🛡️ Admin Approval")
        df, conn = load_data()
        pending = df[df['Status'] == 'Pending']
        if not pending.empty:
            for idx, row in pending.iterrows():
                c1, c2 = st.columns([3, 1])
                c1.write(f"{row['Full_Name']} ({row['Email']})")
                if c2.button("Approve", key=idx):
                    df.at[idx, 'Status'] = 'Approved'
                    conn.update(data=df)
                    st.rerun()
        else:
            st.info("No pending requests.")
    else:
        st.title("🏠 Training Dashboard")
        st.write("Welcome to the suite.")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()