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
            return

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
    st.write("Saturday: Morning 07:00 AM to 09:00 AM")
    st.write("Evening 06:00 PM to 08:00 PM")
    st.write("Sunday: Morning 07:00 AM to 09:00 AM")
    st.write("Evening 06:00 PM to 08:00 PM")
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
    st.write("Fill your details - Master will approve")
    with st.form("registration"):
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
                st.error("Please fill all * fields")
            elif password != confirm_pass:
                st.error("Passwords do not match!")
            else:
                new_member = {
                    "Name": name,
                    "Contact Number": contact,
                    "Email Address": email,
                    "DOB": str(dob),
                    "Address": address,
                    "Emergency Contact": emergency,
                    "Password": password,
                    "Level": "Exercise - Pending",
                    "Attendance %": "0%",
                    "Registration Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Status": "Pending"
                }
                st.session_state['new_registrations'].append(new_member)
                st.success(f"Vazhga Valamudan {name}! Registration Success")
                st.balloons()

    if st.session_state['new_registrations']:
        st.divider()
        df_new = pd.DataFrame(st.session_state['new_registrations'])
        st.dataframe(df_new, use_container_width=True)
        csv = df_new.to_csv(index=False).encode('utf-8')
        st.download_button("Download New Registrations", csv, f"new_members_{date.today()}.csv", "text/csv")

elif menu == "Change Password":
    st.header("Change Password")
    show_logo()
    user_type = st.radio("I am:", ["Member", "Master"])
    if user_type == "Member":
        st.subheader("Member Change Password")
        phone = st.text_input("Your Contact Number")
        old_pass = st.text_input("Old Password", type="password")
        new_pass = st.text_input("New Password", type="password")
        confirm_new = st.text_input("Confirm New Password", type="password")
        if st.button("Change Member Password", type="primary"):
            if not phone or not old_pass or not new_pass:
                st.error("Fill all fields")
            elif new_pass != confirm_new:
                st.error("New passwords do not match")
            else:
                df = load_members()
                if not df.empty:
                    st.session_state['password_changes'][phone] = new_pass
                    st.success(f"Password changed for {phone}")
                    st.warning("Master: Update Google Sheet manually")
                else:
                    st.session_state['password_changes'][phone] = new_pass
                    st.success("Demo: Password changed locally")
    else:
        st.subheader("Master Change Password")
        master_phone = st.text_input("Master Phone")
        old_master_pass = st.text_input("Old Master Password", type="password")
        new_master_pass = st.text_input("New Master Password", type="password")
        confirm_master_new = st.text_input("Confirm New Master Password", type="password")
        if st.button("Change Master Password", type="primary"):
            if master_phone == MASTER_PHONE and old_master_pass == MASTER_PASS:
                if new_master_pass != confirm_master_new:
                    st.error("Passwords do not match")
                else:
                    st.session_state['master_new_pass'] = new_master_pass
                    st.success("Master Password Changed!")
                    st.code(new_master_pass)
                    st.warning("Update in app.py MASTER_PASS")
            else:
                st.error("Invalid Master credentials")

elif menu == "Member Login":
    st.header("Member Login - Scan Master QR")
    show_logo()
    phone = st.text_input("Your Contact Number")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        df = load_members()
        if phone in st.session_state['password_changes']:
            if password == st.session_state['password_changes'][phone]:
                st.session_state['member_phone'] = phone
                st.session_state['member_name'] = "Member"
                st.success("Login Success with NEW password")
        elif not df.empty:
            phone_col = None
            for c in df.columns:
                if "contact" in c.lower() or "phone" in c.lower():
                    phone_col = c
                    break
            if phone_col:
                user = df[df[phone_col].astype(str).str.strip() == str(phone).strip()]
                if not user.empty:
                    st.session_state['member_phone'] = phone
                    st.session_state['member_name'] = "Member"
                    st.success("Vazhga Valamudan!")
        else:
            st.session_state['member_phone'] = phone if phone else "91234567"
            st.session_state['member_name'] = "Demo Member"
            st.success("Demo Login OK")

    if st.session_state.get('member_phone'):
        st.divider()
        st.subheader("Scan Master QR - Level LOCKED")
        master_qr_code = st.text_input("Enter Master QR Text", placeholder="VMSKY|DATE|LEVEL|...")
        if master_qr_code:
            parsed = parse_qr(master_qr_code)
            if parsed["valid"]:
                st.success(f"QR Valid! Class: {parsed['level']}")
                st.info(f"LOCKED CLASS: {parsed['level']} - ONLY this class")
                if st.button(f"Confirm for {parsed['level']}"):
                    if 'attendance_log' not in st.session_state:
                        st.session_state['attendance_log'] = []
                    entry = {
                        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Contact Number": st.session_state['member_phone'],
                        "Name": st.session_state['member_name'],
                        "Level": parsed['level'],
                        "Type": "Member"
                    }
                    st.session_state['attendance_log'].append(entry)
                    st.success(f"Attendance for {parsed['level']} ONLY!")
                    st.balloons()
            else:
                st.error("Invalid QR")

