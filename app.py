import streamlit as st
import time

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Megaworld BD Portal", page_icon="🏢", layout="wide")

# --- 2. ADVANCED CSS (Animations & Styling) ---
st.markdown("""
    <style>
    /* 1. Dotted Background Pattern */
    .stApp {
        background-color: #f0f4f8;
        background-image: radial-gradient(#d1d1d1 1px, transparent 1px);
        background-size: 30px 30px;
    }

    /* 2. Splash Screen Overlay */
    #splash-screen {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: #0033a0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        color: white;
        animation: fadeOut 1.5s forwards;
        animation-delay: 2s;
    }

    /* 3. Animations */
    @keyframes fadeOut { from {opacity: 1;} to {opacity: 0; visibility: hidden;} }
    
    @keyframes slideUp {
        0% { opacity: 0; transform: translateY(50px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* 4. Login Card Styling */
    .login-card {
        background-color: white;
        padding: 50px;
        border-radius: 15px;
        box-shadow: 0px 15px 35px rgba(0,0,0,0.1);
        border-top: 8px solid #0033a0; /* That blue bar at the top of the card */
        max-width: 500px;
        margin: auto;
        text-align: center;
        animation: slideUp 1s ease-out;
    }

    /* 5. Header Bar */
    .header-bar {
        background-color: #0033a0;
        padding: 15px;
        position: fixed;
        top: 0; left: 0; width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 1000;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }

    /* 6. Text and Input Styling */
    h2 { color: #0033a0 !important; font-family: 'Segoe UI', sans-serif; font-weight: 700; }
    .stTextInput>div>div>input { border-radius: 5px; height: 45px; border: 1px solid #ddd; }
    
    /* 7. Footer */
    .footer {
        position: fixed;
        bottom: 20px; width: 100%;
        text-align: center;
        color: #888;
        font-size: 12px;
    }

    /* 8. Modern Button */
    .stButton>button {
        background-color: #0033a0 !important;
        color: white !important;
        width: 100%;
        height: 45px;
        border-radius: 5px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #00267a !important; transform: scale(1.02); }
    
    /* Hide Streamlit Header/Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIC FOR SPLASH SCREEN ---
if 'splash_done' not in st.session_state:
    # Create the Splash Screen HTML
    splash = st.empty()
    splash.markdown("""
        <div id="splash-screen">
            <h1 style="font-size: 50px;">MEGAWORLD</h1>
            <p style="letter-spacing: 5px;">INTERNATIONAL</p>
            <div style="border: 4px solid #f3f3f3; border-top: 4px solid #ffc72c; border-radius: 50%; width: 40px; height: 40px; animation: spin 2s linear infinite;"></div>
            <style>@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }</style>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(3) # How long the splash screen stays
    splash.empty()
    st.session_state.splash_done = True

# --- 4. SESSION STATE FOR LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'view' not in st.session_state:
    st.session_state.view = 'login'

# --- 5. UI CONTENT ---
if not st.session_state.logged_in:
    # Top Logo Bar
    st.markdown('<div class="header-bar"><span style="color:white; font-weight:bold; margin-left:20px;">MEGAWORLD INTERNATIONAL</span></div>', unsafe_allow_html=True)

    # Centering the Login Card
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.2, 1])

    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        if st.session_state.view == 'login':
            st.markdown("<h2>User Login</h2>", unsafe_allow_html=True)
            email = st.text_input("", placeholder="Email", label_visibility="collapsed")
            password = st.text_input("", type="password", placeholder="Password", label_visibility="collapsed")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("LOGIN"):
                if email == "admin" and password == "1234":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid Login")
            
            st.markdown("<br><a href='#' style='color:#0033a0; text-decoration:none; font-size:14px;'>Need an account? Register</a>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown('<div class="footer">© 2026 Megaworld International Training and Business Development Group. All Rights Reserved.</div>', unsafe_allow_html=True)

# --- 6. MAIN PORTAL AFTER LOGIN ---
else:
    st.markdown('<div class="header-bar"><span style="color:white; font-weight:bold; margin-left:20px;">MEGAWORLD INTERNATIONAL</span></div>', unsafe_allow_html=True)
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.success("Welcome back, Supremo! You are now viewing the full portal.")
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.session_state.splash_done = True # Skip splash on logout
        st.rerun()