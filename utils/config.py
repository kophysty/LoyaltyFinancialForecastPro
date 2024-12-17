import streamlit as st

def initialize_session_state():
    """Initialize missing session state variables with default values"""
    if 'language' not in st.session_state:
        st.session_state['language'] = 'ru'
        
    # Базовые параметры, если они еще не установлены из пресетов
    defaults = {
        # Initial Investment and Financial Parameters
        'initial_investment': 10000000,
        'cashback_rate': 0.15,  # 15% кэшбэк
        'points_usage_rate': 0.70,  # 70% использования баллов
        'expired_points_rate': 0.05,  # 5% от неиспользованных баллов становятся доходом
        
        # Revenue Parameters
        'ad_revenue_per_user': 20,
        'partnership_rate': 0.005,
        
        # Marketing and Operations
        'marketing_budget_fixed': 200000,  # Фиксированный бюджет на первые 6 месяцев
        'marketing_budget_rate': 0.05,  # 5% от выручки после 6 месяцев
        'initial_fot': 0  # Начальный ФОТ (первые 6 месяцев)
    }
    
    # Only initialize variables that are not already set
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
