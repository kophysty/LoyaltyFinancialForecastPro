import streamlit as st
from utils.presets import save_preset

def parameter_management_page():
    st.title("Parameter Management")
    
    st.subheader("Revenue Parameters")
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state['commission_rate'] = st.number_input(
            "Commission Rate",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state['commission_rate'],
            format="%.3f"
        )
        
        st.session_state['monthly_transaction_volume'] = st.number_input(
            "Monthly Transaction Volume ($)",
            min_value=0,
            value=int(st.session_state['monthly_transaction_volume'])
        )
        
        st.session_state['transaction_growth_rate'] = st.number_input(
            "Transaction Growth Rate",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state['transaction_growth_rate'],
            format="%.3f"
        )
        
        st.session_state['initial_subscribers'] = st.number_input(
            "Initial Subscribers",
            min_value=0,
            value=st.session_state['initial_subscribers']
        )
    
    with col2:
        st.session_state['subscriber_growth_rate'] = st.number_input(
            "Subscriber Growth Rate",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state['subscriber_growth_rate'],
            format="%.3f"
        )
        
        st.session_state['subscription_price'] = st.number_input(
            "Subscription Price ($)",
            min_value=0.0,
            value=st.session_state['subscription_price'],
            format="%.2f"
        )
        
        st.session_state['base_ad_revenue'] = st.number_input(
            "Base Ad Revenue ($)",
            min_value=0,
            value=st.session_state['base_ad_revenue']
        )
        
        st.session_state['ad_revenue_growth_rate'] = st.number_input(
            "Ad Revenue Growth Rate",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state['ad_revenue_growth_rate'],
            format="%.3f"
        )
    
    st.subheader("Expense Parameters")
    col3, col4 = st.columns(2)
    
    with col3:
        st.session_state['base_payroll'] = st.number_input(
            "Base Monthly Payroll ($)",
            min_value=0,
            value=st.session_state['base_payroll']
        )
        
        st.session_state['payroll_growth_rate'] = st.number_input(
            "Payroll Growth Rate",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state['payroll_growth_rate'],
            format="%.3f"
        )
    
    with col4:
        st.session_state['base_marketing_spend'] = st.number_input(
            "Base Marketing Spend ($)",
            min_value=0,
            value=st.session_state['base_marketing_spend']
        )
        
        st.session_state['marketing_growth_rate'] = st.number_input(
            "Marketing Growth Rate",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state['marketing_growth_rate'],
            format="%.3f"
        )
    
    st.subheader("Save Custom Preset")
    preset_name = st.text_input("Preset Name")
    if st.button("Save Preset") and preset_name:
        current_values = {key: st.session_state[key] for key in st.session_state.keys() 
                         if key not in ['custom_presets']}
        save_preset(preset_name, current_values)
        st.success(f"Preset '{preset_name}' saved successfully!")

if __name__ == "__main__":
    parameter_management_page()
