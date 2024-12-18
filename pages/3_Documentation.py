
import streamlit as st
from utils.translations import get_translation

def documentation_page():
    lang = st.session_state.get('language', 'ru')
    
    if lang == 'ru':
        st.title("Документация финансовой модели Кошелька Репутации")
        
        st.markdown("""
        ### Ключевые метрики и механика расчётов

        #### Объёмы и обороты
        - **Объём покупок (GMV)** = Активные пользователи × Средний чек × 2.5 транзакций в месяц
            - Средний чек в стандартном сценарии: 2,800₽
            - Отражает все транзакции пользователей в торговых точках
        
        - **Оборот программы лояльности** = GMV × Ставка кэшбэка (12% в стандартном сценарии)
            - Объём начисленных баллов лояльности
            - Например: при GMV = 1,000,000₽ и ставке 12%, оборот программы = 120,000₽ в баллах

        #### Доходы платформы
        
        - **Механика баллов и доходов**:
            - Подтверждённые баллы:
                * Конвертируются в токены
                * Не имеют срока сгорания
            - Неподтверждённые баллы:
                * Сгорают если не подтверждены в течение 2 месяцев
                * После сгорания учитываются как доход платформы
        
        - **Комиссионные доходы**:
            - 3% при обмене баллов
            - 4% при начислении вознаграждений
        
        - **Партнёрские доходы**:
            - Единая премиум-подписка для торговых точек (8000₽/месяц)
            - Доступна с настраиваемого месяца (по умолчанию с 8-го месяца)
        
        #### Расходы
        - **Фонд оплаты труда (ФОТ)**:
            - Первые 6 месяцев: покрывается из начальных инвестиций
            - Месяцы 7-12: 2,500,000₽/месяц
            - После 12 месяцев: 3,500,000₽/месяц

        - **Затраты на маркетинг**:
            - Первые 6 месяцев: 
                * Фиксированный бюджет 200,000₽/месяц
                * Покрывается из первоначальных инвестиций
            - После 6 месяцев: 5% от выручки
            - Эффективность: 200 новых пользователей на 100,000₽

        - **Инфраструктура**: 
            - Базовые затраты 200,000₽/месяц
            - Первые 6 месяцев покрываются из первоначальных инвестиций
            - Масштабируются с ростом пользователей

        #### ROI и финансовые показатели
        - **Расчёт ROI** = (Общая операционная прибыль / (Операционные расходы + Первоначальные инвестиции)) × 100%
            - Операционные расходы включают:
                * ФОТ
                * Маркетинг (после 6-го месяца)
                * Инфраструктуру (после 6-го месяца)
            - Первоначальные инвестиции (60 млн ₽) включаются в расчет ROI при анализе сценариев
            - В первые 6 месяцев маркетинг и инфраструктура покрываются из первоначальных инвестиций

        #### Инвестиции и подготовительный этап
        - **Начальные инвестиции**: 60,000,000₽
        - **Подготовительный этап**: 35,000,000₽
        
        #### Налогообложение
        - **НДС (20%)**:
            - Начисляется на все виды выручки
            - Включает комиссии, подписки и доход от сгоревших баллов
        
        - **Налог на прибыль (20%)**:
            - База = Выручка - НДС - Операционные расходы
            - Включает доход от сгоревших баллов
            - Особенности учёта сгоревших баллов:
                * Баллы становятся доходом только после истечения периода подтверждения (по умолчанию 2 месяца)
                * Доход от сгоревших баллов = Неподтверждённые баллы × Процент сгорания
                * Полностью включается в налогооблагаемую базу

        ### Сценарии и их особенности

        #### Стандартный сценарий
        - Начальные пользователи: 1,000
        - Конверсия в активных: 30%
        - Темп роста: 25% (1й год), 15% (2й год)
        - Средний чек: 2,800₽
        - Ставка кэшбэка: 12%
        - Затраты на маркетинг: 15% от выручки
        - Marketing Efficiency: 200 пользователей на 100K₽

        #### Пессимистичный сценарий
        - Начальные пользователи: 800
        - Конверсия в активных: 25%
        - Темп роста: 20% (1й год), 10% (2й год)
        - Средний чек: 2,500₽
        - Ставка кэшбэка: 12%
        - Затраты на маркетинг: 15% от выручки
        - Marketing Efficiency: 150 пользователей на 100K₽

        #### Оптимистичный сценарий
        - Начальные пользователи: 1,200
        - Конверсия в активных: 35%
        - Темп роста: 30% (1й год), 20% (2й год)
        - Средний чек: 3,200₽
        - Ставка кэшбэка: 12%
        - Затраты на маркетинг: 10% от выручки
        - Marketing Efficiency: 200 пользователей на 100K₽

        ### Управление моделью
        - Все параметры настраиваются в разделе Управление параметрами
        - Сравнение сценариев доступно в разделе Анализ сценариев
        - Стандартные сценарии (Стандартный, Пессимистичный, Оптимистичный) можно изменять
        - Поддерживается создание, сохранение и удаление пользовательских сценариев
        """)
    else:
        st.title("Documentation for the Reputation Wallet Financial Model")
        
        st.markdown("""
        ## Financial Model Guide

        ### Key Metrics and Calculation Mechanics

        #### Volumes and Turnover
        - **Gross Merchandise Value (GMV)** = Active users × Average check × 2.5 transactions per month
            - Average check in standard scenario: 2,800₽
            - Reflects all user transactions at retail outlets
        
        - **Loyalty Program Turnover** = GMV × Cashback rate (12% in standard scenario)
            - Volume of loyalty points accrued
            - For example: with GMV = 1,000,000₽ and rate of 12%, program turnover = 120,000₽ in points

        #### Platform Income
        
        - **Points and Income Mechanics**:
            - Confirmed points:
                * Converted to tokens
                * Do not expire
            - Unconfirmed points:
                * Expire if not confirmed within 2 months
                * After expiration, counted as platform income
        
        - **Commission Income**:
            - 3% when exchanging points
            - 4% when accruing rewards
        
        - **Partner Income**:
            - Retail outlet subscriptions (basic/premium)
        
        #### Expenses
        - **Payroll**:
            - First 6 months: covered from initial investments
            - Months 7-12: 2,500,000₽/month
            - After 12 months: 3,500,000₽/month

        - **Marketing Expenses**:
            - First 6 months: fixed budget of 200,000₽/month
            - After 6 months: 5% of revenue
            - Efficiency: 200 new users per 100,000₽

        - **Infrastructure**: 
            - Basic costs of 200,000₽/month
            - Scales with user growth

        #### ROI and Financial Indicators
        - **ROI Calculation** = (Total operating profit / Total operating expenses) × 100%
            - Operating expenses include:
                * Payroll
                * Marketing
                * Infrastructure
            - Do not include initial investments, as model evaluates operational efficiency

        #### Taxation
        - **VAT (20%)**:
            - Charged on all types of revenue
            - Includes commissions, subscriptions, and income from expired points
        
        - **Corporate Income Tax (20%)**:
            - Base = Revenue - VAT - Operating expenses
            - Includes income from expired points
            - Features of expired points accounting:
                * Points become income only after confirmation period expires (default 2 months)
                * Income from expired points = Unconfirmed points × Expiration percentage
                * Fully included in taxable base

        ### Scenarios and Their Features

        #### Standard Scenario
        - Initial users: 1,000
        - Active conversion: 30%
        - Growth rate: 20% (year 1), 15% (year 2)
        - Average check: 2,800₽
        - Cashback rate: 12%

        #### Pessimistic Scenario
        - Initial users: 800
        - Active conversion: 30%
        - Growth rate: 15% (year 1), 10% (year 2)
        - Average check: 2,500₽
        - Cashback rate: 15%

        #### Optimistic Scenario
        - Initial users: 1,200
        - Active conversion: 45%
        - Growth rate: 25% (year 1), 15% (year 2)
        - Average check: 3,200₽
        - Cashback rate: 17%

        ### Model Management
        - All parameters are configurable in Parameter Management section
        - Scenario comparison available in Scenario Analysis section
        - Supports creation and saving of custom scenarios
        """)

if __name__ == "__main__":
    documentation_page()
