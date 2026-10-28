import streamlit as st
import os
import pandas as pd
from datetime import datetime, date

st.set_page_config(page_title="VMSKY Singapore", layout="centered")

# ===== VENUE FINAL =====
VENUE_NAME = "VMSKY, Temple of Consciousness"
VENUE_ADDRESS = "11 Woodlands Cl, #09-13, Singapore 737853"
MAPS_DEST = "11+Woodlands+Cl+%2309-13+Singapore+737853"
WHATSAPP = "https://wa.me/6580572762"

# Master login - Change here
MASTER_PHONE = "80572762"
MASTER_PASS = "master123"

menu = st.sidebar.selectbox("Menu", ["Home", "Member Login", "Master Login", "Class Timings", "Members Details", "Attendance", "Contact Us"])

def show_logo():
    for f in ["logo.png", "maharishi_final_logo.png"]:
        if os.path.exists(f):
            st.image(f, use_container_width=True)
            return

def show_map_buttons():
    st.link_button("🗺️ Open in Google Maps App", f"https://www.google.com/maps/search/?api=1&query={MAPS_DEST}")
    st.link_button("🧭 Get Directions", f"https://www.google.com/maps/dir/?api=1&destination={MAPS_DEST}")

def show_class_timing():
    st.header("VMSKY Singapore - Regular Class Timings")
    st.subheader("Ladies Class")
    st.write("Tuesday: 09:30 AM to 11:30 AM")
    st.write("Wednesday: 09:30 AM to 11:30 AM")
    st.write("Thursday: 09:30 AM to 11:30 AM")
    st.divider()
    st.subheader("Common Class")
    st.write("Wednesday: 07:15 PM to 08:45 PM")
    st.write("**Saturday:** Morning 07:00 AM to 09:00 AM | Evening 06:00 PM to 08:00 PM")
    st.write("**Sunday:** Morning 07:00 AM to 09:00 AM | Evening 06:00 PM to 08:00 PM")
    st.divider()
    st.subheader("Special Class")
    st.write("Kayakalpam Yoga: Every Month 2nd Sunday 01:30 PM to 05:30 PM")
    st.write("Introspection: Every Month 3rd Sunday 09:00 AM to 05:30 PM")

# ===== LOAD MEMBERS SHEET =====
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
    st.write(f"**{VENUE_NAME}**")
    st.write(VENUE_ADDRESS)
    show_map_buttons()
    st.divider()
    show_class_timing()

# ===== MEMBER LOGIN =====
elif menu == "Member Login":
    st.header("🔐 Member Login")
    show_logo()
    phone = st.text_input("Contact Number")
    password = st.text_input("Password", type="password")
    if st.button("Login", type="primary"):
        df = load_members()
        if not df.empty:
            # Find column names flexibly
            phone_col = [c for c in df.columns if 'contact' in c.lower() or 'phone' in c.lower()][0]
            pass_col = [c for c in df.columns if 'pass' in c.lower()][0] if any('pass' in c.lower() for c in df.columns) else phone_col
            user = df[df[phone_col].astype(str).str.strip() == str(phone).strip()]
            if not user.empty:
                st.success(f"Vazhga Valamudan {user.iloc[0].get('Name', 'Member')}! 🙏")
                st.balloons()
                st.write("**Your Details:**")
                st.dataframe(user.T)
                
                # Show Attendance %
                if 'Attendance' in df.columns or 'attendance' in str(df.columns):
                    st.metric("Attendance %", f"{user.iloc[0].get('Attendance %', '0')}%")
                else:
                    # Calculate from attendance log
                    st.info("Attendance: Weekly 3 classes = 100%")
            else:
                st.error("Member not found. Contact Admin 8057 2762")
        else:
            if phone == MASTER_PHONE and password == MASTER_PASS:
                st.success("Demo Master Login - Add Google Sheet to enable real members")
            else:
                st.error("Add Google Sheet in Secrets to enable login")

