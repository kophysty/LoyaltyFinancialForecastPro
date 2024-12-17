import streamlit as st

def initialize_session_state():
    """Initialize missing session state variables with default values"""
    if 'language' not in st.session_state:
        st.session_state['language'] = 'ru'
    defaults = {
        # Initial Investment
        'initial_investment': 10000000,
        
        # Additional parameters that might not be in presets
        'expired_points_rate': 0.05,  # 5% от неиспользованных баллов (30%) становятся доходом
        'ad_revenue_per_user': 20,
        'partnership_rate': 0.005
    }
    
    # Only initialize variables that are not already set
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
