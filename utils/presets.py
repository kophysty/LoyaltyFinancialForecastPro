import streamlit as st
import json

PRESETS = {
    "pessimistic": {
        "commission_rate": 0.015,
        "monthly_transaction_volume": 800000,
        "transaction_growth_rate": 0.03,
        "initial_subscribers": 800,
        "subscriber_growth_rate": 0.05,
        "subscription_price": 24.99,
        "base_ad_revenue": 4000,
        "ad_revenue_growth_rate": 0.02,
        "base_payroll": 55000,
        "payroll_growth_rate": 0.05,
        "base_marketing_spend": 12000,
        "marketing_growth_rate": 0.07,
        "base_infrastructure_cost": 9000,
        "infrastructure_growth_rate": 0.03
    },
    "standard": {
        "commission_rate": 0.02,
        "monthly_transaction_volume": 1000000,
        "transaction_growth_rate": 0.05,
        "initial_subscribers": 1000,
        "subscriber_growth_rate": 0.08,
        "subscription_price": 29.99,
        "base_ad_revenue": 5000,
        "ad_revenue_growth_rate": 0.03,
        "base_payroll": 50000,
        "payroll_growth_rate": 0.04,
        "base_marketing_spend": 10000,
        "marketing_growth_rate": 0.06,
        "base_infrastructure_cost": 8000,
        "infrastructure_growth_rate": 0.02
    },
    "optimistic": {
        "commission_rate": 0.025,
        "monthly_transaction_volume": 1200000,
        "transaction_growth_rate": 0.07,
        "initial_subscribers": 1200,
        "subscriber_growth_rate": 0.1,
        "subscription_price": 34.99,
        "base_ad_revenue": 6000,
        "ad_revenue_growth_rate": 0.04,
        "base_payroll": 45000,
        "payroll_growth_rate": 0.03,
        "base_marketing_spend": 8000,
        "marketing_growth_rate": 0.05,
        "base_infrastructure_cost": 7000,
        "infrastructure_growth_rate": 0.02
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
