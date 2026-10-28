import streamlit as st
import os
import pandas as pd

st.set_page_config(page_title="VMSKY Singapore", layout="centered")

VENUE_NAME = "VMSKY, Temple of Consciousness"
VENUE_ADDRESS = "11 Woodlands Cl, #09-13, Singapore 737853"
MAPS_DEST = "11+Woodlands+Cl+%2309-13+Singapore+737853"
MAPS_SHORT = "https://maps.app.goo.gl/CJu7kBmf3itpbQkN9"

menu = st.sidebar.selectbox("Menu", ["Home", "Member Login", "Class Timings", "Contact Us"])

def show_logo():
    for f in ["logo.png", "maharishi_final_logo.png"]:
        if os.path.exists(f):
            st.image(f, use_container_width=True)
            return

if menu == "Home":
    st.markdown("<h1 style='text-align:center; color:#FF8C00; font-size:22px;'>Vazhga Vaiyagam Vazhga Valamudan</h1>", unsafe_allow_html=True)
    show_logo()
    st.write(VENUE_ADDRESS)
    st.link_button("WhatsApp 8057 2762", "https://wa.me/6580572762")

    # ===== THIS IS THE FIX - MAP APP OPENS DIRECT =====
    st.divider()
    st.subheader("📍 Location")
    st.write(VENUE_NAME)
    st.write(VENUE_ADDRESS)
    st.link_button("🗺️ Open in Google Maps App", f"https://www.google.com/maps/search/?api=1&query={MAPS_DEST}")
    st.link_button("🧭 Get Directions", f"https://www.google.com/maps/dir/?api=1&destination={MAPS_DEST}")
    
    st.markdown(f"""
    <a href="comgooglemaps://?q={MAPS_DEST}" target="_blank">
    <div style="background:#34A853; color:white; padding:12px; border-radius:10px; text-align:center; font-weight:bold;">
    📱 Open Direct in Maps App
    </div>
    </a>
    """, unsafe_allow_html=True)

    st.divider()
    st.header("VMSKY Singapore - Regular Class Timings")
    st.subheader("Ladies Only Classes")
    st.write("Tuesday: 9:30 AM - 11:30 AM")
    st.write("Wednesday: 9:30 AM - 11:30 AM")
    st.write("Thursday: 9:30 AM - 11:30 AM")
    st.subheader("General Classes")
    st.write("Sunday: 7:00 AM - 09:00 AM : 06:00 PM - 08:00 PM")
    st.write("Wednesday: 7:15 PM - 8:45 PM")
    st.subheader("Special Classes")
    st.write("Kayakalpa Yoga: Every 2nd Sunday 01:30 PM - 05:30 PM")
    st.write("Introspection: Every 3rd Sunday 09:00 AM - 05:30 PM")

elif menu == "Member Login":
    st.header("Member Login")
    show_logo()
    phone = st.text_input("Phone")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        st.success("Login ok - Vazhga Valamudan 🙏")

elif menu == "Class Timings":
    show_logo()
    st.header("VMSKY Singapore - Regular Class Timings")
    st.subheader("Ladies Only Classes")
    st.write("Tuesday: 9:30 AM - 11:30 AM")
    st.write("Wednesday: 9:30 AM - 11:30 AM")
    st.write("Thursday: 9:30 AM - 11:30 AM")
    st.subheader("General Classes")
    st.write("Sunday: 7:00 AM - 09:00 AM : 06:00 PM - 08:00 PM")
    st.write("Wednesday: 7:15 PM - 8:45 PM")
    st.subheader("Special Classes")
    st.write("Kayakalpa Yoga: Every 2nd Sunday 01:30 PM - 05:30 PM")
    st.write("Introspection: Every 3rd Sunday 09:00 AM - 05:30 PM")
    st.divider()
    st.link_button("🗺️ Open in Maps App", f"https://www.google.com/maps/search/?api=1&query={MAPS_DEST}")

elif menu == "Contact Us":
    show_logo()
    st.header("Contact Us")
    st.write(VENUE_NAME)
    st.write(VENUE_ADDRESS)
    st.link_button("🗺️ Open in Google Maps App", f"https://www.google.com/maps/search/?api=1&query={MAPS_DEST}")
    st.link_button("🧭 Get Directions", f"https://www.google.com/maps/dir/?api=1&destination={MAPS_DEST}")
