import streamlit as st
from config import THEMES, PAGES

def apply_theme(theme):
    if theme == "Dark":
        st.markdown(f"<style>.stApp {{background-color: {THEMES[theme]['background']}; color: {THEMES[theme]['color']};}}</style>", unsafe_allow_html=True)
    else:
        st.markdown(f"<style>.stApp {{background-color: {THEMES[theme]['background']}; color: {THEMES[theme]['color']};}}</style>", unsafe_allow_html=True)

def setup_sidebar():
    theme = st.sidebar.radio("🌗 Theme", list(THEMES.keys()))
    apply_theme(theme)

    st.sidebar.title("🩺 Navigation")
    page = st.sidebar.radio("Go to", PAGES)
    return page