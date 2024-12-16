import streamlit as st

def initialize_session_state():
    # Initial Investment
    if 'initial_investment' not in st.session_state:
        st.session_state['initial_investment'] = 10000000
        
    # Base Parameters
    if 'initial_users' not in st.session_state:
        st.session_state['initial_users'] = 1000
    if 'active_conversion' not in st.session_state:
        st.session_state['active_conversion'] = 0.4
    if 'growth_rate_y1' not in st.session_state:
        st.session_state['growth_rate_y1'] = 0.30
    if 'growth_rate_y2' not in st.session_state:
        st.session_state['growth_rate_y2'] = 0.15
    if 'avg_check' not in st.session_state:
        st.session_state['avg_check'] = 3000
    if 'cashback_percent' not in st.session_state:
        st.session_state['cashback_percent'] = 0.15
    if 'points_usage_rate' not in st.session_state:
        st.session_state['points_usage_rate'] = 0.70
        
    # Commission Rates
    if 'exchange_commission_rate' not in st.session_state:
        st.session_state['exchange_commission_rate'] = 0.03
    if 'reward_commission_rate' not in st.session_state:
        st.session_state['reward_commission_rate'] = 0.05
        
    # Expenses
    if 'burn_rate_fot_1' not in st.session_state:
        st.session_state['burn_rate_fot_1'] = 2500000
    if 'burn_rate_fot_2' not in st.session_state:
        st.session_state['burn_rate_fot_2'] = 3500000
    if 'base_infra_cost' not in st.session_state:
        st.session_state['base_infra_cost'] = 200000
    if 'cost_per_user' not in st.session_state:
        st.session_state['cost_per_user'] = 10
    if 'monthly_marketing_budget' not in st.session_state:
        st.session_state['monthly_marketing_budget'] = 200000
    if 'marketing_efficiency' not in st.session_state:
        st.session_state['marketing_efficiency'] = 100
        
    # Additional Revenue
    if 'ad_revenue_per_user' not in st.session_state:
        st.session_state['ad_revenue_per_user'] = 20
    if 'partnership_rate' not in st.session_state:
        st.session_state['partnership_rate'] = 0.005
