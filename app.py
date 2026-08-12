import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="BD Development Portal", layout="wide")

# 1. SETUP GOOGLE SHEETS CONNECTION
# Note: You will put your Sheet URL in the "Secrets" later
conn = st.connection("gsheets", type=GSheetsConnection)

# --- LOGIN SECTION ---
def login():
    st.sidebar.title("🔐 Staff Access")
    password = st.sidebar.text_input("Enter Admin Password", type="password")
    if password == "admin123": # Change this to your preferred password
        return True
    return False

is_admin = login()

# --- MAIN INTERFACE ---
st.title("🚀 Business Development Request Portal")
st.markdown("Please select a request type below to submit your details.")

# Create Tabs for different requests
tab1, tab2, tab3 = st.tabs(["📍 Site Tripping", "🔑 Key Request", "📚 Training Request"])

# --- TAB 1: SITE TRIPPING ---
with tab1:
    with st.form("tripping_form"):
        name = st.text_input("Requester Name")
        project = st.text_input("Project Name/Location")
        date = st.date_input("Target Date")
        submit = st.form_submit_button("Submit Tripping Request")
        
        if submit and name:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Request_Type": "Site Tripping",
                "Requester_Name": name,
                "Details": f"Project: {project}, Date: {date}",
                "Status": "Pending"
            }])
            # Logic to save to GSheet
            existing_data = conn.read(ttl=0)
            updated_df = pd.concat([existing_data, new_data], ignore_index=True)
            conn.update(data=updated_df)
            st.success("Tripping Request Submitted!")

# --- TAB 2: KEY REQUEST ---
with tab2:
    with st.form("key_form"):
        name = st.text_input("Staff Name")
        unit = st.text_input("Unit/Property Number")
        purpose = st.text_area("Purpose of Request")
        submit = st.form_submit_button("Submit Key Request")
        
        if submit and name:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Request_Type": "Key Request",
                "Requester_Name": name,
                "Details": f"Unit: {unit}, Purpose: {purpose}",
                "Status": "Pending"
            }])
            existing_data = conn.read(ttl=0)
            updated_df = pd.concat([existing_data, new_data], ignore_index=True)
            conn.update(data=updated_df)
            st.success("Key Request Submitted!")

# --- TAB 3: TRAINING REQUEST ---
with tab3:
    with st.form("training_form"):
        name = st.text_input("Requesting Dept/Person")
        topic = st.selectbox("Presentation/Topic", ["BD Presentation", "Project Overview", "Sales Training"])
        submit = st.form_submit_button("Submit Training Request")
        
        if submit and name:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Request_Type": "Training",
                "Requester_Name": name,
                "Details": f"Topic: {topic}",
                "Status": "Pending"
            }])
            existing_data = conn.read(ttl=0)
            updated_df = pd.concat([existing_data, new_data], ignore_index=True)
            conn.update(data=updated_df)
            st.success("Training Request Submitted!")

# --- MONITORING SECTION (ONLY FOR ADMIN) ---
if is_admin:
    st.divider()
    st.subheader("📊 Admin Monitoring Dashboard")
    data = conn.read(ttl=0)
    st.dataframe(data, use_container_width=True)
else:
    st.sidebar.info("Log in as Admin to see the Monitoring Dashboard.")