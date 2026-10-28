import streamlit as st
import os
import pandas as pd
from datetime import datetime, date
import qrcode
import io

st.set_page_config(page_title="VMSKY Singapore", layout="centered")

VENUE_NAME = "VMSKY Temple of Consciousness"
VENUE_ADDRESS = "11 Woodlands Cl 09-13 Singapore 737853"
MAPS_LINK = "https://www.google.com/maps/search/?api=1&query=11+Woodlands+Cl+Singapore"
WHATSAPP_LINK = "https://wa.me/6580572762"
WHATSAPP_MSG = "https://wa.me/6580572762?text=Vazhga%20Valamudan%20VMSKY%20Enquiry about Class"
MASTER_PHONE = "80572762"
MASTER_PASS = "master123"

menu = st.sidebar.selectbox("Menu", ["Home", "Member Login", "New Registration", "Change Password", "Master Login", "Class Timings", "Members Details", "Attendance", "Contact Us"])

def show_logo():
    for f in ["logo.png", "maharishi_final_logo.png"]:
        if os.path.exists(f):
            st.image(f, use_container_width=True)

def whatsapp_buttons():
    st.link_button("WhatsApp Chat", WHATSAPP_LINK)
    st.link_button("WhatsApp With Msg", WHATSAPP_MSG)

def map_buttons():
    st.link_button("Open Google Maps", MAPS_LINK)
    st.link_button("Get Directions", MAPS_LINK)

def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='blue', back_color='white')
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

def apply_level_changes(df):
    # Fix for level update not showing
    changes = st.session_state.get('level_changes', {})
    if not changes:
        return df
    # Try common contact column names
    contact_cols = ["Contact Number", "Contact", "Mobile", "Phone"]
    contact_col = None
    for col in contact_cols:
        if col in df.columns:
            contact_col = col
            break
    if contact_col is None:
        return df
    for phone, new_level in changes.items():
        try:
            mask = df[contact_col].astype(str).str.contains(str(phone), na=False)
            df.loc[mask, "Level"] = new_level
        except:
            pass
    return df

if 'new_registrations' not in st.session_state:
    st.session_state['new_registrations'] = []
if 'password_changes' not in st.session_state:
    st.session_state['password_changes'] = {}
if 'attendance_log' not in st.session_state:
    st.session_state['attendance_log'] = []
if 'level_changes' not in st.session_state:
    st.session_state['level_changes'] = {}

# HOME - FULL FEATURES BACK
if menu == "Home":
    st.markdown("<h2 style='text-align:center;color:orange'>Vazhga Vaiyagam Vazhga Valamudan</h2>", unsafe_allow_html=True)
    show_logo()
    st.subheader("Address")
    st.write(VENUE_NAME)
    st.write(VENUE_ADDRESS)
    st.divider()
    st.subheader("WhatsApp Us")
    whatsapp_buttons()
    st.write("Phone 80572762")
    st.divider()
    st.subheader("Location")
    map_buttons()
    st.divider()
    st.subheader("Class Timings")
    
    # Ladies Class - Pink Color Big Size
    st.markdown("<h2 style='color:#E91E63; font-size:28px;'>Ladies Class</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#880E4F; font-size:20px; font-weight:bold;'>Tue 09:30 AM to 11:30 AM</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#880E4F; font-size:20px; font-weight:bold;'>Wed 09:30 AM to 11:30 AM</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#880E4F; font-size:20px; font-weight:bold;'>Thu 09:30 AM to 11:30 AM</p>", unsafe_allow_html=True)
    
    st.divider()
    
    # Common Class - Blue Color Big Size
    st.markdown("<h2 style='color:#1565C0; font-size:28px;'>Common Class</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#0D47A1; font-size:20px; font-weight:bold;'>Wed 07:15 PM to 08:45 PM</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#0D47A1; font-size:20px; font-weight:bold;'>Sat 07:00 AM to 09:00 AM</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#0D47A1; font-size:20px; font-weight:bold;'>Sat 06:00 PM to 08:00 PM</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#0D47A1; font-size:20px; font-weight:bold;'>Sun 07:00 AM to 09:00 AM</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#0D47A1; font-size:20px; font-weight:bold;'>Sun 06:00 PM to 08:00 PM</p>", unsafe_allow_html=True)
    
    st.divider()
    
    # Special Class - Orange Color
    st.markdown("<h2 style='color:#FF6F00; font-size:28px;'>Special Class</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#E65100; font-size:18px; font-weight:bold;'>Kayakalpam 2nd Sunday 01:30 PM to 05:30 PM</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#E65100; font-size:18px; font-weight:bold;'>Introspection 3rd Sunday 09:00 AM to 05:30 PM</p>", unsafe_allow_html=True)

