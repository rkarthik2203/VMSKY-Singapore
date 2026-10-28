import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="VMSKY Singapore", page_icon="🙏", layout="centered")

# Sidebar Menu
menu = st.sidebar.selectbox("Menu", ["🏠 Home", "🧘 Daily Practice", "📅 Class Timings", "📍 Contact Us"])

# ===== HOME PAGE =====
if menu == "🏠 Home":
    st.title("Vazhga Vaiyagam Vazhga Valamudan")
    
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
    st.write("Tuesday: 7:00 PM - 8:30 PM")
    st.write("Thursday: 7:00 PM - 8:30 PM")
    st.write("Saturday: 4:00 PM - 5:30 PM")
    
    st.subheader("👥 General Classes")
    st.write("Sunday: 9:00 AM - 10:30 AM")
    st.write("Wednesday: 7:00 PM - 8:30 PM")
    st.write("Friday: 7:00 PM - 8:30 PM")
    
    st.subheader("⭐ Special Classes")
    st.write("Kayakalpa Yoga: Every 2nd Saturday")
    st.write("Introspection: Last Sunday")
    
    st.divider()
    
    # ===== ADDRESS + LINKS TOGETHER =====
    st.header("📍 Our Location & Contact")
    st.markdown("**Venue:** VMSKY TOC, 11,Woodlands close, #09-13 Singapore")
    
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("📲 WhatsApp 8057 2762", "https://wa.me/6580572762?text=Vazhga%20Valamudan%20I%20want%20to%20join%20VMSKY%20Singapore%20class")
    with col2:
        st.link_button("🗺️ Get Directions", "https://maps.app.goo.gl/mSMJu4YnH3gHghiV7")
    
    st.markdown("---")
    st.markdown("📲 **WhatsApp:** [Chat +65 8057 2762](https://wa.me/6580572762)")
    st.markdown("🗺️ **Maps:** [Open Location](https://maps.app.goo.gl/mSMJu4YnH3gHghiV7)")

elif menu == "🧘 Daily Practice":
    st.header("🧘 Daily Practice")
    st.write("Daily meditation and exercises...")

elif menu == "📅 Class Timings":
    st.header("📅 Class Timings - Same as Home page")

elif menu == "📍 Contact Us":
    st.header("📍 Contact Us")
    st.write("VMSKY TOC, 11,Woodlands close, #09-13 Singapore")
    st.link_button("📲 WhatsApp Us", "https://wa.me/6580572762?text=Vazhga%20Valamudan")
    st.link_button("🗺️ View on Map", "https://maps.app.goo.gl/mSMJu4YnH3gHghiV7")
