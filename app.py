import streamlit as st
import os
import pandas as pd
from datetime import datetime, date
import qrcode
import io

st.set_page_config(page_title="VMSKY Singapore", layout="centered")

VENUE_NAME = "VMSKY, Temple of Consciousness"
VENUE_ADDRESS = "11 Woodlands Cl, #09-13, Singapore 737853"
MAPS_DEST = "11+Woodlands+Cl+%2309-13+Singapore+737853"
WHATSAPP = "https://wa.me/6580572762"
MASTER_PHONE = "80572762"
MASTER_PASS = "master123"

menu = st.sidebar.selectbox("Menu", ["Home", "Member Login", "New Registration", "Change Password", "Master Login", "Class Timings", "Members Details", "Attendance", "Contact Us"])

def show_logo():
    for f in ["logo.png", "maharishi_final_logo.png"]:
        if os.path.exists(f):
            st.image(f, use_container_width=True)

def show_map_buttons():
    st.link_button("Open in Google Maps App", f"https://www.google.com/maps/search/?api=1&query={MAPS_DEST}")

def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

def parse_qr(qr_text):
    try:
        parts = qr_text.split("|")
        if len(parts) >= 4 and parts[0] == "VMSKY":
            return {"date": parts[1], "level": parts[2], "master_phone": parts[3], "valid": True}
    except:
        pass
    return {"valid": False}

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
    st.write("Kayakalpam Yoga: 2nd Sunday 01:30 PM to 05:30 PM")
    st.write("Introspection: 3rd Sunday 09:00 AM to 05:30 PM")

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

if 'new_registrations' not in st.session_state:
    st.session_state['new_registrations'] = []
if 'password_changes' not in st.session_state:
    st.session_state['password_changes'] = {}
if 'attendance_log' not in st.session_state:
    st.session_state['attendance_log'] = []
if 'level_changes' not in st.session_state:
    st.session_state['level_changes'] = {}

if menu == "Home":
    st.markdown("<h1 style='text-align:center; color:#FF8C00; font-size:20px;'>Vazhga Vaiyagam Vazhga Valamudan</h1>", unsafe_allow_html=True)
    show_logo()
    st.write(VENUE_NAME)
    st.write(VENUE_ADDRESS)
    show_map_buttons()
    st.divider()
    show_class_timing()

elif menu == "New Registration":
    st.header("New Member Registration")
    show_logo()
    with st.form("reg_form"):
        name = st.text_input("Full Name *")
        contact = st.text_input("Mobile Number *")
        email = st.text_input("Email Address *")
        dob = st.date_input("Date of Birth", value=date(1990, 1, 1))
        address = st.text_area("Address")
        emergency = st.text_input("Emergency Contact")
        password = st.text_input("Create Password *", type="password")
        confirm_pass = st.text_input("Confirm Password *", type="password")
        how_know = st.selectbox("How did you know?", ["Friend", "Facebook", "WhatsApp", "Temple", "Others"])
        submit = st.form_submit_button("Register Now", type="primary")
        if submit:
            if not name or not contact or not email or not password:
                st.error("Fill all * fields")
            elif password != confirm_pass:
                st.error("Passwords do not match")
            else:
                new_member = {
                    "Name": name,
                    "Contact Number": contact,
                    "Email Address": email,
                    "DOB": str(dob),
                    "Address":