elif menu == "Master Login":
    st.header("Master Login - Full Control")
    show_logo()
    m_phone = st.text_input("Master Phone")
    m_pass = st.text_input("Master Password", type="password")
    master_current_pass = st.session_state.get('master_new_pass', MASTER_PASS)
    if st.button("Master Login"):
        if m_phone == MASTER_PHONE and m_pass == master_current_pass:
            st.session_state['master'] = True
            st.session_state['master_phone'] = m_phone
            st.success("Master Login Success!")
        else:
            st.error("Invalid")

    if st.session_state.get('master'):
        st.divider()
        tab1, tab2, tab3 = st.tabs(["Generate QR", "Change Level", "New Registrations"])
        with tab1:
            st.subheader("Generate LOCKED QR")
            today = date.today().strftime("%Y-%m-%d")
            locked_level = st.selectbox("LOCK Class Type", 
                ["Exercise", "Kayakalpam", "Agnai", "Santhi", "Thanduvadasuthi", "Thuriyam", 
                 "Introspection 1", "Introspection 2", "Introspection 3", "Bramaganam", "Arulnithi"])
            timestamp = datetime.now().strftime("%H%M%S")
            qr_data = f"VMSKY|{today}|{locked_level}|{st.session_state.get('master_phone', MASTER_PHONE)}|{timestamp}"
            st.write(f"QR: {qr_data}")
            qr_image = generate_qr(qr_data)
            st.image(qr_image, caption=f"LOCKED QR: {locked_level}", width=320)
        with tab2:
            st.subheader("Change Member Level - ONLY Master")
            member_phone_to_change = st.text_input("Member Contact Number")
            new_level = st.selectbox("New Level", 
                ["Exercise", "Kayakalpam", "Agnai", "Santhi", "Thanduvadasuthi", "Thuriyam", 
                 "Introspection 1", "Introspection 2", "Introspection 3", "Bramaganam", "Arulnithi", "Master"])
            if st.button("Update Level"):
                if member_phone_to_change:
                    if 'level_changes' not in st.session_state:
                        st.session_state['level_changes'] = {}
                    st.session_state['level_changes'][member_phone_to_change] = new_level
                    st.success(f"Level changed for {member_phone_to_change} to {new_level}")
        with tab3:
            st.subheader("New Registrations")
            if st.session_state['new_registrations']:
                df_new = pd.DataFrame(st.session_state['new_registrations'])
                st.dataframe(df_new, use_container_width=True)
                csv = df_new.to_csv(index=False).encode('utf-8')
                st.download_button("Download", csv, f"new_members_{date.today()}.csv", "text/csv")
            else:
                st.info("No new registrations")

elif menu == "Class Timings":
    show_logo()
    show_class_timing()
    show_map_buttons()

elif menu == "Members Details":
    st.header("Members Details")
    show_logo()
    df = load_members()
    all_data = []
    if not df.empty:
        all_data.append(df)
    if st.session_state['new_registrations']:
        all_data.append(pd.DataFrame(st.session_state['new_registrations']))
    if all_data:
        combined = pd.concat(all_data, ignore_index=True) if len(all_data) > 1 else all_data[0]
        st.success(f"Total Members: {len(combined)}")
        search = st.text_input("Search by Name or Contact")
        if search:
           
