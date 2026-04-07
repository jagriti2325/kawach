import streamlit as st
from config import PAGE_CONFIG
from pages.home import show_home_page
from pages.about import show_about_page

# --- STEP 1: MUST BE THE FIRST ST COMMAND ---
st.set_page_config(**PAGE_CONFIG)

# --- STEP 2: SESSION STATE ---
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# --- STEP 3: ALL CSS STYLING (Original + Dark Mode Merged) ---
st.markdown("""
<style>
/* Font and Reset */
* {font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}
body, html {margin: 0; padding: 0;}

/* Main App Background */
.stApp {background: linear-gradient(135deg, #0f172a 0%, #1a1f35 100%); color: white;}
.stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, label, span, div, button, a, li, ul, ol {color: #e2e8f0 !important;}

/* Top Header */
.top-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    padding: 32px 40px;
    margin-bottom: 0;
    border-radius: 0;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.15);
}

.title-block {
    display: flex;
    align-items: center;
    gap: 20px;
}

.logo-icon {
    width: 110px;
    height: 110px;
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(56, 189, 248, 0.3), rgba(99, 102, 241, 0.2));
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 56px;
    box-shadow: 0 8px 24px rgba(56, 189, 248, 0.2);
    border: 2px solid rgba(56, 189, 248, 0.3);
}

.title-text {
    margin: 0;
    color: #ffffff !important;
    font-size: 9.5rem !important; /* Your original large size */
    font-weight: 900 !important;
    line-height: 0.88 !important;
    letter-spacing: -2px !important;
    background: linear-gradient(135deg, #38bdf8, #6366f1) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}

.subtitle-text {
    margin: 0 !important;
    color: #cbd5e0 !important;
    font-size: 2.2rem !important;
    margin-top: 8px !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px !important;
}

/* UI Components (Buttons, Selectbox, etc) */
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

.stSelectbox > div {
    background-color: #1e293b !important;
    border: 2px solid #334155 !important;
    border-radius: 12px !important;
}

.stFileUploader > div {
    background: linear-gradient(135deg, #1a1f35 0%, #151b2b 100%) !important;
    border: 2px dashed #334155 !important;
    border-radius: 12px;
}

/* Status Messages */
.stSuccess {background: linear-gradient(135deg, #1f3a1f 0%, #1a2e1a 100%) !important; border: 2px solid #10b981 !important;}
.stError {background: linear-gradient(135deg, #3a1f1f 0%, #2e1a1a 100%) !important; border: 2px solid #ef4444 !important;}
.stInfo {background: linear-gradient(135deg, #1e3a5f 0%, #1a2340 100%) !important; border: 2px solid #3b82f6 !important;}

/* Hide Main Menu/Sidebars */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stSidebar"] {display: none;}
.stSidebar {display: none;}
</style>
""", unsafe_allow_html=True)

# --- STEP 4: HEADER HTML ---
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

# --- STEP 5: NAVIGATION ---
st.write("") # Small spacer
nav1, nav2 = st.columns([1.2, 1.2])
with nav1:
    if st.button("🏠 Home", key="nav_home", use_container_width=True):
        st.session_state.current_page = "Home"
        st.rerun()
with nav2:
    if st.button("ℹ️ About", key="nav_about", use_container_width=True):
        st.session_state.current_page = "About"
        st.rerun()

# --- STEP 6: PAGE CONTENT ---
if st.session_state.current_page == "Home":
    show_home_page()
else:
    show_about_page()