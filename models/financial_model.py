import pandas as pd
import streamlit as st

class FinancialModel:
    def __init__(self):
        self.months = range(1, 25)  # 2 years
        
    def calculate_revenue(self):
        commission_revenue = []
        subscription_revenue = []
        advertising_revenue = []
        
        for month in self.months:
            # Commission Revenue
            commission_rate = st.session_state['commission_rate']
            transaction_volume = st.session_state['monthly_transaction_volume'] * \
                               (1 + st.session_state['transaction_growth_rate']) ** (month - 1)
            commission = transaction_volume * commission_rate
            commission_revenue.append(commission)
            
            # Subscription Revenue
            subscribers = st.session_state['initial_subscribers'] * \
                         (1 + st.session_state['subscriber_growth_rate']) ** (month - 1)
            subscription_revenue.append(subscribers * st.session_state['subscription_price'])
            
            # Advertising Revenue
            ad_revenue = st.session_state['base_ad_revenue'] * \
                        (1 + st.session_state['ad_revenue_growth_rate']) ** (month - 1)
            advertising_revenue.append(ad_revenue)
            
        return commission_revenue, subscription_revenue, advertising_revenue
    
    def calculate_expenses(self):
        payroll_expenses = []
        marketing_expenses = []
        infrastructure_expenses = []
        
        for month in self.months:
            # Payroll Expenses
            base_payroll = st.session_state['base_payroll']
            payroll = base_payroll * (1 + st.session_state['payroll_growth_rate']) ** (month - 1)
            payroll_expenses.append(payroll)
            
            # Marketing Expenses
            marketing = st.session_state['base_marketing_spend'] * \
                       (1 + st.session_state['marketing_growth_rate']) ** (month - 1)
            marketing_expenses.append(marketing)
            
            # Infrastructure Expenses
            infrastructure = st.session_state['base_infrastructure_cost'] * \
                           (1 + st.session_state['infrastructure_growth_rate']) ** (month - 1)
            infrastructure_expenses.append(infrastructure)
            
        return payroll_expenses, marketing_expenses, infrastructure_expenses
    
    def calculate_financials(self):
        commission_revenue, subscription_revenue, ad_revenue = self.calculate_revenue()
        payroll_expenses, marketing_expenses, infrastructure_expenses = self.calculate_expenses()
        
        total_revenue = [sum(x) for x in zip(commission_revenue, subscription_revenue, ad_revenue)]
        total_expenses = [sum(x) for x in zip(payroll_expenses, marketing_expenses, infrastructure_expenses)]
        
        return {
            'months': list(self.months),
            'commission_revenue': commission_revenue,
            'subscription_revenue': subscription_revenue,
            'ad_revenue': ad_revenue,
            'total_revenue': total_revenue,
            'payroll_expenses': payroll_expenses,
            'marketing_expenses': marketing_expenses,
            'infrastructure_expenses': infrastructure_expenses,
            'total_expenses': total_expenses
        }
