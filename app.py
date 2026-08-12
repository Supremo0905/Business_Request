import streamlit as st
import time

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Executive Portal", page_icon="🏢", layout="wide")

# --- 2. LUXURY RESPONSIVE CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    /* Background and Global Styles */
    .stApp {
        background: linear-gradient(rgba(0, 31, 100, 0.7), rgba(0, 31, 100, 0.7)), 
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
        padding: 15px 5%;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        z-index: 1000;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .nav-bar .logo { color: white; font-weight: 700; letter-spacing: 2px; font-size: clamp(14px, 4vw, 18px); }
    .nav-bar .meta { color: rgba(255,255,255,0.6); font-size: 11px; }

    /* MOBILE RESPONSIVE LOGIN CARD */
    div[data-testid="stVerticalBlock"] > div:has(div.login-card-anchor) {
        background: rgba(255, 255, 255, 0.98);
        padding: clamp(30px, 8vw, 60px) !important;
        border-radius: 24px !important;
        box-shadow: 0 40px 100px -20px rgba(0, 0, 0, 0.6) !important;
        width: 100%;
        max-width: 420px; /* PC Width */
        margin: auto;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Styling for the Logo/Avatar placeholder on the card */
    .avatar-placeholder {
        width: 80px;
        height: 80px;
        background: #f0f2f6;
        border-radius: 20px;
        margin: 0 auto 25px auto;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.05);
    }

    /* Titles & Text */
    h2 {
        color: #00227a !important;
        font-weight: 700 !important;
        letter-spacing: -1.5px !important;
        margin-bottom: 10px !important;
        text-align: center;
        font-size: 28px !important;
    }
    .sub-text {
        color: #555 !important;
        text-align: center;
        margin-bottom: 30px !important;
        font-size: 14px;
        line-height: 1.6;
    }

    /* Form Fields */
    .stTextInput input {
        border-radius: 12px !important;
        background: #f8f9fc !important;
        padding: 15px !important;
        border: 1px solid #dee2e6 !important;
        font-size: 14px !important;
    }
    
    /* ACCESS PORTAL BUTTON */
    .stButton>button {
        background: #00227a !important;
        color: white !important;
        width: 100%;
        padding: 16px !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        border: none !important;
        margin-top: 15px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: #ffb800 !important;
        color: #00227a !important;
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }

    /* FORGOT PASSWORD LINK */
    .forgot-link {
        margin-top: 30px;
        text-align: center;
        font-size: 13px;
        color: #666;
    }
    .forgot-link a {
        color: #00227a;
        text-decoration: none;
        font-weight: 600;
    }

    /* SPLASH SCREEN */
    .splash {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: #001f64;
        z-index: 10000;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        animation: fadeOut 1s forwards;
        animation-delay: 1.5s;
    }
    @keyframes fadeOut { to { opacity: 0; visibility: hidden; } }

    /* Footer for mobile/desktop */
    .footer-note {
        position: fixed;
        bottom: 20px;
        width: 100%;
        text-align: center;
        color: rgba(255,255,255,0.5);
        font-size: 11px;
        z-index: 500;
    }

    /* Media query to ensure card looks good on mobile screens */
    @media (max-width: 640px) {
        div[data-testid="stVerticalBlock"] > div:has(div.login-card-anchor) {
            max-width: 90% !important;
            padding: 30px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SPLASH SCREEN ANIMATION ---
if 'initialized' not in st.session_state:
    st.markdown('<div class="splash"><h1 style="color:white; letter-spacing:10px;">LOREM IPSUM</h1><div style="width:50px; height:2px; background:#ffb800;"></div></div>', unsafe_allow_html=True)
    time.sleep(1.8)
    st.session_state.initialized = True

# --- 4. TOP NAVIGATION (MOBILE & PC READY) ---
st.markdown("""
    <div class="nav-bar">
        <div class="logo">LOREM IPSUM</div>
        <div class="meta">EST. 1989</div>
    </div>
""", unsafe_allow_html=True)

# --- 5. CENTERED LOGIN CONTENT ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Use empty space to vertical center
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    
    # Grid system: 3 columns (Narrow, Content, Narrow)
    # The middle column acts as the card wrapper
    _, col_mid, _ = st.columns([0.1, 2, 0.1]) if st.session_state.get('mobile_view', False) else st.columns([1, 1.2, 1])

    with col_mid:
        st.markdown('<div class="login-card-anchor"></div>', unsafe_allow_html=True)
        st.markdown('<div class="avatar-placeholder"></div>', unsafe_allow_html=True)
        
        st.markdown("<h2>AGENT PORTAL</h2>", unsafe_allow_html=True)
        st.markdown('<p class="sub-text">Enter your credentials to access the executive dashboard.</p>', unsafe_allow_html=True)
        
        user_input = st.text_input("User ID", placeholder="Corporate ID", label_visibility="collapsed")
        pass_input = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
        
        if st.button("ACCESS PORTAL"):
            if user_input == "admin" and pass_input == "1234":
                st.session_state.logged_in = True
                st.success("Authorized. Initializing suite...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Access Denied: Invalid Credentials.")

        st.markdown(f"""
            <div class="forgot-link">
                Forgot password? <br>
                <a href="mailto:mwi.bdcmanagement@megaworld-marketing.com">contact mwi.bdcmanagement@megaworld-marketing.com</a>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="footer-note">© 2026 TRAINING & BUSINESS DEVELOPMENT GROUP. PRIVATE PORTAL.</div>', unsafe_allow_html=True)

# --- 6. AUTHENTICATED AREA ---
else:
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    st.title("Executive Dashboard")
    st.info("You are currently viewing the restricted Management Portal.")
    
    if st.sidebar.button("Sign Out"):
        st.session_state.logged_in = False
        st.rerun()