import streamlit as st
import os
import pandas as pd
from datetime import datetime, date
import qrcode
import io

st.set_page_config(page_title="VMSKY Singapore", layout="centered")

VENUE_NAME = "VMSKY Temple"
VENUE_ADDRESS = "11 Woodlands Cl Singapore"
MAPS_DEST = "11+Woodlands+Cl+Singapore"
WHATSAPP = "https://wa.me/6580572762"
MASTER_PHONE = "80572762"
MASTER_PASS = "master123"

menu = st.sidebar.selectbox("Menu", ["Home", "Member Login", "New Registration", "Change Password", "Master Login", "Class Timings", "Members Details", "Attendance", "Contact Us"])

def show_logo():
    for f in ["logo.png", "maharishi_final_logo.png"]:
        if os.path.exists(f):
            st.image(f, use_container_width=True)

def whatsapp_button():
    st.link_button("Chat on WhatsApp", WHATSAPP)

def map_buttons():
    st.link_button("Open Maps", "https://www.google.com/maps/search/?api=1&query=" + MAPS_DEST)

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
    st.divider()
    whatsapp_button()
    st.divider()
    map_buttons()
    st.divider()
    st.write("Ladies Tue Wed Thu 09:30-11:
