import streamlit as st
import json
from utils.logging_config import log_info, log_warning, log_error

PRESETS = {
    "pessimistic": {
        "initial_users": 800,
        "active_conversion": 0.3,
        "growth_rate_y1": 0.15,
        "growth_rate_y2": 0.1,
        "avg_check": 2500,
        "points_usage_rate": 0.60,
        "cashback_rate": 0.15,
        "expired_points_rate": 0.03,
        "exchange_commission_rate": 0.02,
        "reward_commission_rate": 0.03,
        "burn_rate_fot_1": 2500000,
        "burn_rate_fot_2": 3000000,
        "base_infra_cost": 250000,
        "marketing_efficiency": 150,
        "marketing_spend_rate": 0.2,
        "ad_revenue_per_user": 15,
        "partnership_rate": 0.003,
        "claim_period_months": 2,
        # Параметры подписок для пессимистичного сценария
        "basic_subscription_price": 299,
        "basic_subscription_start_month": 8,
        "premium_subscription_price": 999,
        "premium_subscription_start_month": 12,
        "business_subscription_price": 4999,
        "business_subscription_start_month": 15,
        "basic_subscription_conversion": 0.03,
        "premium_subscription_conversion": 0.01,
        # Добавляем параметр initial_investment для согласованности
        "initial_investment": 60000000,
        "preparatory_expenses": 35000000
    },
    "standard": {
        "initial_users": 1000,
        "active_conversion": 0.30,  # Более реалистичная конверсия
        "claim_period_months": 2,  # Период для подтверждения баллов в месяцах
        "growth_rate_y1": 0.20,  # Сохраняем для инновационного продукта
        "growth_rate_y2": 0.15,  # Повышаем т.к. будет эффект сетевой ценности
        "avg_check": 2800,  # Немного консервативнее
        "points_usage_rate": 0.55,  # Более реалистичное использование
        "cashback_rate": 0.12,  # Оптимизированный кэшбэк
        "expired_points_rate": 0.07,  # Больше баллов будет сгорать
        "exchange_commission_rate": 0.03,
        "reward_commission_rate": 0.04,  # Немного снижаем
        "base_infra_cost": 200000,
        "marketing_efficiency": 200,
        "marketing_spend_rate": 0.1,
        "ad_revenue_per_user": 20,
        "partnership_rate": 0.005,
        "burn_rate_fot_1": 2500000,
        "burn_rate_fot_2": 3500000,
        "marketing_budget_fixed": 200000,
        "marketing_budget_rate": 0.05,
        "initial_fot": 0,
        # Параметры подписок
        "basic_subscription_price": 299,
        "basic_subscription_start_month": 6,  # Обновлено
        "premium_subscription_price": 999,
        "premium_subscription_start_month": 12,  # Обновлено
        "business_subscription_price": 4999,
        "business_subscription_start_month": 12,  # Обновлено
        "basic_subscription_conversion": 0.05,
        "premium_subscription_conversion": 0.02
    },
    "optimistic": {
        "initial_users": 1200,
        "active_conversion": 0.45,
        "growth_rate_y1": 0.25,
        "growth_rate_y2": 0.15,
        "avg_check": 3200,
        "points_usage_rate": 0.65,
        "cashback_rate": 0.17,
        "expired_points_rate": 0.07,  # Оптимистичный сценарий: больше баллов сгорает
        "exchange_commission_rate": 0.04,
        "reward_commission_rate": 0.06,
        "burn_rate_fot_1": 2000000,
        "burn_rate_fot_2": 3000000,
        "base_infra_cost": 180000,
        "marketing_efficiency": 200,
        "marketing_spend_rate": 0.05,
        "ad_revenue_per_user": 25,
        "partnership_rate": 0.007
    }
}


def load_preset(preset_name):
    """Load a preset and ensure all parameters are properly set"""
    if preset_name in PRESETS:
        try:
            log_info(f"Loading preset: {preset_name}")
            preset_data = PRESETS[preset_name].copy()
            
            # Список всех параметров для отслеживания
            all_params = [
                # Базовые параметры
                'initial_users', 'active_conversion', 'growth_rate_y1', 'growth_rate_y2',
                'avg_check', 'points_usage_rate', 'cashback_rate', 'expired_points_rate',
                'exchange_commission_rate', 'reward_commission_rate', 'base_infra_cost',
                'marketing_efficiency', 'marketing_spend_rate', 'initial_investment',
                'preparatory_expenses', 'claim_period_months',
                # Параметры подписок
                'basic_subscription_price', 'basic_subscription_start_month',
                'premium_subscription_price', 'premium_subscription_start_month',
                'business_subscription_price', 'business_subscription_start_month',
                'basic_subscription_conversion', 'premium_subscription_conversion'
            ]
            
            # Очищаем все параметры из session_state
            for param in all_params:
                if param in st.session_state:
                    del st.session_state[param]
                    log_info(f"Cleared {param} from session state")
            
            # Загружаем все параметры из пресета
            for param in all_params:
                if param in preset_data:
                    st.session_state[param] = preset_data[param]
                    log_info(f"Set {param} = {preset_data[param]}")
                else:
                    log_warning(f"Missing parameter in preset: {param}")
            
            # Проверяем критические параметры подписок
            subscription_starts = [
                'basic_subscription_start_month',
                'premium_subscription_start_month',
                'business_subscription_start_month'
            ]
            
            for param in subscription_starts:
                if param in st.session_state:
                    log_info(f"Subscription parameter loaded: {param} = {st.session_state[param]}")
                else:
                    log_error(f"Critical subscription parameter missing: {param}")
            
            log_info(f"Finished loading preset {preset_name}")
            return True
            
        except Exception as e:
            log_error(f"Error loading preset {preset_name}: {str(e)}")
            return False


def save_preset(preset_name, values):
    global PRESETS
    try:
        if preset_name in ["pessimistic", "standard", "optimistic"]:
            # Обновляем существующий пресет со всеми параметрами подписок
            subscription_params = [
                'basic_subscription_price', 'basic_subscription_start_month',
                'premium_subscription_price', 'premium_subscription_start_month',
                'business_subscription_price', 'business_subscription_start_month',
                'basic_subscription_conversion', 'premium_subscription_conversion'
            ]
            
            # Проверяем наличие всех параметров подписок
            for param in subscription_params:
                if param not in values and param in st.session_state:
                    values[param] = st.session_state[param]
            
            PRESETS[preset_name].update(values)
            log_info(f"Updated preset {preset_name} with values: {values}")
        else:
            # Сохраняем новый пользовательский пресет
            with open('custom_presets.json', 'r') as f:
                custom_presets = json.load(f)
    except FileNotFoundError:
        custom_presets = {}

    if preset_name not in ["pessimistic", "standard", "optimistic"]:
        custom_presets[preset_name] = values
        with open('custom_presets.json', 'w') as f:
            json.dump(custom_presets, f)
            log_info(f"Saved custom preset {preset_name}")


def load_custom_preset(preset_name):
    try:
        with open('custom_presets.json', 'r') as f:
            custom_presets = json.load(f)
            if preset_name in custom_presets:
                for key, value in custom_presets[preset_name].items():
                    st.session_state[key] = value
    except FileNotFoundError:
        st.error("No custom presets found")
