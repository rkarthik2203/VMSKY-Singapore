import streamlit as st
import os
import pandas as pd
from datetime import datetime, date
import qrcode
from PIL import Image
import io

st.set_page_config(page_title="VMSKY Singapore", layout="centered")

VENUE_NAME = "VMSKY, Temple of Consciousness"
VENUE_ADDRESS = "11 Woodlands Cl, #09-13, Singapore 737853"
MAPS_DEST = "11+Woodlands+Cl+%2309-13+Singapore+737853"
WHATSAPP = "https://wa.me/6580572762"
MASTER_PHONE = "80572762"
MASTER_PASS = "master123"

menu = st.sidebar.selectbox("Menu", ["Home", "Member Login", "Master Login", "Class Timings", "Members Details", "Attendance", "Contact Us"])

def show_logo():
    for f in ["logo.png", "maharishi_final_logo.png"]:
        if os.path.exists(f):
            st.image(f, use_container_width=True)
            return

def show_map_buttons():
    st.link_button("Open in Google Maps App", f"https://www.google.com/maps/search/?api=1&query={MAPS_DEST}")
    st.link_button("Get Directions", f"https://www.google.com/maps/dir/?api=1&destination={MAPS_DEST}")

def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

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

# ===== HOME =====
if menu == "Home":
    st.markdown("<h1 style='text-align:center; color:#FF8C00; font-size:20px;'>Vazhga Vaiyagam Vazhga Valamudan</h1>", unsafe_allow_html=True)
    show_logo()
    st.write(VENUE_NAME)
    st.write(VENUE_ADDRESS)
    show_map_buttons()
    st.divider()
    show_class_timing()

# ===== MEMBER LOGIN + SCAN MASTER QR =====
elif menu == "Member Login":
    st.header("Member Login - Scan Master QR for Attendance")
    show_logo()
    phone = st.text_input("Your Contact Number")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
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
                    st.session_state['member_phone'] = phone
                    st.session_state['member_name'] = str(user.iloc[0].get('Name', 'Member'))
                    st.success(f"Vazhga Valamudan {st.session_state['member_name']}! Now scan Master QR below")
                else:
                    st.error("Member not found")
        else:
            # Demo login
            st.session_state['member_phone'] = phone if phone else "91234567"
            st.session_state['member_name'] = "Demo Member"
            st.success("Demo Login OK - Now scan Master QR")

    if st.session_state.get('member_phone'):
        st.divider()
        st.subheader("📱 Scan Master QR Code to Confirm Attendance")
        st.write("Ask Master to show his QR code on his phone, then scan or enter code below:")
        
        # Master QR for today - members need to enter what master shows
        master_qr_code = st.text_input("Enter Master QR Code Text (shown on Master phone)", placeholder="Example: VMSKY-MASTER-2026-05-13-WED-Common")
        
        # Also camera scan option
        st.write("OR Scan via Camera:")
        camera_image = st.camera_input("Scan QR Code")
        
        if camera_image:
            st.info("Camera captured! If QR is visible, enter the code text above to confirm.")
        
        level_today = st.selectbox("Today Level", ["Exercise", "Kayakalpam", "Agnai", "Santhi", "Thanduvadasuthi", "Thuriyam", "Introspection 1", "Introspection 2", "Introspection 3", "Bramaganam", "Arulnithi"])
        
        if st.button("Confirm My Attendance ✅"):
            if master_qr_code or camera_image:
                if 'attendance_log' not in st.session_state:
                    st.session_state['attendance_log'] = []
                
                entry = {
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Contact Number": st.session_state['member_phone'],
                    "Name": st.session_state['member_name'],
                    "Level": level_today,
                    "Master QR": master_qr_code if master_qr_code else "Camera Scan",
                    "Type": "Member",
                    "Attendance %": "Calculated"
                }
                st.session_state['attendance_log'].append(entry)
                st.success(f"Attendance Confirmed for {st.session_state['member_name']} - {level_today} 🙏")
                st.balloons()
                
                # Show attendance %
                count = sum(1 for x in st.session_state['attendance_log'] if x['Contact Number'] == st.session_state['member_phone'])
                percent = min(count / 3 * 100, 100)
                st.metric("Your Weekly Attendance", f"{percent:.0f}%", f"{count}/3 classes")
            else:
                st.warning("Please enter Master QR code or scan")

