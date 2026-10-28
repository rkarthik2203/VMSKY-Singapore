import streamlit as st
import os
import pandas as pd
from datetime import datetime, date
import qrcode
import io

st.set_page_config(page_title="VMSKY Singapore", layout="centered")

VENUE_NAME = "VMSKY Temple"
VENUE_ADDRESS = "11 Woodlands Singapore"
MAPS_DEST = "11 Woodlands Singapore"
WHATSAPP = "https://wa.me/6580572762"
MASTER_PHONE = "80572762"
MASTER_PASS = "master123"

menu = st.sidebar.selectbox("Menu", ["Home", "Member Login", "New Registration", "Change Password", "Master Login", "Class Timings", "Members Details", "Attendance", "Contact Us"])

def show_logo():
    for f in ["logo.png", "maharishi_final_logo.png"]:
        if os.path.exists(f):
            st.image(f, use_container_width=True)

def whatsapp_button():
    st.link_button("WhatsApp", WHATSAPP)

def map_buttons():
    st.link_button("Maps", "https://maps.google.com")

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
            r = {}
            r["date"] = parts[1]
            r["level"] = parts[2]
            r["master_phone"] = parts[3]
            r["valid"] = True
            return r
    except:
        pass
    r2 = {}
    r2["valid"] = False
    return r2

def load_members():
    url = st.secrets.get("SHEET_URL", "")
    if url:
        try:
            df = pd.read_csv(url)
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
    st.title("Vazhga Vaiyagam")
    show_logo()
    st.write(VENUE_NAME)
    st.write(VENUE_ADDRESS)
    whatsapp_button()
    map_buttons()
    st.write("Ladies Class")
    st.write("Tue Wed Thu")
    st.write("Common Class")
    st.write("Wed Sat Sun")

