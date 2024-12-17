import streamlit as st

def initialize_session_state():
    """Initialize missing session state variables with default values"""
    # Initialize only if no preset was loaded
    if 'initial_users' not in st.session_state:
        # Load standard preset as default
        from utils.presets import PRESETS
        preset_data = PRESETS['standard'].copy()
        for key, value in preset_data.items():
            st.session_state[key] = value
