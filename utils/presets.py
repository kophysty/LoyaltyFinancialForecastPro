import streamlit as st
import json

PRESETS = {
    "pessimistic": {
        "initial_users": 800,
        "active_conversion": 0.25,  # Ниже стандартного
        "growth_rate_y1": 0.20,  # Ниже стандартного (25% -> 20%)
        "growth_rate_y2": 0.10,  # Ниже стандартного
        "avg_check": 2500,
        "points_usage_rate": 0.50,  # Ниже стандартного
        "cashback_rate": 0.12,  # Равно стандартному
        "expired_points_rate": 0.05,  # Меньше баллов сгорает
        "exchange_commission_rate": 0.02,
        "reward_commission_rate": 0.03,
        "base_infra_cost": 250000,
        "marketing_efficiency": 150,
        "marketing_spend_rate": 0.15,  # Равно стандартному
        "ad_revenue_per_user": 15,
        "partnership_rate": 0.003,
        "burn_rate_fot_1": 2500000,
        "burn_rate_fot_2": 3000000,
        "premium_business_start_month": 8,  # Равно стандартному
        "premium_user_start_month": 13,
        "ad_start_month": 8,  # Равно стандартному
        "premium_business_rate": 0.20,  # Ниже стандартного (20% вместо 30%)
        "premium_business_price": 8000  # Равно стандартному
    },
    "standard": {
        "initial_users": 1000,
        "active_conversion": 0.30,  # Более реалистичная конверсия
        "claim_period_months": 2,  # Период для подтверждения баллов в месяцах
        "growth_rate_y1": 0.25,  # Обновлено согласно требованиям
        "growth_rate_y2": 0.15,  # Эффект сетевой ценности
        "avg_check": 2800,  # Немного консервативнее
        "points_usage_rate": 0.55,  # Более реалистичное использование
        "cashback_rate": 0.12,  # Оптимизированный кэшбэк
        "expired_points_rate": 0.07,  # Больше баллов будет сгорать
        "exchange_commission_rate": 0.03,
        "reward_commission_rate": 0.04,
        "base_infra_cost": 200000,
        "marketing_efficiency": 200,
        "marketing_spend_rate": 0.15,  # Обновлено согласно требованиям
        "ad_revenue_per_user": 20,
        "partnership_rate": 0.005,
        "burn_rate_fot_1": 2500000,
        "burn_rate_fot_2": 3500000,
        "premium_business_start_month": 8,  # Обновлено согласно требованиям
        "premium_user_start_month": 13,
        "ad_start_month": 8,  # Обновлено согласно требованиям
        "premium_business_rate": 0.3,  # 30% партнеров на премиум-тарифе
        "premium_business_price": 8000  # Стоимость премиум-подписки
    },
    "optimistic": {
        "initial_users": 1200,
        "active_conversion": 0.35,  # Выше стандартного
        "growth_rate_y1": 0.30,  # Выше стандартного (25% -> 30%)
        "growth_rate_y2": 0.20,  # Выше стандартного
        "avg_check": 3200,
        "points_usage_rate": 0.60,  # Выше стандартного
        "cashback_rate": 0.12,  # Равно стандартному
        "expired_points_rate": 0.09,  # Больше баллов сгорает
        "exchange_commission_rate": 0.04,
        "reward_commission_rate": 0.05,
        "base_infra_cost": 180000,
        "marketing_efficiency": 250,  # Выше стандартного
        "marketing_spend_rate": 0.15,  # Равно стандартному
        "ad_revenue_per_user": 25,
        "partnership_rate": 0.007,
        "burn_rate_fot_1": 2000000,
        "burn_rate_fot_2": 3000000,
        "premium_business_start_month": 8,  # Равно стандартному
        "premium_user_start_month": 13,
        "ad_start_month": 8,  # Равно стандартному
        "premium_business_rate": 0.40,  # Выше стандартного (40% вместо 30%)
        "premium_business_price": 8000  # Равно стандартному
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

def delete_custom_preset(preset_name):
    """Delete a custom preset from custom_presets.json"""
    try:
        with open('custom_presets.json', 'r') as f:
            custom_presets = json.load(f)
        
        if preset_name in custom_presets:
            del custom_presets[preset_name]
            
            with open('custom_presets.json', 'w') as f:
                json.dump(custom_presets, f)
            return True
        return False
    except FileNotFoundError:
        return False

def is_custom_preset(preset_name):
    """Check if a preset is a custom preset"""
    try:
        with open('custom_presets.json', 'r') as f:
            custom_presets = json.load(f)
        return preset_name in custom_presets
    except FileNotFoundError:
        return False
