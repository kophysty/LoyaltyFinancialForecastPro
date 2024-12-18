import streamlit as st

def initialize_session_state():
    """Initialize missing session state variables with default values"""
    from utils.presets import PRESETS
    
    # Список всех параметров подписок
    subscription_params = [
        'basic_subscription_price', 'basic_subscription_start_month',
        'premium_subscription_price', 'premium_subscription_start_month',
        'business_subscription_price', 'business_subscription_start_month',
        'basic_subscription_conversion', 'premium_subscription_conversion'
    ]
    
    # Если состояние не инициализировано, загружаем стандартный пресет
    if 'initial_users' not in st.session_state:
        preset_data = PRESETS['standard'].copy()
        
        # Загружаем все параметры из пресета
        for key, value in preset_data.items():
            st.session_state[key] = value
        
        # Проверяем и устанавливаем параметры подписок
        for param in subscription_params:
            if param not in st.session_state:
                if param in preset_data:
                    st.session_state[param] = preset_data[param]
                    print(f"Initialized {param} = {preset_data[param]}")
    
    # Проверяем, что все необходимые параметры подписок присутствуют
    missing_params = [param for param in subscription_params if param not in st.session_state]
    if missing_params:
        print(f"Missing subscription parameters: {missing_params}")
        preset_data = PRESETS['standard'].copy()
        for param in missing_params:
            if param in preset_data:
                st.session_state[param] = preset_data[param]
                print(f"Fixed missing {param} = {preset_data[param]}")
