import streamlit as st
from config.settings import PAGE_CONFIG
from styles.custom_css import get_custom_css
from components.auth import render_auth_page
from components.sidebar import render_sidebar
from pages.form_input import render_form_input
from pages.dashboard import render_dashboard
from utils.state_manager import initialize_session_state

def main():
    """Main application entry point"""
    # Set page configuration
    st.set_page_config(**PAGE_CONFIG)
    
    # Apply custom CSS
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    # Handle authentication
    if not st.session_state.authenticated:
        render_auth_page()
    else:
        # Render main application
        render_main_app()

def render_main_app():
    """Render main application after authentication"""
    # Render sidebar navigation
    render_sidebar()
    
    # Initialize current page if not set
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Form Input'
    
    # Route to appropriate page
    if st.session_state.current_page == 'Form Input':
        render_form_input()
    elif st.session_state.current_page == 'Dashboard':
        render_dashboard()
    else:
        # Default to form input if unknown page
        st.session_state.current_page = 'Form Input'
        render_form_input()

if __name__ == "__main__":
    main()