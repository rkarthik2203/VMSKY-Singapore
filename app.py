import streamlit as st
import os
import pandas as pd
from datetime import datetime, date

st.set_page_config(page_title="VMSKY Singapore", layout="centered")

VENUE_NAME = "VMSKY, Temple of Consciousness"
VENUE_ADDRESS = "11 Woodlands Cl, #09-13, Singapore 737853"
MAPS_DEST = "11+Woodlands+Cl+%2309-13+Singapore+737853"
WHATSAPP = "https://wa.me/6580572762"

MASTER_PHONE = "80572762"
MASTER_PASS = "master123"

menu = st.sidebar.selectbox("Menu", ["Home", "Member Login", "Master Login", "Class Timings", "Members Details", "Attendance", "Contact Us"])

def show_logo():
    for f in ["logo.png", "maharishi_final_logo.png", "maharishi_logo.png"]:
        if os.path.exists(f):
            st.image(f, use_container_width=True)
            return

def show_map_buttons():
    st.link_button("Open in Google Maps App", f"https://www.google.com/maps/search/?api=1&query={MAPS_DEST}")
    st.link_button("Get Directions", f"https://www.google.com/maps/dir/?api=1&destination={MAPS_DEST}")

def show_class_timing():
    st.header("VMSKY Singapore - Regular Class Timings")
    st.subheader("Ladies Class")
    st.write("Tuesday: 09:30 AM to 11:30 AM")
    st.write("Wednesday: 09:30 AM to 11:30 AM")
    st.write("Thursday: 09:30 AM to 11:30 AM")
    st.divider()
    st.subheader("Common Class")
    st.write("Wednesday: 07:15 PM to 08:45 PM")
    st.write("Saturday: Morning 07:00 AM to 09:00 AM | Evening 06:00 PM to 08:00 PM")
    st.write("Sunday: Morning 07:00 AM to 09:00 AM | Evening 06:00 PM to 08:00 PM")
    st.divider()
    st.subheader("Special Class")
    st.write("Kayakalpam Yoga: Every Month 2nd Sunday 01:30 PM to 05:30 PM")
    st.write("Introspection: Every Month 3rd Sunday 09:00 AM to 05:30 PM")

@st.cache_data(ttl=60)
def load_members():
    sheet_url = st.secrets.get("SHEET_URL", "")
    if sheet_url:
        try:
            df = pd.read_csv(sheet_url)
            return df
        except:
            return pd.DataFrame()
    return pd.DataFrame()

if menu == "Home":
    st.markdown("<h1 style='text-align:center; color:#FF8C00; font-size:20px;'>Vazhga Vaiyagam Vazhga Valamudan</h1>", unsafe_allow_html=True)
    show_logo()
    st.write(VENUE_NAME)
    st.write(VENUE_ADDRESS)
    show_map_buttons()
    st.divider()
    show_class_timing()

elif menu == "Member Login":
    st.header("Member Login")
    show_logo()
    phone = st.text_input("Contact Number")
    password = st.text_input("Password", type="password")
    if st.button("Login", type="primary"):
        df = load_members()
        if not df.empty:
            phone_col = None
            for c in df.columns:
                if "contact" in c.lower() or "phone" in c.lower():
                    phone_col = c
                    break
            if phone_col:
                user = df[df[phone_col].astype(str).str.strip() == str(phone).strip()]
                if not user.empty:
                    st.success(f"Vazhga Valamudan {user.iloc[0].get('Name', 'Member')}!")
                    st.balloons()
                    st.dataframe(user.T)
                else:
                    st.error("Member not found")
            else:
                st.error("Contact column not found in sheet")
        else:
            st.warning("Add SHEET_URL in Secrets. Demo: 80572762 / master123")

elif menu == "Master Login":
    st.header("Master Login")
    show_logo()
    m_phone = st.text_input("Master Phone")
    m_pass = st.text_input("Master Password", type="password")
    if st.button("Master Login"):
        if m_phone == MASTER_PHONE and m_pass == MASTER_PASS:
            st.session_state['master'] = True
            st.success("Master Login Success")
        else:
            st.error("Invalid Master login. Use 80572762 / master123")

    if st.session_state.get('master'):
        st.divider()
        st.subheader("Mark Attendance")
        df = load_members()
        contact_num = st.text_input("Enter Member Contact Number")
        level_today = st.selectbox("Today Level", 
            ["Exercise", "Kayakalpam", "Agnai", "Santhi", "Thanduvadasuthi", "Thuriyam", 
             "Introspection 1", "Introspection 2", "Introspection 3", "Bramaganam", "Arulnithi"])
        
        if st.button("Confirm Attendance"):
            if contact_num:
                if 'attendance_log' not in st.session_state:
                    st.session_state['attendance_log'] = []
                entry = {
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Contact Number": contact_num,
                    "Level": level_today,
                    "Confirmed By": "Master"
                }
                st.session_state['attendance_log'].append(entry)
                st.success(f"Attendance Confirmed for {contact_num}")
                st.balloons()
        
        if st.session_state.get('attendance_log'):
            log_df = pd.DataFrame(st.session_state['attendance_log'])
            st.dataframe(log_df, use_container_width=True)
            csv = log_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Attendance CSV", csv, f"attendance_{date.today()}.csv", "text/csv")

elif menu == "Class Timings":
    show_logo()
   
