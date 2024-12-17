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
        'cashback_rate': 0.15,  # 15% кэшбэка
        'points_usage_rate': 0.70,  # 70% использования баллов
        'expired_points_rate': 0.05,  # 5% от неиспользованных баллов (30%) становятся доходом
        'exchange_commission_rate': 0.03,
        'reward_commission_rate': 0.05,
        
        # Expenses
        'base_infra_cost': 200000,
        'marketing_spend_rate': 0.05,  # 5% от дохода
        'marketing_efficiency': 100,
        
        # Additional Revenue
        'ad_revenue_per_user': 20,
        'partnership_rate': 0.005
    }
    
    # Initialize all variables in session state
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
