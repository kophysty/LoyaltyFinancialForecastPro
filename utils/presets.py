import streamlit as st
import json

PRESETS = {
    "pessimistic": {
        "initial_users": 800,
        "active_conversion": 0.3,
        "growth_rate_y1": 0.15,  # Ниже стандартного
        "growth_rate_y2": 0.1,  # Ниже стандартного
        "avg_check": 2500,
        "points_usage_rate": 0.60,
        "cashback_rate": 0.15,
        "expired_points_rate": 0.03,  # Пессимистичный сценарий: меньше баллов сгорает
        "exchange_commission_rate": 0.02,
        "reward_commission_rate": 0.03,
        "burn_rate_fot_1": 2500000,
        "burn_rate_fot_2": 3000000,
        "base_infra_cost": 250000,
        "marketing_efficiency": 150,
        "marketing_spend_rate": 0.2,
        "ad_revenue_per_user": 15,
        "partnership_rate": 0.003
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
        "initial_investment": 10000000,
        "marketing_budget_fixed": 200000,
        "marketing_budget_rate": 0.05,
        "initial_fot": 0
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
    if preset_name in PRESETS:
        for key, value in PRESETS[preset_name].items():
            st.session_state[key] = value


def save_preset(preset_name, values):
    try:
        with open('custom_presets.json', 'r') as f:
            custom_presets = json.load(f)
    except FileNotFoundError:
        custom_presets = {}

    custom_presets[preset_name] = values

    with open('custom_presets.json', 'w') as f:
        json.dump(custom_presets, f)


def load_custom_preset(preset_name):
    try:
        with open('custom_presets.json', 'r') as f:
            custom_presets = json.load(f)
            if preset_name in custom_presets:
                for key, value in custom_presets[preset_name].items():
                    st.session_state[key] = value
    except FileNotFoundError:
        st.error("No custom presets found")
