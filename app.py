 import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="VMSKY Singapore", page_icon="🙏", layout="centered")

# Sidebar Menu
menu = st.sidebar.selectbox("Menu", ["🏠 Home", "🔐 Member Login", "🧘 Daily Practice", "📅 Class Timings", "👥 Members Details", "📍 Contact Us"])
# ===== HOME PAGE =====
if menu == "🏠 Home":
    st.markdown("<h1 style='text-align: center; color: #FF9933; font-size: 26px; font-weight: bold; text-shadow: 1px 1px 2px #FFD700;'>Vazhga Vaiyagam Vazhga Valamudan 🙏</h1>", unsafe_allow_html=True)
    # Picture will now come - using your logo.png
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    elif os.path.exists("maharishi_final_logo.png"):
        st.image("maharishi_final_logo.png", use_container_width=True)
    
    st.markdown("<h3 style='text-align: center;'>VMSKY Singapore</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Vazhga Vaiyagam Vazhga Valamudan 🙏</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Foundation", "25+ Years")
    with col2:
        st.metric("Members", "250+")
    
    st.divider()
    
    # ===== CLASS TIMING - DOWN =====
    st.header("📅 VMSKY Singapore - Regular Class Timings")
    
    st.subheader("👩 Ladies Only Classes")
    st.write("Tuesday: 9:30 AM - 11:30 AM")
    st.write("Thursday: 9:30 AM - 11:30 AM")
    st.write("Saturday: 9:30 AM - 11:30 AM")
    
    st.subheader("👥 General Classes")
    st.write("Sunday: 7:00 AM - 09:00 AM : 06:00 PM- 08:00 PM")
    st.write("Sunday: 7:00 AM - 09:00 AM : 06:00 PM- 08:00 PM")
    st.write("Wednesday: 7:15 PM - 8:45 PM")
    
    st.subheader("⭐ Special Classes")
    st.write("Kayakalpa Yoga: Every 2nd Sunday 01:30 PM- 05:30 PM")
    st.write("Introspection: Every 3rd Sunday 09:00 AM- 05:30 PM")
    
    st.divider()
    
    # ===== ADDRESS + LINKS TOGETHER =====
    st.header("📍 Our Location & Contact")
    st.markdown("**Venue:** VMSKY TOC, 11,Woodlands close, #09-13 Singapore")
    
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("📲 WhatsApp 8057 2762", "https://wa.me/6580572762?text=Vazhga%20Valamudan%20I%20want%20to%20join%20VMSKY%20Singapore%20class")


# Also keep your short link as backup
st.caption("If app not open, [Click here](https://maps.app.goo.gl/mSMJu4YnH3gHghiV7)")
st.markdown("---")
st.markdown("📲 **WhatsApp:** [Chat +65 8057 2762](https://wa.me/6580572762)")
st.markdown("🗺️ **View on Map:** [Open Location]https://maps.app.goo.gl/mSMJu4YnH3gHghiV7")

elif menu == "Daily Practice":
    st.header("🧘 Daily Practice")
    st.write("Daily meditation and exercises...")

elif menu == "Class Timings":
    st.header("📅 Class Timings - Same as Home page")

elif menu == "Contact Us":
    st.header("📍 Contact Us")
    st.write("VMSKY TOC, 11,Woodlands close, #09-13 Singapore")
    st.link_button("📲 WhatsApp Us", "https://wa.me/6580572762?text=Vazhga%20Valamudan")
    st.link_button("🗺️ View on Map", "https://maps.app.goo.gl/mSMJu4YnH3gHghiV7")
