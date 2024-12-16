import streamlit as st
import json

PRESETS = {
    "pessimistic": {
        "initial_users": 800,
        "active_conversion": 0.35,
        "growth_rate_y1": 0.20,
        "growth_rate_y2": 0.10,
        "avg_check": 2500,
        "points_usage_rate": 0.60,
        "exchange_commission_rate": 0.02,
        "reward_commission_rate": 0.03,
        "burn_rate_fot_1": 3000000,
        "burn_rate_fot_2": 4000000,
        "base_infra_cost": 250000,
        "monthly_marketing_budget": 150000,
        "marketing_efficiency": 100,
        "marketing_spend_rate": 0.15,
        "ad_revenue_per_user": 15,
        "partnership_rate": 0.003
    },
    "standard": {
        "initial_users": 1000,
        "active_conversion": 0.40,
        "growth_rate_y1": 0.08,  # Значительно снижен органический рост
        "growth_rate_y2": 0.04,  # Значительно снижен органический рост
        "avg_check": 3000,
        "points_usage_rate": 0.70,
        "exchange_commission_rate": 0.03,
        "reward_commission_rate": 0.05,
        "burn_rate_fot_1": 2500000,
        "burn_rate_fot_2": 3500000,
        "base_infra_cost": 200000,
        "monthly_marketing_budget": 200000,
        "marketing_efficiency": 250,  # Значительно увеличена эффективность маркетинга
        "ad_revenue_per_user": 20,
        "partnership_rate": 0.005
    },
    "optimistic": {
        "initial_users": 1200,
        "active_conversion": 0.45,
        "growth_rate_y1": 0.10,  # Значительно снижен органический рост
        "growth_rate_y2": 0.05,  # Значительно снижен органический рост
        "avg_check": 3500,
        "points_usage_rate": 0.80,
        "exchange_commission_rate": 0.04,
        "reward_commission_rate": 0.06,
        "burn_rate_fot_1": 2000000,
        "burn_rate_fot_2": 3000000,
        "base_infra_cost": 180000,
        "monthly_marketing_budget": 250000,
        "marketing_efficiency": 300,  # Значительно увеличена эффективность маркетинга
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
