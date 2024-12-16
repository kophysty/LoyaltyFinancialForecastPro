import streamlit as st
from utils.logging_config import log_error, log_warning, log_info, log_debug

class FinancialModel:
    def __init__(self):
        self.months = range(1, 25)  # 2 years
        log_info("Initializing Financial Model")
        
    def calculate_financials(self):
        try:
            log_debug("Starting financial calculations")
            months = list(self.months)
            data = []
            
            # Validate required session state variables
            required_vars = ['initial_users', 'active_conversion']
            for var in required_vars:
                if var not in st.session_state:
                    raise KeyError(f"Missing required parameter: {var}")
            
            active_users = st.session_state['initial_users'] * st.session_state['active_conversion']
            log_info(f"Initial active users calculated: {active_users}")
            
            for month in months:
                try:
                    # Growth rates and marketing impact
                    is_first_year = month <= 12
                    base_growth_rate = st.session_state['growth_rate_y1'] if is_first_year else st.session_state['growth_rate_y2']
                    marketing_impact = (st.session_state['monthly_marketing_budget'] / 100000) * st.session_state['marketing_efficiency']
                    total_new_users = active_users * base_growth_rate + marketing_impact
                    active_users += total_new_users
                    
                    # Turnover calculations
                    monthly_check = st.session_state['avg_check']
                    monthly_transactions = 3.5  # увеличено среднее количество транзакций в месяц
                    turnover = active_users * monthly_check * monthly_transactions
                    
                    # Commission calculations
                    # Базовый кэшбэк 7% от оборота
                    cashback = turnover * 0.07
                    # 85% баллов используется
                    used_points = cashback * 0.85
                    # Комиссия обмена 3% от использованных баллов
                    exchange_commission = used_points * st.session_state['exchange_commission_rate']
                    # Комиссия начисления 5% от всего кэшбэка
                    reward_commission = cashback * st.session_state['reward_commission_rate']
                    
                    # Partner and Subscription Revenue
                    # Расчет количества партнеров (магазинов и ресторанов)
                    stores = active_users / 100  # 1 магазин на 100 пользователей
                    restaurants = active_users / 80  # 1 ресторан на 80 пользователей
                    subscription_revenue = 0
                    
                    # Subscription revenue starts from month 13
                    if month > 12:
                        # Распределение подписок по типам
                        basic_stores = stores * 0.35  # 35% базовых подписок
                        premium_stores = stores * 0.15  # 15% премиум подписок
                        basic_restaurants = restaurants * 0.35  # 35% базовых подписок
                        premium_restaurants = restaurants * 0.15  # 15% премиум подписок
                        
                        # Расчет выручки от подписок
                        subscription_revenue = (
                            (basic_stores * 2500) +  # базовая подписка магазина
                            (premium_stores * 8000) +  # премиум подписка магазина
                            (basic_restaurants * 2000) +  # базовая подписка ресторана
                            (premium_restaurants * 6000)  # премиум подписка ресторана
                        )
                    
                    # Premium Revenue Streams
                    premium_user_rate = 0.04  # 4% премиум пользователей
                    premium_subscription = 399  # стоимость премиум подписки
                    premium_services = 300  # дополнительные премиум сервисы
                    
                    # Расчет премиум выручки
                    premium_revenue = active_users * premium_user_rate * (premium_subscription + premium_services)
                    
                    # Additional Revenue
                    ad_revenue = active_users * st.session_state['ad_revenue_per_user']  # реклама
                    partner_revenue = turnover * st.session_state['partnership_rate']  # доход от партнеров
                    
                    # Expenses
                    burn_rate_fot = st.session_state['burn_rate_fot_1'] if is_first_year else st.session_state['burn_rate_fot_2']
                    
                    # Infrastructure costs with scaling
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
                except Exception as e:
                    log_error(e, context=f"Error processing month {month}")
                    raise
            
            return data
            
        except Exception as e:
            log_error(e, context="Error in calculate_financials")
            raise
