import streamlit as st

def initialize_session_state():
    # Revenue Parameters
    if 'commission_rate' not in st.session_state:
        st.session_state['commission_rate'] = 0.02
    if 'monthly_transaction_volume' not in st.session_state:
        st.session_state['monthly_transaction_volume'] = 1000000
    if 'transaction_growth_rate' not in st.session_state:
        st.session_state['transaction_growth_rate'] = 0.05
    if 'initial_subscribers' not in st.session_state:
        st.session_state['initial_subscribers'] = 1000
    if 'subscriber_growth_rate' not in st.session_state:
        st.session_state['subscriber_growth_rate'] = 0.08
    if 'subscription_price' not in st.session_state:
        st.session_state['subscription_price'] = 29.99
    if 'base_ad_revenue' not in st.session_state:
        st.session_state['base_ad_revenue'] = 5000
    if 'ad_revenue_growth_rate' not in st.session_state:
        st.session_state['ad_revenue_growth_rate'] = 0.03
        
    # Expense Parameters
    if 'base_payroll' not in st.session_state:
        st.session_state['base_payroll'] = 50000
    if 'payroll_growth_rate' not in st.session_state:
        st.session_state['payroll_growth_rate'] = 0.04
    if 'base_marketing_spend' not in st.session_state:
        st.session_state['base_marketing_spend'] = 10000
    if 'marketing_growth_rate' not in st.session_state:
        st.session_state['marketing_growth_rate'] = 0.06
    if 'base_infrastructure_cost' not in st.session_state:
        st.session_state['base_infrastructure_cost'] = 8000
    if 'base_infrastructure_cost' not in st.session_state:
        st.session_state['infrastructure_growth_rate'] = 0.02
