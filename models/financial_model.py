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
                    # Marketing calculations
                    if month <= 6:  # First 6 months: fixed budget
                        marketing_expense = 200000  # Fixed monthly budget
                    else:  # After month 6: percentage of revenue
                        marketing_expense = revenue * st.session_state['marketing_spend_rate']
                    
                    # Calculate marketing impact (new users from marketing spend)
                    marketing_impact = (marketing_expense / 100000) * st.session_state['marketing_efficiency']
                    
                    # Total new users is sum of organic growth and marketing impact
                    total_new_users = active_users * base_growth_rate + marketing_impact
                    active_users += total_new_users
                    
                    # Purchase volume (GMV) calculations
                    monthly_check = st.session_state['avg_check']
                    monthly_transactions = 3.5  # увеличено среднее количество транзакций в месяц
                    purchase_volume = active_users * monthly_check * monthly_transactions  # GMV - общий объем покупок пользователей
                    
                    # Commission calculations
                    # Расчет кэшбэка по установленной ставке
                    # Расчет кэшбэка (оборот программы лояльности)
                    loyalty_turnover = purchase_volume * st.session_state['cashback_rate']  # Фактический оборот программы лояльности
                    cashback = loyalty_turnover  # Для сохранения обратной совместимости
                    # Процент использования баллов с учетом периода подтверждения
                    claim_period = st.session_state.get('claim_period_months', 2)
                    used_points = cashback * st.session_state['points_usage_rate']
                    # Расчет дохода от неподтвержденных баллов
                    unclaimed_points = cashback * (1 - st.session_state['points_usage_rate'])
                    # Баллы сгорают только если не подтверждены в течение claim_period месяцев
                    if month <= claim_period:
                        expired_points_income = 0
                    else:
                        # Берем неподтвержденные баллы за период claim_period месяцев назад
                        historical_unclaimed = data[month - claim_period - 1]['unclaimed_points'] if month > claim_period else 0
                        expired_points_income = historical_unclaimed * st.session_state['expired_points_rate']
                    # Комиссия обмена 3% от использованных баллов
                    exchange_commission = used_points * st.session_state['exchange_commission_rate']
                    # Комиссия начисления 5% от всего кэшбэка
                    reward_commission = cashback * st.session_state['reward_commission_rate']
                    
                    # Partner Revenue
                    # Расчет количества партнеров (магазинов и ресторанов)
                    stores = active_users / 100  # 1 магазин на 100 пользователей
                    restaurants = active_users / 80  # 1 ресторан на 80 пользователей
                    
                    # Базовый доход от партнеров
                    partner_revenue = (stores + restaurants) * 1000  # фиксированный доход с партнера
                    
                    # Premium Revenue Streams
                    premium_user_rate = 0.04  # 4% премиум пользователей
                    premium_subscription = 399  # стоимость премиум подписки
                    premium_services = 300  # дополнительные премиум сервисы
                    
                    # Расчет премиум выручки
                    premium_revenue = active_users * premium_user_rate * (premium_subscription + premium_services)
                    
                    # Additional Revenue
                    # Доход от рекламы: фиксированная ставка с пользователя
                    ad_revenue = active_users * 20  # фиксированная ставка 20₽ с пользователя
                    partner_revenue = 0  # убрана комиссия с GMV
                    
                    # Expenses - FOT calculation based on month
                    burn_rate_fot = 0  # First 6 months - no FOT
                    if month > 12:  # Second year
                        burn_rate_fot = 4000000
                    elif month > 6:  # Months 7-12
                        burn_rate_fot = 2500000
                    
                    # Infrastructure costs with scaling
                    infra_multiplier = 1.0
                    if active_users > 50000:
                        infra_multiplier = 2.0
                    elif active_users > 10000:
                        infra_multiplier = 1.5
                    infra_cost = st.session_state['base_infra_cost'] * infra_multiplier
                    
                    # Marketing expenses calculation
                    marketing_expense = 0  # No marketing expenses for first 6 months
                    if month > 6:
                        marketing_expense = revenue * 0.05  # 5% of revenue from month 7
                    
                    # Revenue calculations
                    revenue = (
                        exchange_commission + reward_commission +
                        premium_revenue + ad_revenue + partner_revenue + expired_points_income
                    )

                    # Tax calculations
                    vat = revenue * 0.20  # VAT 20%
                    net_revenue = revenue - vat
                    
                    # Operational expenses
                    operational_expenses = burn_rate_fot + infra_cost
                    expenses_before_tax = operational_expenses + marketing_expense
                    
                    # Profit tax calculation
                    # Добавляем доход от сгоревших баллов к налогооблагаемой базе
                    profit_before_tax = net_revenue - expenses_before_tax
                    # Сгоревшие баллы включаются в налогооблагаемую базу
                    expired_points_taxable = expired_points_income
                    profit_before_tax += expired_points_taxable
                    profit_tax = profit_before_tax * 0.20 if profit_before_tax > 0 else 0
                    total_tax = vat + profit_tax
                    
                    # Total calculations including all taxes
                    total_expenses = expenses_before_tax + total_tax
                    net_profit = profit_before_tax - profit_tax
                    
                    data.append({
                        'month': month,
                        'revenue': revenue,
                        'expenses': total_expenses,
                        'marketing': marketing_expense,
                        'fot': burn_rate_fot,
                        'infra_cost': infra_cost,
                        'operational_expenses': operational_expenses,
                        'profit': net_profit,
                        'taxes': total_tax,
                        'purchase_volume': purchase_volume,
                        'loyalty_turnover': loyalty_turnover,
                        'active_users': active_users,
                        'new_users': marketing_impact,
                        'base_growth': active_users * base_growth_rate,
                        'total_new_users': total_new_users,
                        'commission_revenue': exchange_commission + reward_commission,
                        'expired_points_income': expired_points_income,
                        'unclaimed_points': unclaimed_points,
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