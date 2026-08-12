import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import time

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Megaworld Training Portal", page_icon="🏢", layout="wide")

# --- 2. LUXURY CSS (Stretched & Modern) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(rgba(0, 31, 100, 0.8), rgba(0, 31, 100, 0.8)), 
                    url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80');
        background-size: cover; background-attachment: fixed; font-family: 'Inter', sans-serif;
    }
    header, footer, .stDeployButton, [data-testid="stHeader"] {visibility: hidden !important;}

    /* Navigation Bar */
    .nav-bar {
        position: fixed; top: 0; left: 0; width: 100%;
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px);
        padding: 15px 50px; z-index: 1000; display: flex; justify-content: space-between;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Stretched Luxury Card */
    div[data-testid="stVerticalBlock"] > div:has(div.login-card-anchor) {
        background: white; padding: 40px 60px !important; border-radius: 20px !important;
        box-shadow: 0 40px 100px rgba(0, 0, 0, 0.6) !important;
        width: 100%; max-width: 550px; margin: auto;
    }

    .main-head {
        color: #00227a !important; font-weight: 700; text-align: center;
        font-size: 30px !important; text-transform: uppercase; margin-bottom: 25px;
        letter-spacing: -1px;
    }

    .stButton>button {
        background: #00227a !important; color: white !important; width: 100%;
        border-radius: 10px !important; font-weight: 600; padding: 12px; border: none !important;
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
    def load_data():
        return conn.read(ttl=0)
except:
    st.error("Connecting to Secure Database...")
    st.stop()

# --- 4. SESSION STATE ---
if 'view' not in st.session_state: st.session_state.view = 'login'
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

# --- 5. TOP NAVIGATION ---
st.markdown('<div class="nav-bar"><div style="color:white; font-weight:700; letter-spacing:2px;">MEGAWORLD INTERNATIONAL</div><div style="color:white; font-size:12px;">EST. 1989</div></div>', unsafe_allow_html=True)

# --- 6. LOGIN / REGISTRATION UI ---
if not st.session_state.logged_in:
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
    _, col_mid, _ = st.columns([1, 2, 1])

    with col_mid:
        st.markdown('<div class="login-card-anchor"></div>', unsafe_allow_html=True)
        st.markdown('<div class="avatar-placeholder"></div>', unsafe_allow_html=True)

        if st.session_state.view == 'login':
            st.markdown('<div class="main-head">Training Portal</div>', unsafe_allow_html=True)
            email = st.text_input("Email", placeholder="Enter Email Address", label_visibility="collapsed")
            pw = st.text_input("Password", type="password", placeholder="Enter Password", label_visibility="collapsed")
            
            if st.button("ACCESS PORTAL"):
                # --- SUPER ADMIN CHECK (HARDCODED FOR YOU) ---
                if email == "admin@megaworld-marketing.com" and pw == "supremo2024":
                    st.session_state.logged_in = True
                    st.session_state.is_admin = True
                    st.rerun()
                
                # --- REGISTERED USER CHECK ---
                else:
                    df = load_data()
                    # We make sure password comparison is string-to-string
                    user = df[(df['Email'] == email) & (df['Password'].astype(str) == str(pw))]
                    if not user.empty:
                        if user.iloc[0]['Status'] == 'Approved':
                            st.session_state.logged_in = True
                            st.session_state.is_admin = False
                            st.rerun()
                        else:
                            st.warning("⏳ Access Pending. Your account is awaiting Admin approval.")
                    else:
                        st.error("Invalid credentials. Please try again.")

            if st.button("New here? Create an Account"):
                st.session_state.view = 'register'
                st.rerun()

        else:
            st.markdown('<div class="main-head">Registration</div>', unsafe_allow_html=True)
            new_name = st.text_input("Full Name")
            new_email = st.text_input("Email Address (Personal or Corporate)")
            new_pw = st.text_input("Create Password", type="password")
            
            if st.button("SUBMIT REGISTRATION"):
                if new_name == "" or new_email == "" or new_pw == "":
                    st.error("All fields are required.")
                else:
                    df = load_data()
                    if new_email in df['Email'].values:
                        st.error("This email is already in our system.")
                    else:
                        # Add as PENDING
                        new_row = pd.DataFrame([{"Full_Name": new_name, "Email": new_email, "Password": new_pw, "Status": "Pending"}])
                        updated_df = pd.concat([df, new_row], ignore_index=True)
                        conn.update(data=updated_df)
                        st.success("Registration sent! Please wait for Admin approval.")
                        time.sleep(2)
                        st.session_state.view = 'login'
                        st.rerun()
            
            if st.button("Already have an account? Login"):
                st.session_state.view = 'login'
                st.rerun()

# --- 7. POST-LOGIN DASHBOARD ---
else:
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    
    if st.session_state.is_admin:
        st.title("🛡️ Admin Approval Dashboard")
        st.subheader("Manage New Registrants")
        
        df = load_data()
        pending = df[df['Status'] == 'Pending']
        
        if not pending.empty:
            for index, row in pending.iterrows():
                c1, c2 = st.columns([4, 1])
                c1.write(f"👤 **{row['Full_Name']}** — *{row['Email']}*")
                # Every button gets a unique key based on the row index
                if c2.button(f"Approve User", key=f"app_{index}"):
                    df.at[index, 'Status'] = 'Approved'
                    conn.update(data=df)
                    st.success(f"Successfully Approved {row['Full_Name']}")
                    time.sleep(1)
                    st.rerun()
        else:
            st.info("No pending requests to display.")
    
    else:
        st.title("🏠 Training Dashboard")
        st.write("Welcome to the Megaworld International Executive Training Portal.")
        st.write("Your materials and presentation schedules will appear here shortly.")

    if st.sidebar.button("Sign Out"):
        st.session_state.logged_in = False
        st.rerun()