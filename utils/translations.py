TRANSLATIONS = {
    'en': {
        # Main page
        'title': 'Loyalty Program Financial Model',
        'base_parameters': 'Base Parameters',
        'commission_parameters': 'Commission Parameters',
        'marketing_operations': 'Marketing & Operations',
        'initial_users': 'Initial Users',
        'growth_rate_y1': 'Growth Rate Year 1',
        'growth_rate_y2': 'Growth Rate Year 2',
        'avg_check': 'Average Check (₽)',
        'active_conversion': 'Active Conversion Rate',
        'cashback_percent': 'Cashback Percentage',
        'exchange_commission': 'Exchange Commission Rate',
        'reward_commission': 'Reward Commission Rate',
        'marketing_budget': 'Monthly Marketing Budget (₽)',
        'marketing_efficiency': 'Marketing Efficiency (users per 100K)',
        'payroll_y1': 'Year 1 Monthly Payroll (₽)',
        'payroll_y2': 'Year 2 Monthly Payroll (₽)',
        
        # Metrics
        'monthly_revenue': 'Monthly Revenue',
        'monthly_expenses': 'Monthly Expenses',
        'monthly_profit': 'Monthly Profit',
        'active_participants': 'Active Part.',
        'total_for_2y': 'Total for 2 years',
        'turnover': 'Turnover',
        'payroll': 'Payroll',
        'marketing': 'Marketing',
        'taxes': 'Taxes',
        'new_monthly': 'New monthly',
        'partners': 'Partners',
        
        # Charts
        'revenue_expenses_profit': 'Revenue, Expenses and Profit',
        'revenue_structure': 'Revenue Structure',
        'user_growth': 'User Growth',
        'total_turnover': 'Total Turnover',
        'month': 'Month',
        'amount': 'Amount (₽)',
        'users': 'Users',
        
        # Scenarios
        'scenario': 'Scenario',
        'pessimistic': 'Pessimistic',
        'standard': 'Standard',
        'optimistic': 'Optimistic',
    },
    'ru': {
        # Main page
        'title': 'Модель финансов программы лояльности',
        'base_parameters': 'Базовые параметры',
        'commission_parameters': 'Параметры комиссий',
        'marketing_operations': 'Маркетинг и операции',
        'initial_users': 'Начальные пользователи',
        'growth_rate_y1': 'Рост 1й год',
        'growth_rate_y2': 'Рост 2й год',
        'avg_check': 'Средний чек (₽)',
        'active_conversion': 'Конверсия в активных',
        'cashback_percent': 'Процент кэшбэка',
        'exchange_commission': 'Комиссия обмена',
        'reward_commission': 'Комиссия вознаграждений',
        'marketing_budget': 'Месячный бюджет маркетинга (₽)',
        'marketing_efficiency': 'Эффективность маркетинга (польз./100К)',
        'payroll_y1': 'ФОТ 1й год (₽)',
        'payroll_y2': 'ФОТ 2й год (₽)',
        
        # Metrics
        'monthly_revenue': 'Месячная выручка',
        'monthly_expenses': 'Месячные расходы',
        'monthly_profit': 'Месячная прибыль',
        'active_participants': 'Актив. участники',
        'total_for_2y': 'Общая за 2 года',
        'turnover': 'Оборот',
        'payroll': 'ФОТ',
        'marketing': 'Маркетинг',
        'taxes': 'Налоги',
        'new_monthly': 'Новых в месяц',
        'partners': 'Партнеров',
        
        # Charts
        'revenue_expenses_profit': 'Выручка, расходы и прибыль',
        'revenue_structure': 'Структура выручки',
        'user_growth': 'Рост пользователей',
        'total_turnover': 'Общий оборот',
        'month': 'Месяц',
        'amount': 'Сумма (₽)',
        'users': 'Пользователи',
        
        # Scenarios
        'scenario': 'Сценарий',
        'pessimistic': 'Пессимистичный',
        'standard': 'Стандартный',
        'optimistic': 'Оптимистичный',
    }
}

def get_translation(key, lang='ru'):
    """Get translation for a key in specified language"""
    return TRANSLATIONS.get(lang, TRANSLATIONS['ru']).get(key, key)