# ===== MASTER LOGIN + GENERATE QR + SCAN OTHER MASTER =====
elif menu == "Master Login":
    st.header("Master Login - Generate QR & Attendance")
    show_logo()
    m_phone = st.text_input("Master Phone")
    m_pass = st.text_input("Master Password", type="password")
    
    if st.button("Master Login"):
        if m_phone == MASTER_PHONE and m_pass == MASTER_PASS:
            st.session_state['master'] = True
            st.session_state['master_phone'] = m_phone
            st.success("Master Login Success!")
        else:
            st.error("Invalid - Use 80572762 / master123")

    if st.session_state.get('master'):
        st.divider()
        
        # ===== MASTER GENERATES QR FOR MEMBERS TO SCAN =====
        st.subheader("🔲 Your Master QR Code - Show to Members to Scan")
        
        today = date.today().strftime("%Y-%m-%d")
        current_class = st.selectbox("Select Current Class", ["Ladies", "Common-Wed", "Common-Sat-Morning", "Common-Sat-Evening", "Common-Sun-Morning", "Common-Sun-Evening", "Kayakalpam", "Introspection"])
        
        qr_data = f"VMSKY-MASTER-{today}-{current_class}-{MASTER_PHONE}-VALID"
        st.write(f"**QR Code Data:** `{qr_data}`")
        
        qr_image = generate_qr(qr_data)
        st.image(qr_image, caption=f"Master QR for {today} - {current_class}", width=300)
        st.info("Members scan this QR from their app to mark attendance")
        
        st.divider()
        
        # ===== MASTER SCANS OTHER MASTER QR FOR HIS OWN ATTENDANCE =====
        st.subheader("📱 Master to Master Attendance - Scan Other Master QR")
        st.write("If you are a Master, scan another Master's QR to mark your attendance:")
        
        other_master_qr = st.text_input("Enter Other Master QR Code", placeholder="VMSKY-MASTER-2026-05-13-...")
        camera_master = st.camera_input("Scan Other Master QR")
        
        if st.button("Confirm My Master Attendance"):
            if other_master_qr or camera_master:
                if 'attendance_log' not in st.session_state:
                    st.session_state['attendance_log'] = []
                
                entry = {
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Contact Number": st.session_state.get('master_phone', MASTER_PHONE),
                    "Name": f"Master-{st.session_state.get('master_phone', MASTER_PHONE)}",
                    "Level": current_class,
                    "Master QR": other_master_qr if other_master_qr else "Camera Scan",
                    "Type": "Master-to-Master",
                    "Attendance %": "100%"
                }
                st.session_state['attendance_log'].append(entry)
                st.success("Master Attendance Confirmed via Other Master QR 🙏")
                st.balloons()
            else:
                st.warning("Enter other Master QR code")
        
        if st.session_state.get('attendance_log'):
            st.divider()
            st.subheader("Today Attendance Log")
            log_df = pd.DataFrame(st.session_state['attendance_log'])
            st.dataframe(log_df, use_container_width=True)
            csv = log_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Attendance CSV", csv, f"attendance_{date.today()}.csv", "text/csv")

elif menu == "Class Timings":
    show_logo()
    show_class_timing()
    show_map_buttons()

elif menu == "Members Details":
    st.header("Members Details - See & Download")
    show_logo()
    df = load_members()
    if not df.empty:
        st.success(f"Total Members: {len(df)}")
        st.dataframe(df, use_container_width=True)
        csv_all = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download ALL Members", csv_all, f"VMSKY_Members_{date.today()}.csv", "text/csv")
    else:
        st.warning("Add SHEET_URL in Secrets")
        demo = pd.DataFrame({
            "Name": ["Ramesh", "Lakshmi"],
            "Contact Number": ["91234567", "87654321"],
            "Level": ["Exercise", "Thuriyam"],
            "Email Address": ["a@b.com", "c@d.com"]
        })
        st.dataframe(demo)

elif menu == "Attendance":
    st.header("Attendance Report")
    show_logo()
    if st.session_state.get('attendance_log'):
        log_df = pd.DataFrame(st.session_state['attendance_log'])
        st.dataframe(log_df, use_container_width=True)
        summary = log_df['Contact Number'].value_counts().reset_index()
        summary.columns = ['Contact Number', 'Classes Attended']
        summary['Attendance %'] = summary['Classes Attended'].apply(lambda x: min(x/3*100, 100))
        st.dataframe(summary)
        csv = summary.to_csv(index=False).encode('utf-8')
        st.download_button("Download Attendance %", csv, f"attendance_percent_{date.today()}.csv", "text/csv")
    else:
        st.info("No attendance today")

elif menu == "Contact Us":
    show_logo()
    st.header("Contact Us")
    st.write(VENUE_NAME)
    st.write(VENUE_ADDRESS)
    st.link_button("WhatsApp Us", WHATSAPP)
    show_map_buttons()
