import streamlit as st
import os
import pandas as pd

st.set_page_config(page_title="VMSKY Singapore", layout="centered")

# ===== VENUE FINAL =====
VENUE_NAME = "VMSKY, Temple of Consciousness"
VENUE_ADDRESS = "11 Woodlands Cl, #09-13, Singapore 737853"
MAPS_DEST = "11+Woodlands+Cl+%2309-13+Singapore+737853"
MAPS_SHORT = "https://maps.app.goo.gl/CJu7kBmf3itpbQkN9"
WHATSAPP = "https://wa.me/6580572762"

menu = st.sidebar.selectbox("Menu", ["Home", "Member Login", "Class Timings", "Members Details", "Contact Us"])

def show_logo():
    for f in ["logo.png", "maharishi_final_logo.png", "maharishi_logo.png", "vmsky_logo.png"]:
        if os.path.exists(f):
            st.image(f, use_container_width=True)
            return

def show_map_buttons():
    st.link_button("🗺️ Open in Google Maps App", f"https://www.google.com/maps/search/?api=1&query={MAPS_DEST}")
    st.link_button("🧭 Get Directions", f"https://www.google.com/maps/dir/?api=1&destination={MAPS_DEST}")
    st.markdown(f"""
    <a href="comgooglemaps://?q={MAPS_DEST}" target="_blank" style="text-decoration:none;">
    <div style="background:#34A853; color:white; padding:12px; border-radius:10px; text-align:center; font-weight:bold; margin-top:8px;">
    📱 Open Direct in Maps App
    </div>
    </a>
    """, unsafe_allow_html=True)

# ===== CLASS TIMING FUNCTION - NEW FINAL TIMING =====
def show_class_timing():
    st.header("VMSKY Singapore - Regular Class Timings")
    
    st.subheader("👩 Ladies Class")
    st.write("Tuesday: 09:30 AM to 11:30 AM")
    st.write("Wednesday: 09:30 AM to 11:30 AM")
    st.write("Thursday: 09:30 AM to 11:30 AM")
    
    st.divider()
    st.subheader("👥 Common Class")
    st.write("Wednesday: 07:15 PM to 08:45 PM")
    
    st.write("**Saturday:**")
    st.write("Morning: 07:00 AM to 09:00 AM")
    st.write("Evening: 06:00 PM to 08:00 PM")
    
    st.write("**Sunday:**")
    st.write("Morning: 07:00 AM to 09:00 AM")
    st.write("Evening: 06:00 PM to 08:00 PM")
    
    st.divider()
    st.subheader("⭐ Special Class")
    st.write("**Kayakalpam Yoga:** Every Month 2nd Sunday 01:30 PM to 05:30 PM")
    st.write("**Introspection:** Every Month 3rd Sunday 09:00 AM to 05:30 PM")
    
    st.divider()

if menu == "Home":
    st.markdown("<h1 style='text-align:center; color:#FF8C00; font-size:22px;'>Vazhga Vaiyagam Vazhga Valamudan</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Vazhga Valamudan 🙏</p>", unsafe_allow_html=True)
    show_logo()
    st.divider()
    st.write(f"**{VENUE_NAME}**")
    st.write(VENUE_ADDRESS)
    st.link_button("WhatsApp 8057 2762", WHATSAPP)
    show_map_buttons()
    st.divider()
    show_class_timing()

elif menu == "Member Login":
    st.header("🔐 Member Login")
    show_logo()
    phone = st.text_input("Phone Number")
    password = st.text_input("Password", type="password")
    if st.button("Login", type="primary"):
        if not phone or not password:
            st.warning("Enter phone and password")
        else:
            try:
                sheet_url = st.secrets.get("SHEET_URL", "")
                if sheet_url:
                    df = pd.read_csv(sheet_url)
                    df['phone'] = df['phone'].astype(str).str.strip()
                    df['password'] = df['password'].astype(str).str.strip()
                    user = df[(df['phone'] == str(phone).strip()) & (df['password'] == str(password).strip())]
                    if not user.empty:
                        st.success(f"Vazhga Valamudan {user.iloc[0].get('name','Member')}! 🙏")
                        st.balloons()
                        st.dataframe(user.T)
                    else:
                        st.error("Invalid phone or password. Contact Admin 8057 2762")
                else:
                    if phone == "80572762" and password == "vmsky123":
                        st.success("Demo Login Success! Vazhga Valamudan 🙏")
                    else:
                        st.error("Demo: Phone 80572762 / Password vmsky123")
            except Exception as e:
                st.error(f"Login error: {e}")

elif menu == "Class Timings":
    show_logo()
    show_class_timing()
    st.write(VENUE_ADDRESS)
    show_map_buttons()

elif menu == "Members Details":
    st.header("👥 Members Details")
    show_logo()
    sheet_url = st.secrets.get("SHEET_URL", "")
    if sheet_url:
        try:
            df = pd.read_csv(sheet_url)
            st.success(f"Total Members: {len(df)}")
            st.dataframe(df, use_container_width=True)
            search = st.text_input("Search member")
            if search:
                filtered = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)]
                st.dataframe(filtered)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Google Sheet not connected yet")
        st.code('SHEET_URL = "https://docs.google.com/spreadsheets/d/xxx/pub?output=csv"')

elif menu == "Contact Us":
    show_logo()
    st.header("Contact Us")
    st.write(f"**{VENUE_NAME}**")
    st.write(VENUE_ADDRESS)
    st.write("Phone: +65 8057 2762")
    st.link_button("WhatsApp Us", WHATSAPP)
    show_map_buttons()
