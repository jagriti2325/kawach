import streamlit as st
from config import PAGE_CONFIG
from pages.home import show_home_page
from pages.about import show_about_page

# Set page config
st.set_page_config(**PAGE_CONFIG)

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# Top header styling
st.markdown("""
<style>
* {font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}
body, html {margin: 0; padding: 0;}

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
    font-size: 9.5rem !important;
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

.navbar {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 12px;
    background: linear-gradient(95deg, #f8fafc, #ffffff);
    padding: 14px 40px;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
    border-bottom: 1px solid #e2e8f0;
    margin-bottom: 28px;
}

.nav-button {
    background: #ffffff;
    color: #334155;
    border: 2px solid #e2e8f0;
    padding: 12px 24px;
    border-radius: 12px;
    cursor: pointer;
    font-size: 0.95rem;
    font-weight: 600;
    min-height: 48px;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 8px;
}

.nav-button:hover {
    background: #38bdf8;
    color: #ffffff;
    border-color: #38bdf8;
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(56, 189, 248, 0.3);
}

.field-label, .theme-label {
    color: #1e293b;
    font-weight: 700;
    margin-bottom: 12px;
    display: block;
    font-size: 1.05rem;
    letter-spacing: 0.3px;
}

.stSelectbox {
    margin-bottom: 16px;
}

.stSelectbox > div {
    background-color: #f8fafc !important;
    border-radius: 12px !important;
    border: 2px solid #e2e8f0 !important;
    transition: all 0.3s ease !important;
}

.stSelectbox > div:hover {
    border-color: #38bdf8 !important;
    box-shadow: 0 4px 12px rgba(56, 189, 248, 0.1) !important;
}

.stFileUploader > div {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    border: 2px dashed #cbd5e0;
    border-radius: 12px;
    padding: 24px !important;
    transition: all 0.3s ease;
}

.stFileUploader > div:hover {
    border-color: #38bdf8;
    background: linear-gradient(135deg, #f0f9ff 0%, #f0fdf4 100%);
}

.stButton > button {
    background: linear-gradient(135deg, #38bdf8, #06b6d4) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 28px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(56, 189, 248, 0.4) !important;
}

.stSuccess {
    background: linear-gradient(135deg, #ecfdf5 10%, #dbeafe 90%) !important;
    border: 2px solid #10b981 !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

.stError {
    background: linear-gradient(135deg, #fef2f2 10%, #fee2e2 90%) !important;
    border: 2px solid #ef4444 !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

.stWarning {
    background: linear-gradient(135deg, #fffbeb 10%, #fef3c7 90%) !important;
    border: 2px solid #f59e0b !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

.stInfo {
    background: linear-gradient(135deg, #eff6ff 10%, #dbeafe 90%) !important;
    border: 2px solid #3b82f6 !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stSidebar"] {display: none;}
.stSidebar {display: none;}
</style>
""", unsafe_allow_html=True)

# Title block
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

# Navbar below title (single Streamlit navigation row)
nav1, nav2 = st.columns([1.2, 1.2])
with nav1:
    if st.button("🏠 Home", key="nav_home", use_container_width=True):
        st.session_state.current_page = "Home"
        st.rerun()
with nav2:
    if st.button("ℹ️ About", key="nav_about", use_container_width=True):
        st.session_state.current_page = "About"
        st.rerun()

# Apply dark mode styling
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg, #0f172a 0%, #1a1f35 100%); color: white;}
.stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, label, span, div, button, a, li, ul, ol {color: #e2e8f0 !important;}
    .stButton button {color: white !important; background: linear-gradient(135deg, #3b82f6, #06b6d4) !important; border: none !important; border-radius: 12px !important; padding: 12px 28px !important; font-weight: 600 !important;}
    .stButton button:hover {background: linear-gradient(135deg, #2563eb, #0891b2) !important; transform: translateY(-2px) !important; box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4) !important;}
    .stSelectbox {margin-bottom: 16px;}
    .stSelectbox > div {background-color: #1e293b !important; border: 2px solid #334155 !important; border-radius: 12px !important;}
    .stSelectbox > div:hover {border-color: #3b82f6 !important; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2) !important;}
    .stSelectbox select, .stSelectbox select option {background-color: #1e293b !important; color: #e2e8f0 !important;}
    .stSelectbox div[data-baseweb="select"], .stSelectbox [role="option"], .stSelectbox [role="listbox"] {background-color: #1e293b !important; color: #e2e8f0 !important;}
    .stTextInput input, .stNumberInput input {background-color: #1a1f35 !important; color: #e2e8f0 !important; border: 2px solid #334155 !important; border-radius: 12px !important;}
    .stTextInput input:focus, .stNumberInput input:focus {border-color: #3b82f6 !important; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;}
    .stFileUploader > div {background: linear-gradient(135deg, #1a1f35 0%, #151b2b 100%) !important; border: 2px dashed #334155 !important; border-radius: 12px !important; padding: 24px !important;}
    .stFileUploader > div:hover {border-color: #3b82f6 !important; background: linear-gradient(135deg, #1e293b 0%, #1a1f35 100%) !important;}
    .stFileUploader label, .stFileUploader div, .stFileUploader span, .stFileUploader [role="button"], .stFileUploader button, .stFileUploader a {color: #e2e8f0 !important;}
    .stFileUploader input {background-color: #1a1f35 !important; color: #e2e8f0 !important;}
    .stInfo, .stSuccess, .stWarning, .stError {border-radius: 12px !important; padding: 16px !important;}
    .stInfo {background: linear-gradient(135deg, #1e3a5f 0%, #1a2340 100%) !important; border: 2px solid #3b82f6 !important; color: #93c5fd !important;}
    .stSuccess {background: linear-gradient(135deg, #1f3a1f 0%, #1a2e1a 100%) !important; border: 2px solid #10b981 !important; color: #86efac !important;}
    .stWarning {background: linear-gradient(135deg, #3a2a1f 0%, #2e251a 100%) !important; border: 2px solid #f59e0b !important; color: #fcd34d !important;}
    .stError {background: linear-gradient(135deg, #3a1f1f 0%, #2e1a1a 100%) !important; border: 2px solid #ef4444 !important; color: #fca5a5 !important;}
    .stTable th, .stTable td {color: #e2e8f0 !important;}
    .stSubheader {color: #cbd5e0 !important;}
    input::placeholder, textarea::placeholder {color: #64748b !important;}
    </style>
    """, unsafe_allow_html=True)

# Page content
if st.session_state.current_page == "Home":
    show_home_page()
else:
    show_about_page()