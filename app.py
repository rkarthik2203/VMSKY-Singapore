import streamlit as st
import os
import pandas as pd

st.set_page_config(page_title="VMSKY Singapore", layout="centered")

# ===== CORRECT ADDRESS =====
VENUE_NAME = "VMSKY Trust"
VENUE_ADDRESS = "11 Woodlands Cl, #09-13, Singapore 737853"
MAPS_DEST = "11+Woodlands+Cl+%2309-13+Singapore+737853"
WHATSAPP_LINK = "https://wa.me/6580572762?text=Vazhga%20Valamudan%20I%20want%20to%20join%20VMSKY%20Singapore"

menu = st.sidebar.selectbox("Menu", ["Home", "Member Login", "Class Timings", "Contact Us"])

# ===== FUNCTION TO SHOW LOGO =====
def show_logo():
    logo_files = ["logo.png", "maharishi_final_logo.png", "maharishi_logo.png", "vmsky_logo.png"]
    for f in logo_files:
        if os.path.exists(f):
            st.image(f, use_container_width=True)
            return
    # If no logo file, show text logo
    st.markdown("<h2 style='text-align:center;'>🙏 VMSKY Singapore 🙏</h2>", unsafe_allow_html=True)

if menu == "Home":
    st.markdown("<h1 style='text-align:center; color:#FF8C00; font-size:22px;'>Vazhga Vaiyagam Vazhga Valamudan</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Vazhga Valamudan 🙏</p>", unsafe_allow_html=True)

    show_logo()

    st.divider()
    st.write(f"**{VENUE_NAME}**")
    st.write(VENUE_ADDRESS)

    col1, col2 = st.columns(2)
    with col1:
        st.link_button("WhatsApp 8057 2762", WHATSAPP_LINK)
    with col2:
        st.link_button("Open Maps App", f"https://www.google.com/maps/dir/?api=1&destination={MAPS_DEST}")

    st.markdown(f"""
    <a href="https://www.google.com/maps/dir/?api=1&destination={MAPS_DEST}" target="_blank" style="text-decoration:none;">
    <div style="background:#4285F4; color:white; padding:12px; border-radius:10px; text-align:center; font-weight:bold; margin-top:10px;">
    🗺️ Open in Google Maps App
    </div>
    </a>
    """, unsafe_allow_html=True)

    # ===== CLASS TIMING - DOWN =====
    st.divider()
    st.header("VMSKY Singapore - Regular Class Timings")
    
    st.subheader("Ladies Only Classes")
    st.write("Tuesday: 9:30 AM - 11:30 AM")
    st.write("Thursday: 9:30 AM - 11:30 AM")
    st.write("Saturday: 9:30 AM - 11:30 AM")
    
    st.subheader("General Classes")
    st.write("Sunday: 7:00 AM - 09:00 AM : 06:00 PM - 08:00 PM")
    st.write("Wednesday: 7:15 PM - 8:45 PM")
    
    st.subheader("Special Classes")
    st.write("Kayakalpa Yoga: Every 2nd Sunday 01:30 PM - 05:30 PM")
    st.write("Introspection: Every 3rd Sunday 09:00 AM - 05:30 PM")
    
    st.divider()

elif menu == "Member Login":
    st.header("Member Login")
    show_logo()
    
    phone = st.text_input("Phone Number (e.g. 91234567)")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if not phone or not password:
            st.warning("Please enter phone and password")
        else:
            # ===== TRY GOOGLE SHEET LOGIN =====
            try:
                # If you have google sheet connected in secrets
                sheet_url = st.secrets.get("SHEET_URL", "")
                if sheet_url:
                    df = pd.read_csv(sheet_url)
                    # Expect columns: phone, password, name
                    user = df[(df['phone'].astype(str) == str(phone)) & (df['password'].astype(str) == str(password))]
                    if not user.empty:
                        st.success(f"Vazhga Valamudan {user.iloc[0].get('name','Member')}! Login Success 🙏")
                        st.balloons()
                        st.write("### Your Details")
                        st.dataframe(user)
                    else:
                        st.error("Invalid phone or password. Please contact admin 8057 2762")
                else:
                    # No sheet yet - demo login
                    if phone == "80572762" and password == "vmsky123":
                        st.success("Demo Login Success! Vazhga Valamudan 🙏")
                        st.write("Add your Google Sheet URL in Streamlit Secrets to enable real login")
                    else:
                        st.error("Invalid login. For demo use Phone: 80572762 Password: vmsky123")
                        st.info("To enable real members login, add your Google Sheet CSV link in Streamlit Secrets as SHEET_URL")
            except Exception as e:
                st.error(f"Login error: {e}")
                st.info("Please check Google Sheet format. Need columns: phone, password, name")

    st.divider()
    st.write("Forgot password? WhatsApp admin: 8057 2762")
    st.link_button("Contact Admin on WhatsApp", WHATSAPP_LINK)

elif menu == "Class Timings":
    show_logo()
    st.header("VMSKY Singapore - Regular Class Timings")
    
    st.subheader("Ladies Only Classes")
    st.write("Tuesday: 9:30 AM - 11:30 AM")
    st.write("Thursday: 9:30 AM - 11:30 AM")
    st.write("Saturday: 9:30 AM - 11:30 AM")
    
    st.subheader("General Classes")
    st.write("Sunday: 7:00 AM - 09:00 AM : 06:00 PM - 08:00 PM")
    st.write("Wednesday: 7:15 PM - 8:45 PM")
    
    st.subheader("Special Classes")
    st.write("Kayakalpa Yoga: Every 2nd Sunday 01:30 PM - 05:30 PM")
    st.write("Introspection: Every 3rd Sunday 09:00 AM - 05:30 PM")

    st.divider()
    st.write(VENUE_ADDRESS)
    st.link_button("Open in Maps App", f"https://www.google.com/maps/dir/?api=1&destination={MAPS_DEST}")

elif menu == "Contact Us":
    show_logo()
    st.header("Contact Us")
    st.write(VENUE_NAME)
    st.write(VENUE_ADDRESS)
    st.write("Phone: +65 8057 2762")
    st.link_button("WhatsApp Us", WHATSAPP_LINK)
    st.link_button("Open in Maps App", f"https://www.google.com/maps/dir/?api=1&destination={MAPS_DEST}")
