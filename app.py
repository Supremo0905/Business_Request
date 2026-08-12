import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import time

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Training Portal | Executive Suite", page_icon="🏢", layout="wide")

# --- 2. LUXURY CSS (Fixed Text Wrap & Responsive) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(rgba(0, 31, 100, 0.8), rgba(0, 31, 100, 0.8)), 
                    url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80');
        background-size: cover; background-attachment: fixed; font-family: 'Inter', sans-serif;
    }
    header, footer, .stDeployButton, [data-testid="stHeader"] {visibility: hidden !important;}
    
    /* Login/Register Card */
    div[data-testid="stVerticalBlock"] > div:has(div.login-card-anchor) {
        background: white; 
        padding: 40px 50px !important; 
        border-radius: 24px !important;
        box-shadow: 0 50px 100px rgba(0, 0, 0, 0.5) !important;
        width: 100%; 
        max-width: 550px; 
        margin: auto; 
    }

    /* Fixed Heading - No wrapping */
    .main-head {
        color: #00227a !important; 
        font-weight: 700; 
        text-align: center; 
        font-size: 32px !important; /* Slightly smaller to prevent breaking */
        letter-spacing: -1px;
        margin-bottom: 20px;
        text-transform: uppercase;
    }

    .stButton>button { 
        background: #00227a !important; 
        color: white !important; 
        width: 100% !important; 
        border-radius: 10px !important; 
        font-weight: 600; 
        border: none !important; 
    }
    .stButton>button:hover { background: #ffb800 !important; color: #00227a !important; }

    .avatar-placeholder {
        width: 70px; height: 70px; background: #f0f2f6;
        border-radius: 15px; margin: 0 auto 20px auto;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE CONNECTION ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    def get_users():
        return conn.read(ttl=0)
except Exception as e:
    st.error("⚠️ Connection Error: Please check your Google Sheet Link in Secrets.")
    st.stop()

# --- 4. SESSION STATE ---
if 'view' not in st.session_state: st.session_state.view = 'login'
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- 5. CENTERED UI ---
if not st.session_state.logged_in:
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    _, col_mid, _ = st.columns([1, 2, 1])

    with col_mid:
        st.markdown('<div class="login-card-anchor"></div>', unsafe_allow_html=True)
        st.markdown('<div class="avatar-placeholder"></div>', unsafe_allow_html=True)

        if st.session_state.view == 'login':
            st.markdown('<div class="main-head">Training Portal</div>', unsafe_allow_html=True)
            email = st.text_input("Email", placeholder="Corporate Email", label_visibility="collapsed")
            pw = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
            
            if st.button("ACCESS PORTAL"):
                users_df = get_users()
                # Ensure column names match your sheet exactly!
                user_record = users_df[(users_df['Email'] == email) & (users_df['Password'].astype(str) == str(pw))]
                
                if not user_record.empty:
                    if user_record.iloc[0]['Status'] == 'Approved' or user_record.iloc[0]['Role'] == 'Admin':
                        st.session_state.logged_in = True
                        st.session_state.user_role = user_record.iloc[0]['Role']
                        st.rerun()
                    else:
                        st.warning("⚠️ Pending Admin Approval.")
                else:
                    st.error("Invalid credentials.")

            if st.button("Create Account"):
                st.session_state.view = 'register'
                st.rerun()

        else:
            st.markdown('<div class="main-head">Registration</div>', unsafe_allow_html=True)
            name = st.text_input("Full Name")
            email_reg = st.text_input("Email")
            pass_reg = st.text_input("Create Password", type="password")
            
            if st.button("SUBMIT REGISTRATION"):
                users_df = get_users()
                new_user = pd.DataFrame([{"Full_Name": name, "Email": email_reg, "Password": pass_reg, "Status": "Pending", "Role": "User"}])
                updated_df = pd.concat([users_df, new_user], ignore_index=True)
                conn.update(data=updated_df)
                st.success("Submitted! Awaiting approval.")
                time.sleep(2)
                st.session_state.view = 'login'
                st.rerun()

            if st.button("Back to Login"):
                st.session_state.view = 'login'
                st.rerun()

else:
    st.title("Logged In!")
    if st.button("Sign Out"):
        st.session_state.logged_in = False
        st.rerun()