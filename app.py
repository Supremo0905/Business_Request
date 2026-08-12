import streamlit as st
import time

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Training Portal | Executive Suite", page_icon="🏢", layout="wide")

# --- 2. LUXURY RESPONSIVE CSS (Wider & Balanced) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    /* Background and Global Styles */
    .stApp {
        background: linear-gradient(rgba(0, 31, 100, 0.75), rgba(0, 31, 100, 0.75)), 
                    url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
    }

    /* Remove Streamlit branding */
    header, footer, .stDeployButton, [data-testid="stHeader"] {visibility: hidden !important;}

    /* RESPONSIVE TOP NAV */
    .nav-bar {
        position: fixed;
        top: 0; left: 0; width: 100%;
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        padding: 15px 50px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        z-index: 1000;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .nav-bar .logo { color: white; font-weight: 700; letter-spacing: 2px; font-size: 20px; }
    .nav-bar .meta { color: rgba(255,255,255,0.6); font-size: 11px; }

    /* WIDER & STRETCHED LOGIN CARD FIX */
    div[data-testid="stVerticalBlock"] > div:has(div.login-card-anchor) {
        background: rgba(255, 255, 255, 1);
        padding: 40px 60px !important; /* Balanced padding: less vertical, more horizontal */
        border-radius: 20px !important;
        box-shadow: 0 40px 100px -20px rgba(0, 0, 0, 0.8) !important;
        width: 100%;
        max-width: 550px; /* STRETCHED: Increased from 420px to 550px */
        margin: auto;
        border: none !important;
    }

    /* Styling for the Avatar placeholder (Better proportions) */
    .avatar-placeholder {
        width: 70px;
        height: 70px;
        background: #f0f2f6;
        border-radius: 15px;
        margin: 0 auto 20px auto;
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.05);
    }

    /* Titles & Text */
    h2 {
        color: #00227a !important;
        font-weight: 700 !important;
        letter-spacing: -1px !important;
        margin-bottom: 5px !important;
        text-align: center;
        font-size: 32px !important; /* Larger and bolder */
    }
    .sub-text {
        color: #666 !important;
        text-align: center;
        margin-bottom: 25px !important;
        font-size: 15px;
    }

    /* Form Fields Styling */
    .stTextInput input {
        border-radius: 8px !important;
        background: #f8f9fc !important;
        padding: 12px 15px !important;
        border: 1px solid #ddd !important;
        font-size: 15px !important;
    }
    
    /* ACCESS PORTAL BUTTON (Balanced width) */
    .stButton>button {
        background: #00227a !important;
        color: white !important;
        width: 100%;
        padding: 12px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: none !important;
        margin-top: 10px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #ffb800 !important;
        color: #00227a !important;
        transform: translateY(-2px);
    }

    /* FORGOT PASSWORD LINK */
    .forgot-link {
        margin-top: 25px;
        text-align: center;
        font-size: 13px;
        color: #777;
    }
    .forgot-link a {
        color: #00227a;
        text-decoration: none;
        font-weight: 600;
    }

    /* Footer Text */
    .footer-note {
        position: fixed;
        bottom: 20px;
        width: 100%;
        text-align: center;
        color: rgba(255,255,255,0.4);
        font-size: 11px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE LOGIC ---
if 'initialized' not in st.session_state:
    st.session_state.initialized = True

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- 4. TOP NAVIGATION ---
st.markdown("""
    <div class="nav-bar">
        <div class="logo">LOREM IPSUM</div>
        <div class="meta">EST. 1989</div>
    </div>
""", unsafe_allow_html=True)

# --- 5. CENTERED LOGIN CONTENT ---
if not st.session_state.logged_in:
    # Spacer to push card down
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
    
    # We use a wider column setting to allow the card to "stretch"
    _, col_mid, _ = st.columns([1, 2, 1])

    with col_mid:
        st.markdown('<div class="login-card-anchor"></div>', unsafe_allow_html=True)
        st.markdown('<div class="avatar-placeholder"></div>', unsafe_allow_html=True)
        
        st.markdown("<h2>TRAINING PORTAL</h2>", unsafe_allow_html=True)
        st.markdown('<p class="sub-text">Welcome back. Enter your credentials to access the suite.</p>', unsafe_allow_html=True)
        
        # Creating a neat layout inside the card
        user_input = st.text_input("User ID", placeholder="Corporate Email / ID", label_visibility="collapsed")
        pass_input = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
        
        if st.button("ACCESS PORTAL"):
            if user_input == "admin" and pass_input == "1234":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials.")

        st.markdown(f"""
            <div class="forgot-link">
                Forgot password? <br>
                <a href="mailto:mwi.bdcmanagement@megaworld-marketing.com">contact mwi.bdcmanagement@megaworld-marketing.com</a>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="footer-note">© 2026 TRAINING & BUSINESS DEVELOPMENT GROUP. PRIVATE ACCESS.</div>', unsafe_allow_html=True)

# --- 6. AUTHENTICATED AREA ---
else:
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    st.title("Admin Dashboard")
    st.success("Authorized. Welcome to the Training Portal.")
    
    if st.sidebar.button("Sign Out"):
        st.session_state.logged_in = False
        st.rerun()