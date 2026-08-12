import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import time

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Megaworld BD Portal", page_icon="🏢", layout="wide")

# --- 2. CUSTOM CSS (The "Modernizer") ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #f4f7f9;
    }

    /* Top Navigation Bar Simulation */
    .top-nav {
        background-color: #0033a0; /* Megaworld Blue */
        padding: 15px;
        border-radius: 0px 0px 15px 15px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }

    /* Animation for the Login Card */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .login-card {
        background-color: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
        animation: fadeIn 0.8s ease-out;
        max-width: 450px;
        margin: auto;
    }

    /* Button Styling */
    .stButton>button {
        background-color: #0033a0;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 25px;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #ffc72c; /* Megaworld Gold */
        color: #0033a0;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        justify-content: center;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: white;
        border-radius: 10px 10px 0px 0px;
        padding: 0px 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE (Handling Login/Register) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'view' not in st.session_state:
    st.session_state.view = 'login'

# --- 4. GOOGLE SHEETS CONNECTION ---
# Make sure you have your secrets set up for this!
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.error("GSheets Connection not configured.")

# --- 5. LOGIN / REGISTER UI ---
if not st.session_state.logged_in:
    # Centered Container
    _, col2, _ = st.columns([1, 2, 1])

    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        if st.session_state.view == 'login':
            st.subheader("🏢 BD Agent Portal Login")
            user = st.text_input("Username / REMS ID")
            pw = st.text_input("Password", type="password")
            
            if st.button("Login"):
                if user == "admin" and pw == "1234": # Basic logic for now
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            
            st.caption("Don't have an account?")
            if st.button("Register Here"):
                st.session_state.view = 'register'
                st.rerun()

        else:
            st.subheader("📝 Agent Registration")
            new_user = st.text_input("Full Name")
            rems_id = st.text_input("REMS ID")
            new_pw = st.text_input("Create Password", type="password")
            
            if st.button("Complete Registration"):
                st.success("Account created! Please log in.")
                time.sleep(1)
                st.session_state.view = 'login'
                st.rerun()
            
            if st.button("Back to Login"):
                st.session_state.view = 'login'
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. THE MAIN PORTAL (Logged In) ---
else:
    # Top Custom Header
    st.markdown('<div class="top-nav"><h1>MEGAWORLD INTERNATIONAL</h1><p>Training & Business Development Group</p></div>', unsafe_allow_html=True)

    # Top Menu Navigation using Tabs
    tab_dashboard, tab_tripping, tab_key, tab_training = st.tabs([
        "🏠 Dashboard", "📍 Site Tripping", "🔑 Key Request", "📚 Training Request"
    ])

    with tab_dashboard:
        st.subheader("Welcome back, Supremo!")
        # Add your Monitoring dashboard code here (st.dataframe, etc.)
        st.info("Here you can monitor the status of your submitted requests.")

    with tab_tripping:
        with st.form("trip_form"):
            st.write("### New Site Tripping Request")
            name = st.text_input("Requester Name")
            client = st.text_input("Client Name")
            project = st.selectbox("Project Selection", ["Uptown Bonifacio", "McKinley Hill", "Westside City"])
            date = st.date_input("Tripping Date")
            if st.form_submit_button("Submit Request"):
                st.success("Tripping Request Sent!")

    with tab_key:
        with st.form("key_form"):
            st.write("### Key Requisition")
            unit = st.text_input("Unit Number")
            purpose = st.text_area("Purpose")
            if st.form_submit_button("Request Key"):
                st.balloons()

    with tab_training:
        st.write("### Book a Presentation")
        # Add Training fields here...

    # Sidebar Logout
    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()