# ===== MASTER LOGIN - ATTENDANCE CONFIRM =====
elif menu == "Master Login":
    st.header("👑 Master Login - Attendance Confirm")
    show_logo()
    m_phone = st.text_input("Master Phone")
    m_pass = st.text_input("Master Password", type="password")
    
    if st.button("Master Login"):
        if m_phone == MASTER_PHONE and m_pass == MASTER_PASS:
            st.session_state['master'] = True
            st.success("Master Login Success! Vazhga Valamudan 🙏")
        else:
            sheet_url = st.secrets.get("SHEET_URL", "")
            if sheet_url:
                df = load_members()
                # Check if master in sheet with Level = Master or Arulnithi
                if not df.empty and any('Arulnithi' in str(df.values) or 'Master' in str(df.values)):
                    st.success("Checking sheet for Master...")
            else:
                st.error("Invalid Master login. Default: 80572762 / master123")

    if st.session_state.get('master'):
        st.divider()
        st.subheader("📝 Mark Attendance - Scan / Enter Contact Number")
        
        df = load_members()
        contact_num = st.text_input("Enter Member Contact Number to Mark Attendance")
        level_today = st.selectbox("Today's Class Level", 
            ["Exercise", "Kayakalpam", "Agnai", "Santhi", "Thanduvadasuthi", "Thuriyam", 
             "Introspection 1", "Introspection 2", "Introspection 3", "Bramaganam", "Arulnithi"])
        
        if st.button("Confirm Attendance ✅"):
            if contact_num:
                # Save attendance to session (and download)
                if 'attendance_log' not in st.session_state:
                    st.session_state['attendance_log'] = []
                
                log_entry = {
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Contact Number": contact_num,
                    "Name": "Member" if df.empty else (df[df.astype(str).apply(lambda x: x.str.contains(contact_num, na=False)).any(axis=1)].iloc[0]['Name'] if not df[df.astype(str).apply(lambda x: x.str.contains(contact_num, na=False)).any(axis=1)].empty else contact_num),
                    "Level": level_today,
                    "Confirmed By": "Master",
                    "Venue": VENUE_ADDRESS
                }
                st.session_state['attendance_log'].append(log_entry)
                st.success(f"Attendance Confirmed for {contact_num} - {level_today} 🙏")
                st.balloons()
            else:
                st.warning("Enter contact number")

        if st.session_state.get('attendance_log'):
            st.divider()
            st.subheader("Today's Attendance Log")
            log_df = pd.DataFrame(st.session_state['attendance_log'])
            st.dataframe(log_df, use_container_width=True)
            
            # Calculate Attendance %
            st.write("**Attendance % Calculation:** Weekly 3 classes = 100%")
            for entry in st.session_state['attendance_log']:
                count = sum(1 for x in st.session_state['attendance_log'] if x['Contact Number'] == entry['Contact Number'])
                percent = min(count / 3 * 100, 100)
                st.write(f"{entry['Contact Number']}: {count} classes = {percent:.0f}%")

            # Download button
            csv = log_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Attendance CSV", csv, f"attendance_{date.today()}.csv", "text/csv")

# ===== CLASS TIMINGS =====
elif menu == "Class Timings":
    show_logo()
    show_class_timing()
    show_map_buttons()

# ===== MEMBERS DETAILS - SEE AND DOWNLOAD =====
elif menu == "Members Details":
    st.header("👥 Members Details - See & Download")
    show_logo()
    
    df = load_members()
    if not df.empty:
        st.success(f"Total Members: {len(df)}")
        
        # Search
        search = st.text_input("Search by Name / Contact / Level")
        if search:
            filtered = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)]
            st.dataframe(filtered, use_container_width=True)
            
            # Download filtered
            csv = filtered.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Filtered Data", csv, "filtered_members.csv", "text/csv")
        else:
            st.dataframe(df, use_container_width=True)
        
        # Full download
        csv_all = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download ALL Members Details", csv_all, f"VMSKY_Members_{date.today()}.csv", "text/csv")
        
        # Show columns
        st.divider()
        st.subheader("Columns in Sheet")
        st.write(list(df.columns))
        
    else:
        st.warning("Google Sheet not connected")
        st.info("Your Google Sheet should have these columns:")
        demo = pd.DataFrame({
            "Name": ["Ramesh", "Lakshmi"],
            "Contact Number": ["91234567", "87654321"],
            "Level": ["Exercise", "Thuriyam"],
            "Email Address": ["ramesh@gmail.com", "lakshmi@gmail.com"],
            "Attendance %": ["100%", "66%"],
            "Password": ["123
