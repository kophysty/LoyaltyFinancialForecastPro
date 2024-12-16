import pandas as pd
import streamlit as st

class FinancialModel:
    def __init__(self):
        self.months = range(1, 25)  # 2 years
        
    def calculate_financials(self):
        months = list(self.months)
        data = []
        active_users = st.session_state['initial_users'] * st.session_state['active_conversion']
        
        for month in months:
            # Growth rates and marketing impact
            is_first_year = month <= 12
            base_growth_rate = st.session_state['growth_rate_y1'] if is_first_year else st.session_state['growth_rate_y2']
            marketing_impact = (st.session_state['monthly_marketing_budget'] / 100000) * st.session_state['marketing_efficiency']
            total_new_users = active_users * base_growth_rate + marketing_impact
            active_users += total_new_users
            
            # Turnover and cashback
            turnover = active_users * st.session_state['avg_check'] * 2.5
            cashback = turnover * st.session_state['cashback_percent']
            used_points = cashback * st.session_state['points_usage_rate']
            
            # Commission Revenue
            exchange_commission = used_points * st.session_state['exchange_commission_rate']
            reward_commission = cashback * st.session_state['reward_commission_rate']
            
            # Partner Revenue
            stores = active_users / 150
            restaurants = active_users / 100
            subscription_revenue = 0
            if month > 12:
                subscription_revenue = (
                    (stores * 0.4 * 3000) + (stores * 0.2 * 10000) +
                    (restaurants * 0.4 * 2000) + (restaurants * 0.2 * 7000)
                )
            
            # Additional Revenue
            premium_revenue = active_users * 0.05 * (299 + 200)  # 5% premium users
            ad_revenue = active_users * st.session_state['ad_revenue_per_user']
            partner_revenue = turnover * st.session_state['partnership_rate']
            
            # Expenses
            burn_rate_fot = st.session_state['burn_rate_fot_1'] if is_first_year else st.session_state['burn_rate_fot_2']
            
            # Infrastructure costs
            infra_multiplier = 1.0
            if active_users > 50000:
                infra_multiplier = 2.0
            elif active_users > 10000:
                infra_multiplier = 1.5
            infra_cost = st.session_state['base_infra_cost'] * infra_multiplier
            
            # Total calculations
            operational_expenses = burn_rate_fot + infra_cost
            total_expenses = operational_expenses + st.session_state['monthly_marketing_budget']
            
            revenue = (
                exchange_commission + reward_commission + subscription_revenue +
                premium_revenue + ad_revenue + partner_revenue
            )
            
            # Tax calculations
            vat = revenue * 0.20  # VAT 20%
            net_revenue = revenue - vat
            profit_before_tax = net_revenue - total_expenses
            profit_tax = profit_before_tax * 0.20 if profit_before_tax > 0 else 0
            total_tax = vat + profit_tax
            net_profit = profit_before_tax - profit_tax
            
            data.append({
                'month': month,
                'revenue': revenue,
                'expenses': total_expenses,
                'marketing': st.session_state['monthly_marketing_budget'],
                'fot': burn_rate_fot,
                'infra_cost': infra_cost,
                'operational_expenses': operational_expenses,
                'profit': net_profit,
                'taxes': total_tax,
                'turnover': turnover,
                'active_users': active_users,
                'new_users': marketing_impact,
                'base_growth': active_users * base_growth_rate,
                'total_new_users': total_new_users,
                'commission_revenue': exchange_commission + reward_commission,
                'subscription_revenue': subscription_revenue,
                'premium_revenue': premium_revenue,
                'additional_revenue': ad_revenue + partner_revenue
            })
        
        return data
