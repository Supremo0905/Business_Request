import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import time

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Training Portal", page_icon="🏢", layout="wide")

# --- 2. LUXURY CSS ---
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

    .main-head { color: #00227a !important; font-weight: 700; text-align: center; font-size: 30px !important; text-transform: uppercase; margin-bottom: 25px; }
    .stButton>button { background: #00227a !important; color: white !important; width: 100%; border-radius: 10px !important; font-weight: 600; padding: 12px; border: none !important; }
    .stButton>button:hover { background: #ffb800 !important; color: #00227a !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SMART DATABASE CONNECTION ---
def load_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=0)
        
        # SAFETY CHECK: If sheet is empty or missing columns, create them
        required_columns = ['Full_Name', 'Email', 'Password', 'Status']
        if df is None or df.empty:
            df = pd.DataFrame(columns=required_columns)
        for col in required_columns:
            if col not in df.columns:
                df[col] = None
        
        return df, conn
    except Exception as e:
        st.error(f"🛑 Connection Error: {e}")
        return None, None

# --- 4. SESSION STATE ---
if 'view' not in st.session_state: st.session_state.view = 'login'
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

# --- 5. UI ---
st.markdown('<div style="position:fixed;top:0;left:0;width:100%;padding:15px 50px;background:rgba(255,255,255,0.05);backdrop-filter:blur(10px);border-bottom:1px solid rgba(255,255,255,0.1);z-index:1000;color:white;font-weight:700;">MEGAWORLD INTERNATIONAL</div>', unsafe_allow_html=True)

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
                # ADMIN BYPASS
                if email == "admin@megaworld-marketing.com" and pw == "supremo2024":
                    st.session_state.logged_in = True
                    st.session_state.is_admin = True
                    st.rerun()
                else:
                    df, conn = load_data()
                    if df is not None and not df.empty:
                        # Normalize columns to handle minor typos
                        user = df[(df['Email'] == email) & (df['Password'].astype(str) == str(pw))]
                        if not user.empty:
                            if user.iloc[0]['Status'] == 'Approved':
                                st.session_state.logged_in = True
                                st.rerun()
                            else:
                                st.warning("⏳ Access Pending Approval.")
                        else:
                            st.error("Invalid Credentials.")

            if st.button("New Agent? Register"):
                st.session_state.view = 'register'
                st.rerun()

        else:
            st.markdown('<div class="main-head">Registration</div>', unsafe_allow_html=True)
            new_name = st.text_input("Full Name")
            new_email = st.text_input("Email Address")
            new_pw = st.text_input("Create Password", type="password")
            
            if st.button("SUBMIT REGISTRATION"):
                df, conn = load_data()
                if df is not None:
                    if new_email in df['Email'].values:
                        st.error("Email already registered.")
                    else:
                        new_row = pd.DataFrame([{"Full_Name": new_name, "Email": new_email, "Password": new_pw, "Status": "Pending"}])
                        updated_df = pd.concat([df, new_row], ignore_index=True)
                        conn.update(data=updated_df)
                        st.success("Registration sent! Please notify Admin.")
                        time.sleep(2)
                        st.session_state.view = 'login'
                        st.rerun()
            
            if st.button("Back to Login"):
                st.session_state.view = 'login'
                st.rerun()

else:
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    if st.session_state.is_admin:
        st.title("🛡️ Admin Dashboard")
        df, conn = load_data()
        if df is not None:
            # Added a check to make sure 'Status' exists before filtering
            if 'Status' in df.columns:
                pending = df[df['Status'] == 'Pending']
                if not pending.empty:
                    for idx, row in pending.iterrows():
                        c1, c2 = st.columns([4,1])
                        c1.write(f"👤 {row['Full_Name']} ({row['Email']})")
                        if c2.button("Approve", key=f"btn_{idx}"):
                            df.at[idx, 'Status'] = 'Approved'
                            conn.update(data=df)
                            st.rerun()
                else:
                    st.info("No pending requests.")
            else:
                st.error("Sheet format error: 'Status' column missing.")
    else:
        st.title("Welcome to the Portal")
        st.write("Logged in successfully.")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()