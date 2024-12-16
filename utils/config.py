import streamlit as st

def initialize_session_state():
    """Initialize all session state variables with default values"""
    if 'language' not in st.session_state:
        st.session_state['language'] = 'ru'
    defaults = {
        # Initial Investment
        'initial_investment': 10000000,
        
        # Base Parameters
        'initial_users': 1000,
        'active_conversion': 0.4,
        'growth_rate_y1': 0.30,
        'growth_rate_y2': 0.15,
        'avg_check': 3000,
        'exchange_commission_rate': 0.03,
        'reward_commission_rate': 0.05,
        
        # Expenses
        'burn_rate_fot_1': 2500000,
        'burn_rate_fot_2': 3500000,
        'base_infra_cost': 200000,
        'monthly_marketing_budget': 200000,
        'marketing_efficiency': 100,
        
        # Additional Revenue
        'ad_revenue_per_user': 20,
        'partnership_rate': 0.005
    }
    
    # Initialize all variables in session state
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
