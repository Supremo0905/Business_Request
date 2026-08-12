import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import time

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Training Portal | Executive Suite", page_icon="🏢", layout="wide")

# --- 2. PREMIUM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    .stApp {
        background: linear-gradient(rgba(0, 31, 100, 0.8), rgba(0, 31, 100, 0.8)), 
                    url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80');
        background-size: cover; background-attachment: fixed; font-family: 'Inter', sans-serif;
    }
    header, footer, .stDeployButton, [data-testid="stHeader"] {visibility: hidden !important;}
    
    @keyframes viewTransition { 0% { opacity: 0; transform: translateX(20px); } 100% { opacity: 1; transform: translateX(0); } }

    div[data-testid="stVerticalBlock"] > div:has(div.login-card-anchor) {
        background: white; padding: 50px 60px !important; border-radius: 24px !important;
        box-shadow: 0 50px 100px rgba(0, 0, 0, 0.5) !important;
        width: 100%; max-width: 550px; margin: auto; animation: viewTransition 0.6s ease-out;
    }
    h2 { color: #00227a !important; font-weight: 700; text-align: center; font-size: 36px !important; }
    .stButton>button { background: #00227a !important; color: white !important; width: 100%; padding: 14px !important; border-radius: 10px !important; font-weight: 600; text-transform: uppercase; border: none !important; transition: 0.4s; }
    .stButton>button:hover { background: #ffb800 !important; color: #00227a !important; }
    .secondary-btn>div>button { background: transparent !important; color: #00227a !important; border: 2px solid #00227a !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

def get_users():
    return conn.read(ttl=0) # Read fresh data every time

# --- 4. SESSION STATE ---
if 'view' not in st.session_state: st.session_state.view = 'login'
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_role' not in st.session_state: st.session_state.user_role = None

# --- 5. LOGIN/REGISTER LOGIC ---
if not st.session_state.logged_in:
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    _, col_mid, _ = st.columns([1, 2, 1])

    with col_mid:
        st.markdown('<div class="login-card-anchor"></div>', unsafe_allow_html=True)
        
        # --- LOGIN VIEW ---
        if st.session_state.view == 'login':
            st.markdown("<h2>TRAINING PORTAL</h2>", unsafe_allow_html=True)
            email = st.text_input("Email", placeholder="Corporate Email", label_visibility="collapsed")
            pw = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
            
            if st.button("ACCESS PORTAL"):
                users_df = get_users()
                # Check if user exists
                user_record = users_df[(users_df['Email'] == email) & (users_df['Password'] == str(pw))]
                
                if not user_record.empty:
                    status = user_record.iloc[0]['Status']
                    role = user_record.iloc[0]['Role']
                    
                    if status == 'Approved' or role == 'Admin':
                        st.session_state.logged_in = True
                        st.session_state.user_role = role
                        st.rerun()
                    else:
                        st.warning("⚠️ Your account is awaiting Admin Approval.")
                else:
                    st.error("Invalid Email or Password.")

            if st.button("CREATE AN ACCOUNT"):
                st.session_state.view = 'register'
                st.rerun()

        # --- REGISTRATION VIEW ---
        else:
            st.markdown("<h2>REGISTRATION</h2>", unsafe_allow_html=True)
            full_name = st.text_input("Full Name", placeholder="Full Name")
            email_reg = st.text_input("Email", placeholder="Corporate Email")
            pass_reg = st.text_input("Create Password", type="password")
            
            if st.button("SUBMIT FOR APPROVAL"):
                users_df = get_users()
                if email_reg in users_df['Email'].values:
                    st.error("Email already exists!")
                else:
                    # Create new row
                    new_user = pd.DataFrame([{
                        "Full_Name": full_name,
                        "Email": email_reg,
                        "Password": pass_reg,
                        "Status": "Pending",
                        "Role": "User"
                    }])
                    updated_df = pd.concat([users_df, new_user], ignore_index=True)
                    conn.update(data=updated_df)
                    st.success("Success! Contact Admin for approval.")
                    time.sleep(2)
                    st.session_state.view = 'login'
                    st.rerun()

            if st.button("BACK TO LOGIN"):
                st.session_state.view = 'login'
                st.rerun()

# --- 6. AUTHENTICATED AREA ---
else:
    st.sidebar.title("Navigation")
    if st.sidebar.button("Sign Out"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.user_role == 'Admin':
        st.title("🛡️ Admin Approval Dashboard")
        st.write("Review and approve new registrants below.")
        
        users_df = get_users()
        pending_users = users_df[users_df['Status'] == 'Pending']
        
        if not pending_users.empty:
            for index, row in pending_users.iterrows():
                col1, col2 = st.columns([3, 1])
                col1.write(f"**{row['Full_Name']}** ({row['Email']})")
                if col2.button(f"Approve", key=index):
                    users_df.at[index, 'Status'] = 'Approved'
                    conn.update(data=users_df)
                    st.success(f"Approved {row['Full_Name']}!")
                    st.rerun()
        else:
            st.info("No pending approvals.")

    else:
        st.title("🏠 Training Dashboard")
        st.write("Welcome to the Training Suite. Content coming soon.")