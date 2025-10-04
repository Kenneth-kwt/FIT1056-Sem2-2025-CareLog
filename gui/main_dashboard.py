# gui/main_dashboard.py
import streamlit as st
from app.log import logManager

def launch():
    """Sets up the main Streamlit application window and navigation."""
    st.set_page_config(layout="wide", page_title="CareLog System")