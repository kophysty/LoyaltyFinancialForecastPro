import streamlit as st
from utils.presets import save_preset, PRESETS
from utils.translations import get_translation

def parameter_management_page():
    lang = st.session_state.get('language', 'ru')
    t = lambda key: get_translation(key, lang)
    
    st.title(t('parameter_management'))
    
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
        
        for key, value in preset_data.items():
            st.session_state[key] = value
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Базовые параметры:**")
            
            # Добавляем параметры кэшбэка и использования баллов
            st.session_state['cashback_rate'] = st.slider(
                "Процент кэшбэка",
                min_value=0.0,
                max_value=50.0,
                value=float(preset_data.get('cashback_rate', 0.15) * 100),
                format="%.1f%%",
                help="Процент кэшбэка от суммы покупки",
                key=f"cashback_{selected_preset}"
            ) / 100
            
            st.session_state['points_usage_rate'] = st.slider(
                "Использование баллов",
                min_value=0.0,
                max_value=100.0,
                value=float(preset_data.get('points_usage_rate', 0.70) * 100),
                format="%.1f%%",
                help="Процент использования начисленных баллов",
                key=f"points_usage_{selected_preset}"
            ) / 100
            
            st.session_state['initial_users'] = st.number_input(
                "Начальные пользователи",
                min_value=500,
                max_value=5000,
                value=preset_data.get('initial_users', 1000),
                step=100,
                key=f"init_users_{selected_preset}"
            )
            
            st.session_state['active_conversion'] = st.number_input(
                "Конверсия в активных",
                min_value=0.0,
                max_value=100.0,
                value=preset_data.get('active_conversion', 0.1) * 100,
                format="%.2f",
                help="Значение в процентах"
            ) / 100
            
            st.session_state['growth_rate_y1'] = st.number_input(
                "Рост 1й год",
                min_value=0.0,
                max_value=100.0,
                value=preset_data.get('growth_rate_y1', 0.2) * 100,
                format="%.2f",
                help="Значение в процентах"
            ) / 100
            
            st.session_state['growth_rate_y2'] = st.number_input(
                "Рост 2й год",
                min_value=0.0,
                max_value=100.0,
                value=preset_data.get('growth_rate_y2', 0.15) * 100,
                format="%.2f",
                help="Значение в процентах"
            ) / 100
            
            st.session_state['avg_check'] = st.number_input(
                "Средний чек (₽)",
                min_value=1000,
                max_value=10000,
                value=preset_data.get('avg_check', 2000),
                step=500,
                key=f"avg_check_{selected_preset}"
            )
            
        with col2:
            st.markdown("**Операционные параметры:**")
            st.session_state['initial_investment'] = st.number_input(
                "Начальные инвестиции (₽)",
                min_value=1000000,
                max_value=50000000,
                value=preset_data.get('initial_investment', 10000000),
                step=1000000,
                help="Объем начальных инвестиций"
            )
            
            st.session_state['base_infra_cost'] = st.number_input(
                "Базовая инфраструктура (₽)",
                min_value=100000,
                max_value=1000000,
                value=preset_data.get('base_infra_cost', 300000),
                step=50000,
                key=f"infra_{selected_preset}"
            )
            
            st.session_state['marketing_spend_rate'] = st.slider(
                "Затраты на маркетинг (% от дохода)",
                min_value=0.0,
                max_value=25.0,
                value=float(preset_data.get('marketing_spend_rate', 0.05) * 100),
                step=0.5,
                format="%.1f%%",
                help="Процент от дохода, направляемый на маркетинг",
                key=f"marketing_rate_{selected_preset}"
            ) / 100
            
            st.session_state['claim_period_months'] = st.number_input(
                "Период подтверждения баллов (месяцы)",
                min_value=1,
                max_value=12,
                value=preset_data.get('claim_period_months', 2),
                help="Количество месяцев, в течение которых пользователь должен подтвердить баллы"
            )
            
            st.session_state['marketing_efficiency'] = st.number_input(
                "Эффективность маркетинга (польз./100K)",
                min_value=10,
                max_value=500,
                value=preset_data.get('marketing_efficiency', 100),
                step=10,
                key=f"marketing_eff_{selected_preset}"
            )

        # Функция для получения текущих значений параметров
        def get_current_values():
            return {
                'initial_users': st.session_state['initial_users'],
                'active_conversion': st.session_state['active_conversion'],
                'growth_rate_y1': st.session_state['growth_rate_y1'],
                'growth_rate_y2': st.session_state['growth_rate_y2'],
                'avg_check': st.session_state['avg_check'],
                'cashback_rate': st.session_state['cashback_rate'],
                'points_usage_rate': st.session_state['points_usage_rate'],
                'exchange_commission_rate': st.session_state.get('exchange_commission_rate', 0.03),
                'reward_commission_rate': st.session_state.get('reward_commission_rate', 0.05),
                'base_infra_cost': st.session_state['base_infra_cost'],
                'marketing_spend_rate': st.session_state['marketing_spend_rate'],
                'marketing_efficiency': st.session_state['marketing_efficiency'],
                'ad_revenue_per_user': st.session_state.get('ad_revenue_per_user', 20),
                'partnership_rate': st.session_state.get('partnership_rate', 0.005)
            }

        st.divider()
        st.subheader("Сохранение сценария")
        
        col_save1, col_save2 = st.columns(2)
        
        with col_save1:
            if st.button("Сохранить изменения в текущий сценарий", key="save_current"):
                current_values = get_current_values()
                PRESETS[selected_preset] = current_values
                st.success(f"Изменения сохранены в сценарий {scenario_names[selected_preset]}")
        
        with col_save2:
            new_preset_name = st.text_input("Название нового сценария", key="new_preset_name")
            save_new = st.button("Сохранить как новый сценарий", key="save_new")
            if save_new:
                if new_preset_name:
                    current_values = get_current_values()
                    save_preset(new_preset_name, current_values)
                    st.success(f"Создан новый сценарий: {new_preset_name}")
                else:
                    st.warning("Введите название для нового сценария")

        

if __name__ == "__main__":
    parameter_management_page()