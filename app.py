import streamlit as st
import os
import pandas as pd
from datetime import datetime, date
import qrcode
import io

st.set_page_config(page_title="VMSKY Singapore", layout="centered")

VENUE_NAME = "VMSKY Temple"
VENUE_ADDRESS = "11 Woodlands Cl #09-13 Singapore 737853"
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
    st.link_button("Chat on WhatsApp", WHATSAPP)

def map_buttons():
    st.link_button("Open Google Maps", f"https://www.google.com/maps/search/?api=1&query={MAPS_DEST}")

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

def show_class_timing():
    st.header("Class Timings")
    st.write("Ladies: Tue Wed Thu 09:30-11:30")
    st.write("Common: Wed 19:15-20:45")
    st.write("Sat Sun 07:00-09:00 and 18:00-20:00")
    st.write("Kayakalpam: 2nd Sun 13:30-17:30")
    st.write("Introspection: 3rd Sun 09:00-17:30")

@st.cache_data(tt
