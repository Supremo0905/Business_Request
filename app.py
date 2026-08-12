import streamlit as st
import time

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Megaworld International | Premium Portal", page_icon="🏢", layout="wide")

# --- 2. LUXURY CSS (Glassmorphism & High-End Design) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');

    /* Full Page Background - Luxury Real Estate Look */
    .stApp {
        background: linear-gradient(rgba(0, 51, 160, 0.6), rgba(0, 51, 160, 0.6)), 
                    url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80');
        background-size: cover;
        background-position: center;
        font-family: 'Inter', sans-serif;
    }

    /* Remove Streamlit branding decorations */
    header, footer, .stDeployButton {visibility: hidden;}

    /* Top Navigation Bar */
    .nav-bar {
        position: fixed;
        top: 0; left: 0; width: 100%;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 20px 50px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        z-index: 1000;
        display: flex;
        justify-content: space-between;
    }

    /* Centered Login Container */
    .main-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }

    /* Glassmorphism Card */
    div[data-testid="stVerticalBlock"] > div:has(div.login-card-anchor) {
        background: rgba(255, 255, 255, 0.95);
        padding: 50px !important;
        border-radius: 20px !important;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5) !important;
        max-width: 450px;
        margin: auto;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    /* Titles */
    h1, h2, h3 {
        color: #0033a0 !important;
        text-align: center;
        font-weight: 700 !important;
        letter-spacing: -1px;
    }

    /* Input Fields Modernization */
    input {
        border-radius: 10px !important;
        border: 1px solid #e0e0e0 !important;
        padding: 12px !important;
        background-color: #f8f9fa !important;
    }

    /* Premium Button */
    .stButton>button {
        width: 100%;
        background-color: #0033a0 !important;
        color: white !important;
        padding: 15px !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: none !important;
        transition: 0.4s all;
        margin-top: 20px;
    }
    
    .stButton>button:hover {
        background-color: #ffc72c !important;
        color: #0033a0 !important;
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }

    /* Custom Splash Overlay */
    .splash {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: #0033a0;
        z-index: 9999;
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
        font-size: 40px;
        font-weight: bold;
        animation: fadeOut 2s forwards;
        animation-delay: 1.5s;
    }
    @keyframes fadeOut { to { opacity: 0; visibility: hidden; } }

    /* Footer Text */
    .custom-footer {
        text-align: center;
        color: rgba(255,255,255,0.7);
        font-size: 13px;
        position: fixed;
        bottom: 30px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. THE SPLASH SCREEN ---
if 'init' not in st.session_state:
    st.markdown('<div class="splash">MEGAWORLD INTERNATIONAL</div>', unsafe_allow_html=True)
    time.sleep(2.5)
    st.session_state.init = True

# --- 4. TOP NAVIGATION ---
st.markdown("""
    <div class="nav-bar">
        <div style="color: white; font-weight: bold; letter-spacing: 2px;">MEGAWORLD INTERNATIONAL</div>
        <div style="color: rgba(255,255,255,0.7); font-size: 12px;">EST. 1989</div>
    </div>
""", unsafe_allow_html=True)

# --- 5. LOGIN LOGIC ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # This spacing pushes the card to the center
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    
    # We use a column layout to wrap everything in a "Card"
    _, center_col, _ = st.columns([1, 1.5, 1])

    with center_col:
        # This empty markdown acts as an "anchor" for our CSS to find and style the card
        st.markdown('<div class="login-card-anchor"></div>', unsafe_allow_html=True)
        
        st.write("### AGENT PORTAL")
        st.write("Welcome back. Please enter your corporate credentials.")
        
        email = st.text_input("Email Address", placeholder="e.g. supremo@megaworld.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        
        if st.button("Access Portal"):
            if email == "admin" and password == "1234":
                st.session_state.logged_in = True
                st.success("Access Granted. Redirecting...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")

        st.markdown("<p style='text-align:center; font-size: 14px; margin-top:20px; color:#666;'>Forgot password? Contact IT Support</p>", unsafe_allow_html=True)

    st.markdown('<div class="custom-footer">© 2026 Megaworld International Training and Business Development Group.</div>', unsafe_allow_html=True)

# --- 6. POST-LOGIN (DASHBOARD) ---
else:
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    st.title("Welcome to the Executive Suite")
    st.write("You are logged in as Supremo.")
    
    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()