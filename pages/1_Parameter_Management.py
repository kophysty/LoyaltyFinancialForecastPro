import streamlit as st
import json
from utils.presets import save_preset, delete_custom_preset, is_custom_preset, PRESETS
from utils.translations import get_translation

def parameter_management_page():
    lang = st.session_state.get('language', 'ru')
    t = lambda key: get_translation(key, lang)
    
    st.title(t('parameter_management'))
    
    st.header(t('preset_scenarios'))
    
    # Загружаем пользовательские сценарии
    try:
        with open('custom_presets.json', 'r') as f:
            custom_presets = json.load(f)
    except FileNotFoundError:
        custom_presets = {}
    
    # Объединяем стандартные и пользовательские сценарии
    scenario_names = {
        "standard": "Стандартный",
        "pessimistic": "Пессимистичный",
        "optimistic": "Оптимистичный",
        **{name: f"Пользовательский: {name}" for name in custom_presets.keys()}
    }
    
    col_select, col_delete = st.columns([3, 1])
        
    with col_select:
        selected_preset = st.selectbox(
            "Выберите сценарий для просмотра",
            options=list(scenario_names.keys()),
            format_func=lambda x: scenario_names[x],
            index=list(scenario_names.keys()).index("standard")  # Устанавливаем "Стандартный" по умолчанию
        )
    
    with col_delete:
        if is_custom_preset(selected_preset):
            if st.button("🗑️ Удалить сценарий", type="secondary", help="Удалить пользовательский сценарий"):
                if delete_custom_preset(selected_preset):
                    st.success(f"Сценарий '{selected_preset}' успешно удален")
                    st.session_state['current_scenario'] = 'standard'  # Возвращаемся к стандартному сценарию
                    st.rerun()
                else:
                    st.error("Не удалось удалить сценарий")
    
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

            st.markdown("**Управление доходами:**")
            st.session_state['premium_business_start_month'] = st.number_input(
                "Месяц начала подписок Премиум Бизнес",
                min_value=1,
                max_value=24,
                value=preset_data.get('premium_business_start_month', 13),
                step=1,
                help="В каком месяце начнут действовать подписки Премиум Бизнес"
            )
            
            st.session_state['premium_business_rate'] = st.slider(
                "Процент партнеров на премиум-тарифе",
                min_value=0.0,
                max_value=100.0,
                value=float(preset_data.get('premium_business_rate', 0.3) * 100),
                format="%.1f%%",
                help="Процент партнеров, которые приобретают премиум-подписку",
                key=f"premium_business_rate_{selected_preset}"
            ) / 100
            
            st.session_state['premium_business_price'] = st.number_input(
                "Стоимость Премиум Бизнес (₽)",
                min_value=1000,
                max_value=20000,
                value=preset_data.get('premium_business_price', 8000),
                step=1000,
                help="Стоимость премиум-подписки для бизнеса"
            )

            st.session_state['premium_user_start_month'] = st.number_input(
                "Месяц начала подписок Премиум Пользователи",
                min_value=1,
                max_value=24,
                value=preset_data.get('premium_user_start_month', 13),
                step=1,
                help="В каком месяце начнут действовать премиум-подписки для пользователей"
            )
            
            st.session_state['premium_user_price'] = st.number_input(
                "Стоимость премиум-подписки для пользователей (₽)",
                min_value=100,
                max_value=5000,
                value=preset_data.get('premium_user_price', 299),
                step=100,
                help="Месячная стоимость премиум-подписки для обычных пользователей"
            )

            st.session_state['ad_start_month'] = st.number_input(
                "Месяц начала показа рекламы",
                min_value=1,
                max_value=24,
                value=preset_data.get('ad_start_month', 13),
                step=1,
                help="В каком месяце начнётся показ рекламы"
            )
            
            st.session_state['ad_revenue_per_user'] = st.number_input(
                "Доход с пользователя от рекламы (₽)",
                min_value=0,
                max_value=100,
                value=preset_data.get('ad_revenue_per_user', 20),
                step=5,
                help="Сколько в среднем приносит один пользователь от рекламы в месяц"
            )
            
        with col2:
            st.markdown("**Операционные параметры:**")
            st.session_state['initial_investment'] = st.number_input(
                "Начальные инвестиции (₽)",
                min_value=1000000,
                max_value=50000000,
                value=preset_data.get('initial_investment', 10000000),
                step=1000000,
                help="Объем начальных инвестиций на запуск проекта"
            )
            
            st.session_state['preparatory_expenses'] = st.number_input(
                "Расходы на подготовительный этап (₽)",
                min_value=1000000,
                max_value=30000000,
                value=preset_data.get('preparatory_expenses', 21000000),
                step=1000000,
                help="Расходы на подготовительный этап перед запуском (~$300K)"
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
            
            st.session_state['expired_points_rate'] = st.slider(
                "Процент сгорающих баллов",
                min_value=0.0,
                max_value=100.0,
                value=float(preset_data.get('expired_points_rate', 0.07) * 100),
                format="%.1f%%",
                help="Процент неподтвержденных баллов, которые сгорают после периода подтверждения",
                key=f"expired_points_{selected_preset}"
            ) / 100
            
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
                'expired_points_rate': st.session_state['expired_points_rate'],
                'exchange_commission_rate': st.session_state.get('exchange_commission_rate', 0.03),
                'reward_commission_rate': st.session_state.get('reward_commission_rate', 0.05),
                'base_infra_cost': st.session_state['base_infra_cost'],
                'marketing_spend_rate': st.session_state['marketing_spend_rate'],
                'marketing_efficiency': st.session_state['marketing_efficiency'],
                'ad_revenue_per_user': st.session_state.get('ad_revenue_per_user', 20),
                'partnership_rate': st.session_state.get('partnership_rate', 0.005),
                'initial_investment': st.session_state['initial_investment'],
                'preparatory_expenses': st.session_state['preparatory_expenses'],
                'claim_period_months': st.session_state['claim_period_months'],
                'premium_business_start_month': st.session_state['premium_business_start_month'],
                'premium_business_rate': st.session_state['premium_business_rate'],
                'premium_business_price': st.session_state['premium_business_price'],
                'premium_user_start_month': st.session_state['premium_user_start_month'],
                'premium_user_price': st.session_state['premium_user_price'],
                'ad_start_month': st.session_state['ad_start_month'],
                'ad_revenue_per_user': st.session_state['ad_revenue_per_user'],
                'premium_user_price': st.session_state['premium_user_price']
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

        st.divider()
        st.subheader("Восстановление значений по умолчанию")
        
        # Кнопка для восстановления значений по умолчанию
        if st.button("Восстановить значения по умолчанию для всех сценариев", type="primary"):
            # Восстанавливаем стандартные значения для всех сценариев
            PRESETS["standard"] = {
                "initial_users": 1000,
                "active_conversion": 0.30,
                "claim_period_months": 2,
                "growth_rate_y1": 0.25,  # Согласно требованиям
                "growth_rate_y2": 0.15,
                "avg_check": 2800,
                "points_usage_rate": 0.55,
                "cashback_rate": 0.12,
                "expired_points_rate": 0.07,
                "exchange_commission_rate": 0.03,
                "reward_commission_rate": 0.04,
                "base_infra_cost": 200000,
                "marketing_efficiency": 200,
                "marketing_spend_rate": 0.15,  # Согласно требованиям
                "ad_revenue_per_user": 20,
                "partnership_rate": 0.005,
                "burn_rate_fot_1": 2500000,
                "burn_rate_fot_2": 3500000,
                "premium_business_start_month": 8,  # Согласно требованиям
                "premium_user_start_month": 13,
                "ad_start_month": 8,  # Согласно требованиям
                "premium_business_rate": 0.30,
                "premium_business_price": 8000,
                "premium_user_price": 299,
                "premium_user_price": 299
            }
            
            PRESETS["pessimistic"] = {
                **PRESETS["standard"],
                "initial_users": 800,
                "active_conversion": 0.25,
                "growth_rate_y1": 0.20,
                "growth_rate_y2": 0.10,
                "avg_check": 2500,
                "points_usage_rate": 0.50,
                "exchange_commission_rate": 0.02,
                "reward_commission_rate": 0.03,
                "base_infra_cost": 250000,
                "marketing_efficiency": 150,
                "ad_revenue_per_user": 15,
                "partnership_rate": 0.003,
                "burn_rate_fot_1": 2500000,
                "burn_rate_fot_2": 3000000,
                "premium_business_rate": 0.20,
                "premium_user_price": 299
            }
            
            PRESETS["optimistic"] = {
                **PRESETS["standard"],
                "initial_users": 1200,
                "active_conversion": 0.35,
                "growth_rate_y1": 0.30,
                "growth_rate_y2": 0.20,
                "avg_check": 3200,
                "points_usage_rate": 0.60,
                "exchange_commission_rate": 0.04,
                "reward_commission_rate": 0.05,
                "base_infra_cost": 180000,
                "marketing_efficiency": 250,
                "ad_revenue_per_user": 25,
                "partnership_rate": 0.007,
                "burn_rate_fot_1": 2000000,
                "burn_rate_fot_2": 3000000,
                "premium_business_rate": 0.40,
                "premium_user_price": 299
            }
            
            # Перезагружаем страницу для применения изменений
            st.success("Значения по умолчанию восстановлены!")
            st.rerun()

        

if __name__ == "__main__":
    parameter_management_page()