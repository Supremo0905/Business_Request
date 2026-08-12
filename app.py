import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import time

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Megaworld BD Portal", page_icon="🏢", layout="wide")

# --- 2. FIXED CUSTOM CSS ---
st.markdown("""
    <style>
    /* Force the main background color */
    .stApp {
        background-color: #f4f7f9;
    }

    /* Top Navigation Bar Styling */
    .top-nav {
        background-color: #0033a0; /* Megaworld Blue */
        padding: 20px;
        border-radius: 0px 0px 15px 15px;
        color: white !important; /* Force text white */
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    .top-nav h1, .top-nav p {
        color: white !important;
        margin: 0;
    }

    /* Modern Login Card */
    .login-card {
        background-color: #ffffff; /* Pure white */
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
        max-width: 450px;
        margin: auto;
        border: 1px solid #e0e0e0;
    }

    /* FORCE TEXT COLOR INSIDE LOGIN AREA */
    .login-card h3, .login-card p, .login-card label, .login-card div {
        color: #1f1f1f !important; /* Dark charcoal color */
    }

    /* Fix for Streamlit input labels (the text above boxes) */
    .stWidgetLabel p {
        color: #1f1f1f !important;
        font-weight: 600 !important;
    }

    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .login-container {
        animation: fadeIn 0.8s ease-out;
    }

    /* Button Styling */
    .stButton>button {
        background-color: #0033a0;
        color: white !important;
        border-radius: 8px;
        width: 100%;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #ffc72c;
        color: #0033a0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'view' not in st.session_state:
    st.session_state.view = 'login'

# --- 4. LOGIN / REGISTER UI ---
if not st.session_state.logged_in:
    # Use columns to center the card
    _, col2, _ = st.columns([1, 2, 1])

    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        if st.session_state.view == 'login':
            st.markdown("<h3>🏢 Agent Login</h3>", unsafe_allow_html=True)
            user = st.text_input("Username or REMS ID", placeholder="Enter your ID...")
            pw = st.text_input("Password", type="password", placeholder="Enter password...")
            
            if st.button("LOG IN"):
                if user == "admin" and pw == "1234":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")
            
            st.markdown("<p style='text-align:center; margin-top:15px;'>Don't have an account?</p>", unsafe_allow_html=True)
            if st.button("REGISTER NEW ACCOUNT"):
                st.session_state.view = 'register'
                st.rerun()

        else:
            st.markdown("<h3>📝 Agent Registration</h3>", unsafe_allow_html=True)
            new_user = st.text_input("Full Name")
            rems_id = st.text_input("REMS ID")
            new_pw = st.text_input("Create Password", type="password")
            
            if st.button("COMPLETE REGISTRATION"):
                st.success("Success! Please log in.")
                time.sleep(1)
                st.session_state.view = 'login'
                st.rerun()
            
            if st.button("CANCEL"):
                st.session_state.view = 'login'
                st.rerun()
        
        st.markdown('</div></div>', unsafe_allow_html=True)

# --- 5. THE MAIN PORTAL (Logged In) ---
else:
    # Top Header
    st.markdown('<div class="top-nav"><h1>MEGAWORLD INTERNATIONAL</h1><p>Training & Business Development Group</p></div>', unsafe_allow_html=True)

    tab_dashboard, tab_requests, tab_manage = st.tabs(["🏠 Dashboard", "📝 Submit Requests", "⚙️ Admin Tools"])

    with tab_dashboard:
        st.subheader("Welcome back, Supremo!")
        st.write("You are logged in to the BD Monitoring Portal.")
        # Place your Dashboard metrics/GSheets display here

    with tab_requests:
        request_type = st.selectbox("What would you like to request?", ["Site Tripping", "Key Requisition", "Training/Presentation"])
        
        with st.form("request_form"):
            st.write(f"### {request_type} Form")
            # Dynamic fields based on selection
            name = st.text_input("Requester Name")
            details = st.text_area("Details / Notes")
            
            if st.form_submit_button("Submit to BD Group"):
                st.success(f"Your {request_type} has been submitted!")

    with tab_manage:
        st.info("This area is restricted to authorized personnel.")

    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()