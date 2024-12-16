import streamlit as st

def documentation_page():
    st.title("Parameter Documentation")
    
    st.markdown("""
    ## Revenue Parameters
    
    ### Commission Revenue
    - **Commission Rate**: Percentage of transaction value charged as commission
    - **Monthly Transaction Volume**: Total value of transactions processed per month
    - **Transaction Growth Rate**: Monthly growth rate of transaction volume
    
    ### Subscription Revenue
    - **Initial Subscribers**: Number of subscribers at the start
    - **Subscriber Growth Rate**: Monthly growth rate of subscribers
    - **Subscription Price**: Monthly subscription fee per user
    
    ### Advertising Revenue
    - **Base Ad Revenue**: Initial monthly advertising revenue
    - **Ad Revenue Growth Rate**: Monthly growth rate of advertising revenue
    
    ## Expense Parameters
    
    ### Payroll Expenses (ФОТ)
    
    Расходы на заработную плату (ФОТ) меняются в зависимости от периода:
    
    1. **Первые 6 месяцев (1-6)**: 
       - Расходы отсутствуют (₽0)
       - Период начального развития и тестирования
    
    2. **Второе полугодие (7-12 месяц)**:
       - Фиксированная сумма ₽2,500,000 в месяц
       - Начало активного найма и развития команды
    
    3. **Второй год (13-24 месяц)**:
       - Увеличение до ₽4,000,000 в месяц
       - Расширение команды для поддержки роста бизнеса
    
    > **Важно**: Эти значения являются базовыми и могут корректироваться в различных сценариях
    
    ### Marketing Expenses
    - **Base Marketing Spend**: Initial monthly marketing budget
    - **Marketing Growth Rate**: Monthly growth rate of marketing expenses
    
    ### Infrastructure Expenses
    - **Base Infrastructure Cost**: Initial monthly infrastructure costs
    - **Infrastructure Growth Rate**: Monthly growth rate of infrastructure costs
    
    ## Scenarios
    
    ### Pessimistic Scenario
    - Lower growth rates
    - Higher expenses
    - Conservative revenue projections
    
    ### Standard Scenario
    - Moderate growth rates
    - Balanced expenses
    - Realistic revenue projections
    
    ### Optimistic Scenario
    - Higher growth rates
    - Optimized expenses
    - Aggressive revenue projections
    """)
    
    st.subheader("Calculation Methodology")
    st.markdown("""
    ### Revenue Calculations
    1. Commission Revenue = Transaction Volume × Commission Rate
    2. Subscription Revenue = Number of Subscribers × Subscription Price
    st.markdown("""
    ## История изменений модели
    
    ### Обновление от 16.12.2024
    
    #### Изменения в расчете ФОТ
    - Реализована поэтапная система расчета ФОТ
    - Добавлены нулевые расходы для первых 6 месяцев
    - Установлен фиксированный ФОТ 2.5М руб. для месяцев 7-12
    - Увеличен ФОТ до 4М руб. для второго года
    
    #### Базовые параметры
    Оптимизирован набор базовых параметров:
    - Начальное количество пользователей
    - Темп роста 1й год
    - Темп роста 2й год
    - Средний чек
    
    > **Примечание**: Данный раздел будет обновляться с каждым значительным изменением в модели
    """)

    3. Total Revenue = Commission Revenue + Subscription Revenue + Ad Revenue
    
    ### Expense Calculations
    1. Monthly Expenses = Payroll + Marketing + Infrastructure
    2. Growth rates are applied monthly using compound growth formula
    3. Total Expenses = Sum of all expense categories
    
    ### Profit Calculation
    - Monthly Profit = Total Revenue - Total Expenses
    - ROI = (Profit / Total Expenses) × 100
    """)

if __name__ == "__main__":
    documentation_page()
