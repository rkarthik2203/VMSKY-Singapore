import streamlit as st
from datetime import datetime

# ========== EASY SETTINGS - CHANGE HERE ANYTIME ==========
APP_NAME = "VMSKY Singapore"
APP_COLOR_PRIMARY = "#0A3D8A"  # Change to any color: #800000 = maroon, #006400 = green
APP_COLOR_ORANGE = "#FF8C00"
BLESSING_LEFT = "வாழ்க வையகம்"
BLESSING_RIGHT = "வாழ்க வளமுடன்"
import streamlit as st

st.markdown("""
### 🧘‍♀️ VMSKY Singapore - Regular Class Timings

#### 👩 Ladies Only Classes
**Tuesday, Wednesday, Thursday**
🕤 Morning: 9:30 AM to 11:30 AM

#### 👨‍👩‍👧‍👦 General Classes (Everyone)
**Saturday & Sunday**
🌅 Morning: 7:00 AM to 9:00 AM
🌇 Evening: 6:00 PM to 8:00 PM

---
#### ✨ Special Classes

**Kayakalpam Yoga**
🗓️ Every Month - 2nd Sunday
🕜 1:30 PM to 5:30 PM

**Introspection Course (Manavalakalai)**
🗓️ Every Month - 3rd Sunday
🕘 9:00 AM to 5:30 PM (Full Day)

---
📍 **Venue:** VMSKY Trust, 126 Joo Seng Road, Singapore
📞 **Contact us on WhatsApp for booking**
""")
# 16 Levels
COURSES = [
    "1. Foundation Course - அடிப்படை பயிற்சி",
    "2. Kundalini Yoga Basic",
    "3. Introspection I - அகத்தாய்வு I",
    "4. Introspection II",
    "5. Introspection III",
    "6. Brahma Gnanam L1",
    "7. Brahma Gnanam L2",
    "8. Kaya Kalpa Yoga - காயகல்ப யோகா",
    "9. Advanced Kundalini",
    "10. Turiyatheetham - துரியாதீதம்",
    "11. Perception of Consciousness",
    "12. Brahmanandam",
    "13. Assistant Master Course",
    "14. Master Course L1",
    "15. Master Course L2 (Professor) - பேராசிரியர்",
    "16. Senior Professor - Brahma Gnanam Master",
]

st.set_page_config(page_title=APP_NAME, page_icon="🧘", layout="centered")

# Style
st.markdown(f"""
<style>
.stApp {{background: #F8FBFF;}}
.header {{background: linear-gradient(90deg, {APP_COLOR_PRIMARY}, {APP_COLOR_ORANGE}); color:white; padding:20px; border-radius:15px; text-align:center;}}
.bless {{display:flex; justify-content:space-between; color:{APP_COLOR_PRIMARY}; font-weight:bold; margin:10px 0;}}
</style>
""", unsafe_allow_html=True)

if 'login' not in st.session_state:
    st.session_state.login = False
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'role' not in st.session_state:
    st.session_state.role = ""

def splash():
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown(f"<h1 style='text-align:center; color:{APP_COLOR_PRIMARY}'>VMSKY Singapore</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center'>Vethathiri Maharishi Simplified Kundalini Yoga</p>", unsafe_allow_html=True)
    st.markdown(f"<div class='bless'><span>{BLESSING_LEFT}</span><span>{BLESSING_RIGHT}</span></div>", unsafe_allow_html=True)
    st.markdown("---")

if not st.session_state.login:
    splash()
    st.markdown(f"<div class='header'><h2>{APP_NAME}</h2><p>Vethathiri Maharishi Simplified Kundalini Yoga</p></div>", unsafe_allow_html=True)
    st.write("")
    name = st.text_input("Your Name / உங்கள் பெயர்")
    role = st.selectbox("Your Level / நிலை", ["Level 1 - Student / Member", "Level 2 - Teacher / Assistant Master", "Level 3 - Master / Admin (You)"])
    if st.button("Login 🙏 Vazhga Valamudan", type="primary", use_container_width=True):
        if name:
            st.session_state.name = name
            st.session_state.role = role
            st.session_state.login = True
            st.rerun()
        else:
            st.warning("Please enter name")
else:
    splash()
    st.sidebar.title(APP_NAME)
    st.sidebar.write(f"👤 {st.session_state.name}")
    st.sidebar.write(f"🎓 {st.session_state.role}")
    menu = st.sidebar.radio("Menu", ["🏠 Dashboard", "📚 16 Levels Courses", "🧘 Daily Practice", "⚙️ Master Settings"])
    
    if menu == "🏠 Dashboard":
        st.header(f"Vazhga Valamudan, {st.session_state.name}!")
        col1, col2, col3 = st.columns(3)
        col1.metric("Level", "Foundation")
        col2.metric("Members", "250+")
        col3.metric("Next Class", "Sunday 9AM")
        st.info("💡 Today's Blessing: Vazhga Vaiyagam Vazhga Valamudan — Maharishi")
        st.success("Your app is working with your final Maharishi logo!")
    
    elif menu == "📚 16 Levels Courses":
        st.header("16 Levels - From Foundation to Professor")
        for c in COURSES:
            with st.expander(c):
                st.write("Course content, videos, PDFs will be here")
                if "Level 3" in st.session_state.role:
                    st.button(f"Edit {c}", key=c)
                else:
                    st.button(f"Join / View", key=c)
    
    elif menu == "🧘 Daily Practice":
        st.header("Daily Practice Log")
        st.write("Morning meditation, evening introspection")
        mood = st.select_slider("How peaceful today?", ["Low", "Medium", "High", "Blissful"])
        if st.button("Save Practice"):
            st.success(f"Saved! Vazhga Valamudan! Mood: {mood}")
    
    elif menu == "⚙️ Master Settings":
        if "Level 3" in st.session_state.role:
            st.header("Master Control - Only You")
            st.write("Here you can change app color and logo")
            color = st.color_picker("Pick App Primary Color", APP_COLOR_PRIMARY)
            st.write(f"Copy this code {color} and replace in top of app.py line APP_COLOR_PRIMARY")
            st.file_uploader("Upload new logo (rename to logo.png)")
            st.success("You are Master — Full Access!")
        else:
            st.error("Only Level 3 Master can access. Please login as Master.")
    
    if st.sidebar.button("Logout"):
        st.session_state.login = False
        st.rerun()
