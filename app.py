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

# Initialize storage for new registrations and password changes
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

# ===== NEW REGISTRATION - Members fill by their own =====
elif menu == "New Registration":
    st.header("📝 New Member Registration")
    show_logo()
    st.write("Fill your details - Master will approve and assign Level")
    
    with st.form("registration"):
        name = st.text_input("Full Name *")
        contact = st.text_input("Mobile Number * (e.g. 91234567)")
        email = st.text_input("Email Address *")
        dob = st.date_input("Date of Birth", value=date(1990, 1, 1))
        address = st.text_area("Address")
        emergency = st.text_input("Emergency Contact Number")
        password = st.text_input("Create Password *", type="password")
        confirm_pass = st.text_input("Confirm Password *", type="password")
        how_know = st.selectbox("How did you know about VMSKY?", ["Friend", "Facebook", "WhatsApp", "Temple", "Others"])
        
        submit = st.form_submit_button("Register Now", type="primary")
        
        if submit:
            if not name or not contact or not email or not password:
                st.error("Please fill all * fields")
            elif password != confirm_pass:
                st.error("Passwords do not match!")
            elif len(contact) < 8:
                st.error("Enter valid mobile number")
            else:
                new_member = {
                    "Name": name,
                    "Contact Number": contact,
                    "Email Address": email,
                    "DOB": str(dob),
                    "Address": address,
                    "Emergency Contact": emergency,
                    "Password": password,
                    "Level": "Exercise - Pending Master Approval",
                    "Attendance %": "0%",
                    "Registration Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "How Know": how_know,
                    "Status": "Pending"
                }
                st.session_state['new_registrations'].append(new_member)
                st.success(f"Vazhga Valamudan {name}! Registration Success 🙏")
                st.info("Master will review and assign your Level. You can login after approval.")
                st.balloons()
                
                # Show for download
                st.write("Your Registration Details:")
                st.json(new_member)

    if st.session_state['new_registrations']:
        st.divider()
        st.subheader("Recent Registrations (For Master)")
        df_new = pd.DataFrame(st.session_state['new_registrations'])
        st.dataframe(df_new, use_container_width=True)
        csv = df_new.to_csv(index=False).encode('utf-8')
        st.download_button("Download New Registrations", csv, f"new_members_{date.today()}.csv", "text/csv")
        st.caption("Master: Copy these to your Google Sheet to enable login")

# ===== CHANGE PASSWORD - Member and Master =====
elif menu == "Change Password":
    st.header("🔑 Change Password")
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
            elif len(new_pass) < 4:
                st.error("New password must be at least 4 characters")
            else:
                df = load_members()
                if not df.empty:
                    phone_col = None
                    for c in df.columns:
                        if "contact" in c.lower() or "phone" in c.lower():
                            phone_col = c
                            break
                    if phone_col:
                        user = df[df[phone_col].astype(str).str.strip() == str(phone).strip()]
                        if not user.empty:
                            # In real sheet, you need to update via Google Sheets API
                            st.session_state['password_changes'][phone] = new_pass
                            st.success(f"Password changed for {phone}! 🙏")
                            st.warning("Note: For Google Sheet, Master needs to manually update password in sheet. This change is saved locally for now.")
                            st.info(f"Master: Please update in Google Sheet - Contact {phone} New Password: {new_pass}")
                        else:
                            st.error("Member not found")
                else:
                    # Demo
                    st.session_state['password_changes'][phone] = new_pass
                    st.success("Demo: Password changed locally! Add to Google Sheet manually")
    
    else:  # Master
        st.subheader("Master Change Password")
        master_phone = st.text_input("Master Phone")
        old_master_pass = st.text_input("Old Master Password", type="password")
        new_master_pass = st.text_input("New Master Password", type="password")
        confirm_master_new = st.text_input("Confirm New Master Password", type="password")
        
        if st.button("Change Master Password", type="primary"):
            if master_phone == MASTER_PHONE and old_master_pass == MASTER_PASS:
                if new_master_pass != confirm_master_new:
                    st.error("New passwords do not match")
                elif len(new_master_pass) < 4:
                    st.error("Password too short")
                else:
                    st.session_state['master_new_pass'] = new_master_pass
                    st.success("Master Password Changed! 🙏")
                    st.warning(f"New Master Password is: {new_master_pass} - Please update in app.py MASTER