# NEW REGISTRATION
elif menu == "New Registration":
    st.header("New Registration")
    show_logo()
    name = st.text_input("Full Name")
    contact = st.text_input("Mobile Number")
    email = st.text_input("Email")
    dob = st.date_input("DOB", value=date(1990, 1, 1))
    address = st.text_area("Address")
    emergency = st.text_input("Emergency Contact")
    pwd = st.text_input("Create Password", type="password")
    cpwd = st.text_input("Confirm Password", type="password")
    how = st.selectbox("How know", ["Friend", "Facebook", "WhatsApp", "Temple", "Others"])
    if st.button("Register Now", type="primary"):
        if not name or not contact or not email or not pwd:
            st.error("Fill all")
        elif pwd != cpwd:
            st.error("No match")
        else:
            m = {}
            m["Name"] = name
            m["Contact Number"] = contact
            m["Email Address"] = email
            m["DOB"] = str(dob)
            m["Address"] = address
            m["Emergency Contact"] = emergency
            m["Password"] = pwd
            m["Level"] = "Exercise"
            m["Attendance %"] = "0"
            m["Registration Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            m["Status"] = "Pending"
            st.session_state['new_registrations'].append(m)
            st.success("Registration Success")
            st.balloons()
    if st.session_state['new_registrations']:
        df_new = pd.DataFrame(st.session_state['new_registrations'])
        df_new = apply_level_changes(df_new)
        st.dataframe(df_new, use_container_width=True)

# MEMBER LOGIN
elif menu == "Member Login":
    st.header("Member Login")
    show_logo()
    phone = st.text_input("Contact Number")
    pwd = st.text_input("Password", type="password")
    if st.button("Login", type="primary"):
        st.session_state['member_phone'] = phone
        st.session_state['member_name'] = phone
        st.success("Login OK")
    if st.button("Logout"):
        st.session_state['member_phone'] = ""
    if st.session_state.get('member_phone'):
        st.divider()
        st.subheader("Scan Master QR")
        st.write("Ask Master for QR")
        qr_text = st.text_input("Enter Master QR")
        if qr_text:
            parsed = parse_qr(qr_text)
            if parsed["valid"]:
                st.success("QR Valid")
                st.info(parsed["level"])
                if st.button("Confirm Attendance", type="primary"):
                    e = {}
                    e["Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    e["Contact Number"] = st.session_state['member_phone']
                    e["Name"] = st.session_state['member_name']
                    e["Level"] = parsed["level"]
                    e["Type"] = "Member"
                    st.session_state['attendance_log'].append(e)
                    st.success("Attendance Confirmed")
                    st.balloons()
            else:
                st.error("Invalid QR")
        # Show current level after master update
        cur_level = st.session_state['level_changes'].get(st.session_state['member_phone'], "Not updated yet")
        st.write("Your Current Level")
        st.write(cur_level)

# CHANGE PASSWORD
elif menu == "Change Password":
    st.header("Change Password")
    show_logo()
    utype = st.radio("I am", ["Member", "Master"])
    if utype == "Member":
        phone = st.text_input("Contact")
        new = st.text_input("New Password", type="password")
        cnew = st.text_input("Confirm New", type="password")
        if st.button("Change Member Password", type="primary"):
            if new != cnew:
                st.error("No match")
            else:
                st.session_state['password_changes'][phone] = new
                st.success("Password changed")
    else:
        mph = st.text_input("Master Phone")
        om = st.text_input("Old Master Pass", type="password")
        nm = st.text_input("New Master Pass", type="password")
        cnm = st.text_input("Confirm New Master", type="password")
        if st.button("Change Master Password", type="primary"):
            if mph == MASTER_PHONE and om == MASTER_PASS:
                if nm != cnm:
                    st.error("No match")
                else:
                    st.session_state['master_new_pass'] = nm
                    st.success("Master Pass Changed")
                    st.code(nm)
            else:
                st.error("Invalid")

# MASTER LOGIN - LEVEL UPDATE FIX
elif menu == "Master Login":
    st.header("Master Login")
    show_logo()
    mph = st.text_input("Master Phone")
    mpass = st.text_input("Master Password", type="password")
    cur = st.session_state.get('master_new_pass', MASTER_PASS)
    st.caption("Default 80572762 master123")
    if st.button("Master Login", type="primary"):
        if mph == MASTER_PHONE and mpass == cur:
            st.session_state['master'] = True
            st.session_state['master_phone'] = mph
            st.success("Master Login OK")
        else:
            st.error("Invalid")
    if st.session_state.get('master'):
        st.divider()
        t1, t2, t3 = st.tabs(["Generate QR", "Change Level", "New Reg"])
        with t1:
            today = date.today().strftime("%Y-%m-%d")
            lvl = st.selectbox("Lock Level", ["Exercise", "Kayakalpam", "Agnai", "Santhi", "Thanduvadasuthi", "Thuriyam", "Introspection 1", "Introspection 2", "Introspection 3", "Bramaganam", "Arulnithi"])
            ts = datetime.now().strftime("%H%M%S")
            mp = st.session_state.get('master_phone', MASTER_PHONE)
            qd = "VMSKY|" + today + "|" + lvl + "|" + mp + "|" + ts
            st.code(qd)
            img = generate_qr(qd)
            st.image(img, width=320)
        with t2:
            st.subheader("Change Member Level")
            st.write("Master only can change")
            ph = st.text_input("Member Phone Number")
            nl = st.selectbox("New Level", ["Exercise", "Kayakalpam", "Agnai", "Santhi", "Thanduvadasuthi", "Thuriyam", "Introspection 1", "Introspection 2", "Introspection 3", "Bramaganam", "Arulnithi", "Master"])
            if st.button("Update Level", type="primary"):
                if ph:
                    st.session_state['level_changes'][ph] = nl
                    st.success("Level updated")
                    st.write("Now check Members Details")
                    st.write("Level will show updated")
                else:
                    st.error("Enter phone")
            st.divider()
            st.write("All Level Changes")
            if st.session_state['level_changes']:
                for k, v in st.session_state['level_changes'].items():
                    st.write(k + " to " + v)
            else:
                st.info("No changes yet")
        with t3:
            if st.session_state['new_registrations']:
                dfn = pd.DataFrame(st.session_state['new_registrations'])
                dfn = apply_level_changes(dfn)
                st.dataframe(dfn, use_container_width=True)
                csv = dfn.to_csv(index=False).encode('utf-8')
                st.download_button("Download New", csv, "new.csv", "text/csv")
            else:
                st.info("No new reg")

# CLASS TIMINGS
elif menu == "Class Timings":
    show_logo()
    st.header("Class Timings")
    
        
    st.subheader("Class Timings")
    
    # Ladies Class - Pink Color Big Size
    st.markdown("<h2 style='color:#E91E63; font-size:28px;'>Ladies Class</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#880E4F; font-size:20px; font-weight:bold;'>Tue 09:30 AM to 11:30 AM</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#880E4F; font-size:20px; font-weight:bold;'>Wed 09:30 AM to 11:30 AM</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#880E4F; font-size:20px; font-weight:bold;'>Thu 09:30 AM to 11:30 AM</p>", unsafe_allow_html=True)
    
    st.divider()
    
    # Common Class - Blue Color Big Size
    st.markdown("<h2 style='color:#1565C0; font-size:28px;'>Common Class</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#0D47A1; font-size:20px; font-weight:bold;'>Wed 07:15 PM to 08:45 PM</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#0D47A1; font-size:20px; font-weight:bold;'>Sat 07:00 AM to 09:00 AM</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#0D47A1; font-size:20px; font-weight:bold;'>Sat 06:00 PM to 08:00 PM</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#0D47A1; font-size:20px; font-weight:bold;'>Sun 07:00 AM to 09:00 AM</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#0D47A1; font-size:20px; font-weight:bold;'>Sun 06:00 PM to 08:00 PM</p>", unsafe_allow_html=True)
    
    st.divider()
    
    # Special Class - Orange Color
    st.markdown("<h2 style='color:#FF6F00; font-size:28px;'>Special Class</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#E65100; font-size:18px; font-weight:bold;'>Kayakalpam 2nd Sunday 01:30 PM to 05:30 PM</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#E65100; font-size:18px; font-weight:bold;'>Introspection 3rd Sunday 09:00 AM to 05:30 PM</p>", unsafe_allow_html=True)
    st.divider()
    whatsapp_buttons()
    map_buttons()

# MEMBERS DETAILS - LEVEL UPDATE FIX
elif menu == "Members Details":
    st.header("Members Details")
    show_logo()
    df = load_members()
    alld = []
    if not df.empty:
        df = apply_level_changes(df)
        alld.append(df)
    if st.session_state['new_registrations']:
        df_new = pd.DataFrame(st.session_state['new_registrations'])
        df_new = apply_level_changes(df_new)
        alld.append(df_new)
    if alld:
        if len(alld) > 1:
            comb = pd.concat(alld, ignore_index=True)
        else:
            comb = alld[0]
        comb = apply_level_changes(comb)
        st.success("Total Members")
        st.write(len(comb))
        search = st.text_input("Search Name or Phone")
        if search:
            try:
                filt = comb[comb.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)]
                st.dataframe(filt, use_container_width=True)
            except:
                st.dataframe(comb, use_container_width=True)
        else:
            st.dataframe(comb, use_container_width=True)
        csv = comb.to_csv(index=False).encode('utf-8')
        st.download_button("Download All", csv, "members.csv", "text/csv")
        st.divider()
        st.subheader("Level Updates By Master")
        if st.session_state['level_changes']:
            for k, v in st.session_state['level_changes'].items():
                st.write(k + " now " + v)
        else:
            st.info("No level changes yet")
    else:
        st.warning("No members yet")
        st.write("Add SHEET_URL or register")

# ATTENDANCE
elif menu == "Attendance":
    st.header("Attendance Report")
    show_logo()
    if st.session_state['attendance_log']:
        df = pd.DataFrame(st.session_state['attendance_log'])
        df = apply_level_changes(df)
        st.dataframe(df, use_container_width=True)
        st.divider()
        st.subheader("Attendance Percentage")
        try:
            summary = df['Contact Number'].value_counts().reset_index()
            summary.columns = ['Contact Number', 'Classes']
            summary['Percent'] = summary['Classes'].apply(lambda x: min(x * 33, 100))
            st.dataframe(summary, use_container_width=True)
        except:
            st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download", csv, "attendance.csv", "text/csv")
    else:
        st.info("No attendance today")
        st.write("Master generates QR")
        st.write("Member scans QR")
        whatsapp_buttons()

# CONTACT US - FULL FEATURES BACK
elif menu == "Contact Us":
    show_logo()
    st.header("Contact Us")
    st.subheader("VMSKY Temple")
    st.write(VENUE_NAME)
    st.write(VENUE_ADDRESS)
    st.divider()
    st.subheader("WhatsApp")
    whatsapp_buttons()
    st.write("Phone 80572762")
    st.write("Default Msg Vazhga Valamudan")
    st.divider()
    st.subheader("Maps")
    map_buttons()
    st.divider()
    st.subheader("Class Timings")
    st.write("Ladies Tue Wed Thu 0930 to 1130")
    st.write("Common Wed Sat Sun")
    st.write("Kayakalpam 2nd Sunday")
    st.write("Introspection 3rd Sunday")
