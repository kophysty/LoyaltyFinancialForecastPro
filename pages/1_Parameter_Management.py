import streamlit as st
from utils.presets import save_preset, PRESETS

from utils.translations import get_translation

def parameter_management_page():
    # Get current language from session state
    lang = st.session_state.get('language', 'ru')
    t = lambda key: get_translation(key, lang)
    
    st.title(t('parameter_management'))
    
    # Отображение предустановленных сценариев
    st.header(t('preset_scenarios'))
    scenario_names = {
        "pessimistic": "Пессимистичный",
        "standard": "Стандартный",
        "optimistic": "Оптимистичный"
    }
    
    selected_preset = st.selectbox(
        "Выберите сценарий для просмотра",
        options=list(scenario_names.keys()),
        format_func=lambda x: scenario_names[x]
    )
    
    if selected_preset:
        st.subheader(f"Параметры сценария: {scenario_names[selected_preset]}")
        
        # Отображение параметров выбранного сценария
        col1, col2 = st.columns(2)
        preset_data = PRESETS[selected_preset]
        
        with col1:
            st.markdown("**Базовые параметры:**")
            st.write(f"Начальные пользователи: {preset_data['initial_users']:,}")
            st.write(f"Конверсия в активных: {preset_data['active_conversion']:.1%}")
            st.write(f"Рост 1й год: {preset_data['growth_rate_y1']:.1%}")
            st.write(f"Рост 2й год: {preset_data['growth_rate_y2']:.1%}")
            st.write(f"Средний чек: {preset_data['avg_check']:,} ₽")
            st.write(f"Процент кэшбэка: {preset_data['cashback_percent']:.1%}")
            
        with col2:
            st.markdown("**Операционные параметры:**")
            st.write(f"ФОТ 1й год: {preset_data['burn_rate_fot_1']:,} ₽")
            st.write(f"ФОТ 2й год: {preset_data['burn_rate_fot_2']:,} ₽")
            st.write(f"Базовая инфраструктура: {preset_data['base_infra_cost']:,} ₽")
            st.write(f"Маркетинговый бюджет: {preset_data['monthly_marketing_budget']:,} ₽")
            st.write(f"Эффективность маркетинга: {preset_data['marketing_efficiency']} польз./100K")
        
        # Автоматически применяем выбранный сценарий
        for key, value in preset_data.items():
            if key not in st.session_state or st.session_state[key] != value:
                st.session_state[key] = value

        # Кнопка для сохранения изменений в текущий сценарий
        if selected_preset != "standard":  # Запрещаем изменение стандартного сценария
            if st.button(f"Сохранить изменения в сценарий {scenario_names[selected_preset]}"):
                current_values = {
                    'initial_users': st.session_state['initial_users'],
                    'active_conversion': st.session_state['active_conversion'],
                    'growth_rate_y1': st.session_state['growth_rate_y1'],
                    'growth_rate_y2': st.session_state['growth_rate_y2'],
                    'avg_check': st.session_state['avg_check'],
                    'cashback_percent': st.session_state['cashback_percent'],
                    'points_usage_rate': st.session_state['points_usage_rate'],
                    'exchange_commission_rate': st.session_state['exchange_commission_rate'],
                    'reward_commission_rate': st.session_state['reward_commission_rate'],
                    'burn_rate_fot_1': st.session_state['burn_rate_fot_1'],
                    'burn_rate_fot_2': st.session_state['burn_rate_fot_2'],
                    'base_infra_cost': st.session_state['base_infra_cost'],
                    'monthly_marketing_budget': st.session_state['monthly_marketing_budget'],
                    'marketing_efficiency': st.session_state['marketing_efficiency'],
                    'ad_revenue_per_user': st.session_state['ad_revenue_per_user'],
                    'partnership_rate': st.session_state['partnership_rate']
                }
                PRESETS[selected_preset] = current_values
                st.success(f"Изменения сохранены в сценарий {scenario_names[selected_preset]}")
    
    st.divider()
    
    st.subheader(t('revenue_params'))
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state['commission_rate'] = st.number_input(
            t('commission_rate_label'),
            min_value=0.0,
            max_value=1.0,
            value=st.session_state['commission_rate'],
            format="%.3f"
        )
        
        st.session_state['monthly_transaction_volume'] = st.number_input(
            t('monthly_volume'),
            min_value=0,
            value=int(st.session_state['monthly_transaction_volume'])
        )
        
        st.session_state['transaction_growth_rate'] = st.number_input(
            t('transaction_growth'),
            min_value=0.0,
            max_value=1.0,
            value=st.session_state['transaction_growth_rate'],
            format="%.3f"
        )
        
        st.session_state['initial_subscribers'] = st.number_input(
            "Initial Subscribers",
            min_value=0,
            value=st.session_state['initial_subscribers']
        )
    
    with col2:
        st.session_state['subscriber_growth_rate'] = st.number_input(
            "Subscriber Growth Rate",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state['subscriber_growth_rate'],
            format="%.3f"
        )
        
        st.session_state['subscription_price'] = st.number_input(
            "Subscription Price ($)",
            min_value=0.0,
            value=st.session_state['subscription_price'],
            format="%.2f"
        )
        
        st.session_state['base_ad_revenue'] = st.number_input(
            "Base Ad Revenue ($)",
            min_value=0,
            value=st.session_state['base_ad_revenue']
        )
        
        st.session_state['ad_revenue_growth_rate'] = st.number_input(
            "Ad Revenue Growth Rate",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state['ad_revenue_growth_rate'],
            format="%.3f"
        )
    
    st.subheader("Expense Parameters")
    col3, col4 = st.columns(2)
    
    with col3:
        st.session_state['base_payroll'] = st.number_input(
            "Base Monthly Payroll ($)",
            min_value=0,
            value=st.session_state['base_payroll']
        )
        
        st.session_state['payroll_growth_rate'] = st.number_input(
            "Payroll Growth Rate",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state['payroll_growth_rate'],
            format="%.3f"
        )
    
    with col4:
        st.session_state['base_marketing_spend'] = st.number_input(
            "Base Marketing Spend ($)",
            min_value=0,
            value=st.session_state['base_marketing_spend']
        )
        
        st.session_state['marketing_growth_rate'] = st.number_input(
            "Marketing Growth Rate",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state['marketing_growth_rate'],
            format="%.3f"
        )
    
    st.divider()
    st.subheader("Сохранить как новый сценарий")
    col_save1, col_save2 = st.columns(2)
    
    with col_save1:
        preset_name = st.text_input("Название нового сценария")
    
    with col_save2:
        if st.button("Сохранить как новый сценарий") and preset_name:
            current_values = {
                'initial_users': st.session_state['initial_users'],
                'active_conversion': st.session_state['active_conversion'],
                'growth_rate_y1': st.session_state['growth_rate_y1'],
                'growth_rate_y2': st.session_state['growth_rate_y2'],
                'avg_check': st.session_state['avg_check'],
                'cashback_percent': st.session_state['cashback_percent'],
                'points_usage_rate': st.session_state['points_usage_rate'],
                'exchange_commission_rate': st.session_state['exchange_commission_rate'],
                'reward_commission_rate': st.session_state['reward_commission_rate'],
                'burn_rate_fot_1': st.session_state['burn_rate_fot_1'],
                'burn_rate_fot_2': st.session_state['burn_rate_fot_2'],
                'base_infra_cost': st.session_state['base_infra_cost'],
                'monthly_marketing_budget': st.session_state['monthly_marketing_budget'],
                'marketing_efficiency': st.session_state['marketing_efficiency'],
                'ad_revenue_per_user': st.session_state['ad_revenue_per_user'],
                'partnership_rate': st.session_state['partnership_rate']
            }
            save_preset(preset_name, current_values)
            st.success(f"Новый сценарий '{preset_name}' успешно сохранен!")

if __name__ == "__main__":
    parameter_management_page()