elif menu == "New Registration":
    st.header("New Registration")
    show_logo()
    name = st.text_input("Full Name")
    contact = st.text_input("Mobile Number")
    email = st.text_input("Email")
    dob = st.date_input("DOB", value=date(1990, 1, 1))
    address = st.text_area("Address")
    emergency = st.text_input("Emergency Contact")
    pwd = st.text_input("Create Password", type="password")
    cpwd = st.text_input("Confirm Password", type="password")
    if st.button("Register Now", type="primary"):
        if not name or not contact or not email or not pwd:
            st.error("Fill all")
        elif pwd != cpwd:
            st.error("No match")
        else:
            m = {}
            m["Name"] = name
            m["Contact"] = contact
            m["Email"] = email
            m["DOB"] = str(dob)
            m["Address"] = address
            m["Emergency"] = emergency
            m["Password"] = pwd
            m["Level"] = "Exercise Pending"
            m["Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state['new_registrations'].append(m)
            st.success("Registration Success")
            st.balloons()
    if st.session_state['new_registrations']:
        df_new = pd.DataFrame(st.session_state['new_registrations'])
        st.dataframe(df_new, use_container_width=True)

elif menu == "Member Login":
    st.header("Member Login")
    show_logo()
    phone = st.text_input("Contact Number")
    pwd = st.text_input("Password", type="password")
    if st.button("Login", type="primary"):
        st.session_state['member_phone'] = phone
        st.session_state['member_name'] = phone
        st.success("Login OK")
    if st.button("Logout"):
        st.session_state['member_phone'] = ""
    if st.session_state.get('member_phone'):
        st.subheader("Scan Master QR")
        qr_text = st.text_input("Enter Master QR")
        if qr_text:
            parsed = parse_qr(qr_text)
            if parsed["valid"]:
                st.success("QR Valid")
                st.write(parsed["level"])
                if st.button("Confirm Attendance", type="primary"):
                    e = {}
                    e["Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    e["Contact"] = st.session_state['member_phone']
                    e["Level"] = parsed["level"]
                    e["Type"] = "Member"
                    st.session_state['attendance_log'].append(e)
                    st.success("Attendance Confirmed")
                    st.balloons()
            else:
                st.error("Invalid QR")

elif menu == "Change Password":
    st.header("Change Password")
    show_logo()
    utype = st.radio("I am", ["Member", "Master"])
    if utype == "Member":
        phone = st.text_input("Contact")
        new = st.text_input("New Password", type="password")
        cnew = st.text_input("Confirm New", type="password")
        if st.button("Change Member Password", type="primary"):
            if new != cnew:
                st.error("No match")
            else:
                st.session_state['password_changes'][phone] = new
                st.success("Password changed")
    else:
        mph = st.text_input("Master Phone")
        om = st.text_input("Old Master Pass", type="password")
        nm = st.text_input("New Master Pass", type="password")
        cnm = st.text_input("Confirm New Master", type="password")
        if st.button("Change Master Password", type="primary"):
            if mph == MASTER_PHONE and om == MASTER_PASS:
                if nm != cnm:
                    st.error("No match")
                else:
                    st.session_state['master_new_pass'] = nm
                    st.success("Master Pass Changed")
                    st.code(nm)
            else:
                st.error("Invalid")

elif menu == "Master Login":
    st.header("Master Login")
    show_logo()
    mph = st.text_input("Master Phone")
    mpass = st.text_input("Master Password", type="password")
    cur = st.session_state.get('master_new_pass', MASTER_PASS)
    if st.button("Master Login", type="primary"):
        if mph == MASTER_PHONE and mpass == cur:
            st.session_state['master'] = True
            st.session_state['master_phone'] = mph
            st.success("Master Login OK")
        else:
            st.error("Invalid")
    if st.session_state.get('master'):
        t1, t2, t3 = st.tabs(["Generate QR", "Change Level", "New Reg"])
        with t1:
            today = date.today().strftime("%Y-%m-%d")
            lvl = st.selectbox("Lock Level", ["Exercise", "Kayakalpam", "Agnai", "Santhi", "Thanduvadasuthi", "Thuriyam", "Introspection 1", "Introspection 2", "Introspection 3", "Bramaganam", "Arulnithi"])
            ts = datetime.now().strftime("%H%M%S")
            mp = st.session_state.get('master_phone', MASTER_PHONE)
            qd = "VMSKY|" + today + "|" + lvl + "|" + mp + "|" + ts
            st.code(qd)
            img = generate_qr(qd)
            st.image(img, width=320)
        with t2:
            ph = st.text_input("Member Phone")
            nl = st.selectbox("New Level", ["Exercise", "Kayakalpam", "Agnai", "Santhi", "Thanduvadasuthi", "Thuriyam", "Introspection 1", "Introspection 2", "Introspection 3", "Bramaganam", "Arulnithi", "Master"])
            if st.button("Update Level"):
                if ph:
                    st.session_state['level_changes'][ph] = nl
                    st.success("Level changed")
        with t3:
            if st.session_state['new_registrations']:
                dfn = pd.DataFrame(st.session_state['new_registrations'])
                st.dataframe(dfn, use_container_width=True)
            else:
                st.info("No new reg")

elif menu == "Class Timings":
    show_logo()
    st.header("Class Timings")
    st.write("Ladies Class Tue Wed Thu")
    st.write("Common Wed Sat Sun")
    st.write("Kayakalpam 2nd Sunday")
    st.write("Introspection 3rd Sunday")
    whatsapp_button()
    map_buttons()

elif menu == "Members Details":
    st.header("Members Details")
    show_logo()
    df = load_members()
    alld = []
    if not df.empty:
        alld.append(df)
    if st.session_state['new_registrations']:
        alld.append(pd.DataFrame(st.session_state['new_registrations']))
    if alld:
        if len(alld) > 1:
            comb = pd.concat(alld, ignore_index=True)
        else:
            comb = alld[0]
        st.write("Total Members")
        st.write(len(comb))
        st.dataframe(comb, use_container_width=True)
    else:
        st.warning("No members yet")

elif menu == "Attendance":
    st.header("Attendance")
    show_logo()
    if st.session_state['attendance_log']:
        df = pd.DataFrame(st.session_state['attendance_log'])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No attendance today")
        whatsapp_button()

elif menu == "Contact Us":
    show_logo()
    st.header("Contact Us")
    st.write(VENUE_NAME)
    st.write(VENUE_ADDRESS)
    whatsapp_button()
    st.write("Phone 80572762")
    map_buttons()
