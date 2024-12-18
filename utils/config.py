import streamlit as st

def initialize_session_state():
    """Initialize missing session state variables with default values"""
    # Initialize only if no preset was loaded
    if 'initial_users' not in st.session_state:
        # Load standard preset as default
        from utils.presets import PRESETS
        preset_data = PRESETS['standard'].copy()
        
        # Убедимся, что все параметры подписок инициализированы
        subscription_params = [
            'basic_subscription_price', 'basic_subscription_start_month',
            'premium_subscription_price', 'premium_subscription_start_month',
            'business_subscription_price', 'business_subscription_start_month',
            'basic_subscription_conversion', 'premium_subscription_conversion'
        ]
        
        # Загружаем все параметры из пресета
        for key, value in preset_data.items():
            st.session_state[key] = value
            
        # Проверяем наличие всех параметров подписок
        for param in subscription_params:
            if param not in st.session_state and param in preset_data:
                st.session_state[param] = preset_data[param]
