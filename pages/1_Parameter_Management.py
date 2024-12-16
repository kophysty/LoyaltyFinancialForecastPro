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
        preset_data = PRESETS[selected_preset]
        
        # Автоматически применяем выбранный сценарий ко всем полям
        for key, value in preset_data.items():
            st.session_state[key] = value
        
        # Отображение и редактирование параметров
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Базовые параметры:**")
            st.session_state['initial_users'] = st.number_input(
                "Начальные пользователи",
                min_value=500,
                max_value=5000,
                value=preset_data['initial_users'],
                step=100,
                key=f"init_users_{selected_preset}"
            )
            
            st.session_state['active_conversion'] = st.number_input(
                "Конверсия в активных",
                min_value=0.0,
                max_value=1.0,
                value=preset_data['active_conversion'] * 100,
                format="%.2f",
                help="Значение в процентах"
            ) / 100
            
            st.session_state['growth_rate_y1'] = st.number_input(
                "Рост 1й год",
                min_value=0.0,
                max_value=100.0,
                value=preset_data['growth_rate_y1'] * 100,
                format="%.2f",
                help="Значение в процентах"
            ) / 100
            
            st.session_state['growth_rate_y2'] = st.number_input(
                "Рост 2й год",
                min_value=0.0,
                max_value=100.0,
                value=preset_data['growth_rate_y2'] * 100,
                format="%.2f",
                help="Значение в процентах"
            ) / 100
            
            st.session_state['avg_check'] = st.number_input(
                "Средний чек (₽)",
                min_value=1000,
                max_value=10000,
                value=preset_data['avg_check'],
                step=500,
                key=f"avg_check_{selected_preset}"
            )
            
            st.session_state['cashback_percent'] = st.number_input(
                "Процент кэшбэка",
                min_value=0.0,
                max_value=100.0,
                value=preset_data['cashback_percent'] * 100,
                format="%.2f",
                help="Значение в процентах"
            ) / 100
            
        with col2:
            st.markdown("**Операционные параметры:**")
            st.session_state['burn_rate_fot_1'] = st.number_input(
                "ФОТ 1й год (₽)",
                min_value=1000000,
                max_value=5000000,
                value=preset_data['burn_rate_fot_1'],
                step=100000,
                key=f"fot_1_{selected_preset}"
            )
            
            st.session_state['burn_rate_fot_2'] = st.number_input(
                "ФОТ 2й год (₽)",
                min_value=1000000,
                max_value=7000000,
                value=preset_data['burn_rate_fot_2'],
                step=100000,
                key=f"fot_2_{selected_preset}"
            )
            
            st.session_state['base_infra_cost'] = st.number_input(
                "Базовая инфраструктура (₽)",
                min_value=100000,
                max_value=1000000,
                value=preset_data['base_infra_cost'],
                step=50000,
                key=f"infra_{selected_preset}"
            )
            
            st.session_state['monthly_marketing_budget'] = st.number_input(
                "Маркетинговый бюджет (₽)",
                min_value=100000,
                max_value=5000000,
                value=preset_data['monthly_marketing_budget'],
                step=100000,
                key=f"marketing_{selected_preset}"
            )
            
            st.session_state['marketing_efficiency'] = st.number_input(
                "Эффективность маркетинга (польз./100K)",
                min_value=10,
                max_value=500,
                value=preset_data['marketing_efficiency'],
                step=10,
                key=f"marketing_eff_{selected_preset}"
            )

        # Кнопки для сохранения изменений
        col_save1, col_save2 = st.columns(2)
        
        with col_save1:
            if selected_preset != "standard":  # Запрещаем изменение стандартного сценария
                if st.button(f"Сохранить изменения в сценарий {scenario_names[selected_preset]}", key=f"save_{selected_preset}"):
                    current_values = {
                        'initial_users': st.session_state['initial_users'],
                        'active_conversion': st.session_state['active_conversion'],
                        'growth_rate_y1': st.session_state['growth_rate_y1'],
                        'growth_rate_y2': st.session_state['growth_rate_y2'],
                        'avg_check': st.session_state['avg_check'],
                        'cashback_percent': st.session_state['cashback_percent'],
                        'points_usage_rate': st.session_state.get('points_usage_rate', 0.7),
                        'exchange_commission_rate': st.session_state.get('exchange_commission_rate', 0.03),
                        'reward_commission_rate': st.session_state.get('reward_commission_rate', 0.05),
                        'burn_rate_fot_1': st.session_state['burn_rate_fot_1'],
                        'burn_rate_fot_2': st.session_state['burn_rate_fot_2'],
                        'base_infra_cost': st.session_state['base_infra_cost'],
                        'monthly_marketing_budget': st.session_state['monthly_marketing_budget'],
                        'marketing_efficiency': st.session_state['marketing_efficiency'],
                        'ad_revenue_per_user': st.session_state.get('ad_revenue_per_user', 20),
                        'partnership_rate': st.session_state.get('partnership_rate', 0.005)
                    }
                    PRESETS[selected_preset] = current_values
                    st.success(f"Изменения сохранены в сценарий {scenario_names[selected_preset]}")
        
        with col_save2:
            new_preset_name = st.text_input("Сохранить как новый сценарий", key=f"new_name_{selected_preset}")
            if st.button("Сохранить копию", key=f"save_copy_{selected_preset}"):
                if new_preset_name:
                    current_values = {
                        'initial_users': st.session_state['initial_users'],
                        'active_conversion': st.session_state['active_conversion'],
                        'growth_rate_y1': st.session_state['growth_rate_y1'],
                        'growth_rate_y2': st.session_state['growth_rate_y2'],
                        'avg_check': st.session_state['avg_check'],
                        'cashback_percent': st.session_state['cashback_percent'],
                        'points_usage_rate': st.session_state.get('points_usage_rate', 0.7),
                        'exchange_commission_rate': st.session_state.get('exchange_commission_rate', 0.03),
                        'reward_commission_rate': st.session_state.get('reward_commission_rate', 0.05),
                        'burn_rate_fot_1': st.session_state['burn_rate_fot_1'],
                        'burn_rate_fot_2': st.session_state['burn_rate_fot_2'],
                        'base_infra_cost': st.session_state['base_infra_cost'],
                        'monthly_marketing_budget': st.session_state['monthly_marketing_budget'],
                        'marketing_efficiency': st.session_state['marketing_efficiency'],
                        'ad_revenue_per_user': st.session_state.get('ad_revenue_per_user', 20),
                        'partnership_rate': st.session_state.get('partnership_rate', 0.005)
                    }
                    save_preset(new_preset_name, current_values)
                    st.success(f"Создан новый сценарий: {new_preset_name}")
                else:
                    st.warning("Введите название для нового сценария")
    
    st.divider()
    
    st.subheader(t('revenue_params'))
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state['commission_rate'] = st.number_input(
            t('commission_rate_label'),
            min_value=0.0,
            max_value=100.0,
            value=st.session_state['commission_rate'] * 100,
            format="%.1f",
            help="Значение в процентах"
        ) / 100
        
        st.session_state['monthly_transaction_volume'] = st.number_input(
            t('monthly_volume'),
            min_value=0,
            value=int(st.session_state['monthly_transaction_volume'])
        )
        
        st.session_state['transaction_growth_rate'] = st.number_input(
            t('transaction_growth'),
            min_value=0.0,
            max_value=100.0,
            value=st.session_state['transaction_growth_rate'] * 100,
            format="%.1f",
            help="Значение в процентах"
        ) / 100
        
        st.session_state['initial_subscribers'] = st.number_input(
            "Initial Subscribers",
            min_value=0,
            value=st.session_state['initial_subscribers']
        )
    
    with col2:
        st.session_state['subscriber_growth_rate'] = st.number_input(
            "Темп роста подписчиков",
            min_value=0.0,
            max_value=100.0,
            value=st.session_state['subscriber_growth_rate'] * 100,
            format="%.1f",
            help="Значение в процентах"
        ) / 100
        
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
            "Темп роста рекламных доходов",
            min_value=0.0,
            max_value=100.0,
            value=st.session_state['ad_revenue_growth_rate'] * 100,
            format="%.1f",
            help="Значение в процентах"
        ) / 100
    
    st.subheader("Expense Parameters")
    col3, col4 = st.columns(2)
    
    with col3:
        st.session_state['base_payroll'] = st.number_input(
            "Base Monthly Payroll ($)",
            min_value=0,
            value=st.session_state['base_payroll']
        )
        
        st.session_state['payroll_growth_rate'] = st.number_input(
            "Темп роста ФОТ",
            min_value=0.0,
            max_value=100.0,
            value=st.session_state['payroll_growth_rate'] * 100,
            format="%.1f",
            help="Значение в процентах"
        ) / 100
    
    with col4:
        st.session_state['base_marketing_spend'] = st.number_input(
            "Base Marketing Spend ($)",
            min_value=0,
            value=st.session_state['base_marketing_spend']
        )
        
        st.session_state['marketing_growth_rate'] = st.number_input(
            "Темп роста маркетингового бюджета",
            min_value=0.0,
            max_value=100.0,
            value=st.session_state['marketing_growth_rate'] * 100,
            format="%.1f",
            help="Значение в процентах"
        ) / 100
    
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