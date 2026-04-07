import streamlit as st
from config import PAGE_CONFIG

# --- STEP 1: MUST BE THE FIRST ST COMMAND ---
st.set_page_config(**PAGE_CONFIG)

# --- STEP 2: NOW IMPORT OTHER FILES ---
from pages.home import show_home_page
from pages.about import show_about_page

# --- STEP 3: SESSION STATE ---
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# --- STEP 4: STYLING ---
st.markdown("""
<style>
    .stApp {background: #0f172a; color: white;}
    /* Your other CSS remains here */
</style>
""", unsafe_allow_html=True)

# --- STEP 5: HEADER ---
st.markdown("<h1 style='text-align: center;'>🛡️ Kawach</h1>", unsafe_allow_html=True)

# --- STEP 6: NAVIGATION ---
col1, col2 = st.columns(2)
with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.current_page = "Home"
        st.rerun()
with col2:
    if st.button("ℹ️ About", use_container_width=True):
        st.session_state.current_page = "About"
        st.rerun()

# --- STEP 7: ROUTING ---
if st.session_state.current_page == "Home":
    show_home_page()
else:
    show_about_page()