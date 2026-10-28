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

def whatsapp_button():
    st.link_button("Chat on WhatsApp - 80572762", WHATSAPP)

def map_buttons():
    st.link_button("Open in Google Maps App", f"https://www.google.com/maps/search/?api=1&query={MAPS_DEST}")
    st.link_button("Get Directions", f"https://www.google.com/maps/dir/?api=1&destination={MAPS_DEST}")

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
            result = {}
            result["date"] = parts[1]
            result["level"] = parts[2]
            result["master_phone"] = parts[3]
            result["valid"] = True
            return result
    except:
        pass
    result2 = {}
    result2["valid"] = False
    return result2

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

if 'new_registrations' not in st.session_state:
    st.session_state['new_registrations'] = []
if 'password_changes' not in st.session_state:
    st.session_state['password_changes'] = {}
if 'attendance_log' not in st.session_state:
    st.session_state['attendance_log'] = []
if 'level_changes' not in st.session_state:
    st.session_state['level_changes'] = {}

# ===== HOME - FIXED WHATSAPP =====
if menu == "Home":
    st.markdown("<h1 style='text-align:center; color:#FF8C00; font-size:22px;'>Vazhga Vaiyagam Vazhga Valamudan</h1>", unsafe_allow_html=True)
    show_logo()
    st.write(VENUE_NAME)
    st.write(VENUE_ADDRESS)
    st.divider()
    st.subheader("Contact Us on WhatsApp")
    whatsapp_button()
    st.divider()
    st.subheader("Location")
    map_buttons()
    st.divider()
    show_class_timing()

# ===== NEW REGISTRATION - FIXED SUBMIT =====
elif menu == "New Registration":
    st.header("New Member Registration")
    show_logo()
    st.write("Fill all details - Master will approve")
    st.divider()
    
    name = st.text_input("Full Name *", key="reg_name")
    contact = st.text_input("Mobile Number *", key="reg_contact")
    email = st.text_input("Email Address *", key="reg_email")
    dob = st.date_input("Date of Birth", value=date(1990, 1, 1), key="reg_dob")
    address = st.text_area("Address", key="reg_address")
    emergency = st.text_input("Emergency Contact", key="reg_emer")
    password = st.text_input("Create Password *", type="password", key="reg_pass")
    confirm_pass = st.text_input("Confirm Password *", type="password", key="reg_cpass")
    how_know = st.selectbox("How did you know?", ["Friend", "Facebook", "WhatsApp", "Temple", "Others"], key="reg_how")
    
    if st.button("Register Now", type="primary"):
        if not name or not contact or not email or not password:
            st.error("Please fill all * fields")
        elif password != confirm_pass:
            st.error("Passwords do not match!")
        elif len(contact) < 8:
            st.error("Enter valid mobile number")
        else:
            new_member = {}
            new_member["Name"] = name
            new_member["Contact Number"] = contact
            new_member["Email Address"] = email
            new_member["DOB"] = str(dob)
            new_member["Address"] = address
            new_member["Emergency Contact"] = emergency
            new_member["Password"] = password
            new_member["Level"] = "Exercise - Pending"
            new_member["Registration Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_member["Status"] = "Pending"
            st.session_state['new_registrations'].append(new_member)
            st.success(f"Vazhga Valamudan {name}! Registration Success! Please go to Member Login")
            st.balloons()
    
    st.divider()
    if st.session_state['new_registrations']:
        st.subheader("Your Registrations - Download for Master")
        df_new = pd.DataFrame(st.session_state['new_registrations'])
        st.dataframe(df_new, use_container_width=True)
        csv = df_new.to_csv(index=False).encode('utf-8')
        st.download_button("Download New Registrations", csv, f"new_members_{date.today()}.csv", "text/csv")
    else:
        st.info("No registrations yet - Fill above form and click Register Now")

# ===== MEMBER LOGIN - FIXED EMPTY =====
elif menu == "Member Login":
    st.header("Member Login")
    show_logo()
    st.write("Login and Scan Master QR - Level LOCKED by Master")
    st.divider()
    
    phone = st.text_input("Your Contact Number", key="mem_phone")
    password = st.text_input("Password", type="password", key="mem_pass")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login", type="primary"):
            st.session_state['member_phone'] = phone
            st.session_state['member_name'] = phone
            st.success(f"Login Success! Phone: {phone}")
            st.rerun()
    with col2:
        if st.button("Logout"):
            st.session_state['member_phone'] = ""
            st.session_state['member_name'] = ""
            st.info("Logged out")
    
    if st.session_state.get('member_phone'):
        st.divider()
        st.subheader("Scan Master QR - Level LOCKED")
        st.write("Ask Master to
