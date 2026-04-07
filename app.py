# ==========================================
# 📞 Contact & Support
# For questions, feedback, or technical issues, please contact our support team.
# Version: 2.0 | Last Updated: 2026
# ==========================================

import streamlit as st
from config import PAGE_CONFIG
from pages.home import show_home_page
from pages.about import show_about_page

# --- STEP 1: THE ABSOLUTE FIRST STREAMLIT COMMAND ---
# This MUST come before any other st. command or any UI-rendering strings.
st.set_page_config(**PAGE_CONFIG)

# --- STEP 2: SESSION STATE INITIALIZATION ---
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# --- STEP 3: CUSTOM CSS (Merged Styling) ---
st.markdown("""
<style>
/* Global Font & Reset */
* {font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}
body, html {margin: 0; padding: 0;}

/* Dark Theme Background */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1a1f35 100%);
    color: #e2e8f0;
}

/* Custom Header Styling */
.top-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    padding: 32px 40px;
    margin-bottom: 0;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.15);
}

.title-block {
    display: flex;
    align-items: center;
    gap: 20px;
}

.logo-icon {
    width: 100px;
    height: 100px;
    border-radius: 20px;
    background: linear-gradient(135deg, rgba(56, 189, 248, 0.3), rgba(99, 102, 241, 0.2));
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 50px;
    border: 2px solid rgba(56, 189, 248, 0.3);
}

.title-text {
    margin: 0;
    color: #ffffff !important;
    font-size: 7rem !important;
    font-weight: 900 !important;
    line-height: 0.88 !important;
    letter-spacing: -2px !important;
    background: linear-gradient(135deg, #38bdf8, #6366f1) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}

.subtitle-text {
    margin: 0 !important;
    color: #cbd5e0 !important;
    font-size: 1.8rem !important;
    margin-top: 8px !important;
    font-weight: 500 !important;
}

/* Navigation Buttons */
.stButton > button {
    background: linear-gradient(135deg, #38bdf8, #06b6d4) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 28px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(56, 189, 248, 0.4) !important;
}

/* Selectbox & Inputs */
.stSelectbox > div {
    background-color: #1e293b !important;
    border: 2px solid #334155 !important;
    border-radius: 12px !important;
}

/* Hide Default Streamlit Elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

# --- STEP 4: RENDER THE HEADER ---
st.markdown("""
<div class='top-header'>
    <div class='title-block'>
        <div class='logo-icon'>🛡️</div>
        <div>
            <p class='title-text'>Kawach</p>
            <p class='subtitle-text'>AI Diagnostic Hub</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- STEP 5: NAVIGATION MENU ---
st.write("") # Spacer
nav1, nav2 = st.columns([1, 1])

with nav1:
    if st.button("🏠 Home", key="nav_home", use_container_width=True):
        st.session_state.current_page = "Home"
        st.rerun()

with nav2:
    if st.button("ℹ️ About", key="nav_about", use_container_width=True):
        st.session_state.current_page = "About"
        st.rerun()

# --- STEP 6: PAGE ROUTING CONTENT ---
if st.session_state.current_page == "Home":
    show_home_page()
else:
    show_about_page()