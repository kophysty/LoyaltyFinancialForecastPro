import streamlit as st

def initialize_session_state():
    """Initialize all session state variables with default values"""
    defaults = {
        # Initial Investment
        'initial_investment': 10000000,
        
        # Base Parameters
        'initial_users': 1000,
        'initial_subscribers': 1000,
        'active_conversion': 0.4,
        'growth_rate_y1': 0.30,
        'growth_rate_y2': 0.15,
        'avg_check': 3000,
        'cashback_percent': 0.15,
        'points_usage_rate': 0.70,
        'monthly_transaction_volume': 1000000,
        'transaction_growth_rate': 0.05,
        'subscriber_growth_rate': 0.08,
        'subscription_price': 29.99,
        
        # Commission Rates
        'commission_rate': 0.02,
        'exchange_commission_rate': 0.03,
        'reward_commission_rate': 0.05,
        
        # Expenses
        'burn_rate_fot_1': 2500000,
        'burn_rate_fot_2': 3500000,
        'base_infra_cost': 200000,
        'cost_per_user': 10,
        'monthly_marketing_budget': 200000,
        'marketing_efficiency': 100,
        'base_marketing_spend': 10000,
        'marketing_growth_rate': 0.06,
        'base_payroll': 50000,
        'payroll_growth_rate': 0.04,
        'infrastructure_growth_rate': 0.02,
        
        # Additional Revenue
        'ad_revenue_per_user': 20,
        'partnership_rate': 0.005,
        'base_ad_revenue': 5000,
        'ad_revenue_growth_rate': 0.03
    }
    
    # Initialize all variables in session state
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
