import streamlit as st
import plotly.graph_objects as go
from models.financial_model import FinancialModel
from utils.config import initialize_session_state
from utils.presets import load_preset
from utils.logging_config import log_error, log_warning, log_info, log_debug

# Configure the application
try:
    log_info("Starting Loyalty Program Financial Modeling application")
    st.set_page_config(
    page_title="Loyalty Program Financial Modeling",
    page_icon="📊",
    layout="wide"
)

def format_currency(value):
    return f"₽{value:,.0f}"

def format_number(value):
    return f"{value:,.0f}"

def main():
    try:
        log_info("Initializing main application")
        initialize_session_state()
        
        st.title("Финансовая модель программы лояльности")
    
    # Header with month selector
    col1, col2 = st.columns([3, 1])
    with col2:
        selected_month = st.selectbox(
            "Показатели за",
            options=range(1, 25),
            format_func=lambda x: f"{x} месяц"
        )
    
    # Calculate financial data
    model = FinancialModel()
    results = model.calculate_financials()
    current_month = results[selected_month - 1]
    total_profit = sum(month['profit'] for month in results)
    
    # Main metrics cards
    st.markdown("### Ключевые показатели")
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        st.markdown("#### Месячная выручка")
        st.markdown(f"### {format_currency(current_month['revenue'])}")
        total_revenue = sum(month['revenue'] for month in results)
        st.markdown(f"За 2 года: {format_currency(total_revenue)}")
    
    with metrics_col2:
        st.markdown("#### Месячные расходы")
        total_month_expenses = current_month['expenses'] + current_month['taxes']
        st.markdown(f"### {format_currency(total_month_expenses)}")
        st.markdown(f"""
        ФОТ: {format_currency(current_month['fot'])}  
        Маркетинг: {format_currency(current_month['marketing'])}  
        Налоги: {format_currency(current_month['taxes'])}
        """)
    
    with metrics_col3:
        st.markdown("#### Месячная прибыль")
        st.markdown(f"### {format_currency(current_month['profit'])}")
        st.markdown(f"За 2 года: {format_currency(total_profit)}")
    
    with metrics_col4:
        st.markdown("#### Активные пользователи")
        st.markdown(f"### {format_number(current_month['active_users'])}")
        st.markdown(f"""
        Новых в месяц: +{format_number(current_month['total_new_users'])}  
        Партнеров: {format_number(current_month['active_users'] / 100)}
        """)
    
    # Charts
    st.markdown("### Графики")
    
    # Revenue and Expenses
    fig_financials = go.Figure()
    fig_financials.add_trace(go.Scatter(
        x=[r['month'] for r in results],
        y=[r['revenue'] for r in results],
        name='Выручка',
        line=dict(color='#8884d8')
    ))
    fig_financials.add_trace(go.Scatter(
        x=[r['month'] for r in results],
        y=[r['marketing'] for r in results],
        name='Маркетинг',
        line=dict(color='#82ca9d')
    ))
    fig_financials.add_trace(go.Scatter(
        x=[r['month'] for r in results],
        y=[r['fot'] for r in results],
        name='ФОТ',
        line=dict(color='#ff7300')
    ))
    fig_financials.add_trace(go.Scatter(
        x=[r['month'] for r in results],
        y=[r['taxes'] for r in results],
        name='Налоги',
        line=dict(color='#d88884')
    ))
    fig_financials.add_trace(go.Scatter(
        x=[r['month'] for r in results],
        y=[r['profit'] for r in results],
        name='Чистая прибыль',
        line=dict(color='#ffc658')
    ))
    
    fig_financials.update_layout(
        title='Выручка, расходы и прибыль',
        xaxis_title='Месяц',
        yaxis_title='Сумма (₽)',
        height=500
    )
    st.plotly_chart(fig_financials, use_container_width=True)
    
    # Revenue Structure
    fig_revenue = go.Figure()
    
    # Calculate cumulative sums for stacking
    y_commission = [r['commission_revenue'] for r in results]
    y_subscription = [r['subscription_revenue'] for r in results]
    y_premium = [r['premium_revenue'] for r in results]
    y_additional = [r['additional_revenue'] for r in results]
    
    x_months = [r['month'] for r in results]
    
    # Add traces in reverse order for proper stacking
    fig_revenue.add_trace(go.Scatter(
        x=x_months,
        y=[sum(x) for x in zip(y_commission, y_subscription, y_premium, y_additional)],
        fill='tonexty',
        name='Доп. доходы',
        line=dict(color='#ff7300')
    ))
    
    fig_revenue.add_trace(go.Scatter(
        x=x_months,
        y=[sum(x) for x in zip(y_commission, y_subscription, y_premium)],
        fill='tonexty',
        name='Премиум',
        line=dict(color='#ffc658')
    ))
    
    fig_revenue.add_trace(go.Scatter(
        x=x_months,
        y=[sum(x) for x in zip(y_commission, y_subscription)],
        fill='tonexty',
        name='Подписки',
        line=dict(color='#82ca9d')
    ))
    
    fig_revenue.add_trace(go.Scatter(
        x=x_months,
        y=y_commission,
        fill='tonexty',
        name='Комиссии',
        line=dict(color='#8884d8')
    ))
    
    fig_revenue.update_layout(
        title='Структура выручки',
        xaxis_title='Месяц',
        yaxis_title='Сумма (₽)',
        height=500
    )
    st.plotly_chart(fig_revenue, use_container_width=True)
    
    # User Growth
    fig_users = go.Figure()
    fig_users.add_trace(go.Scatter(
        x=[r['month'] for r in results],
        y=[r['active_users'] for r in results],
        name='Активные пользователи',
        line=dict(color='#8884d8')
    ))
    fig_users.add_trace(go.Scatter(
        x=[r['month'] for r in results],
        y=[r['new_users'] for r in results],
        name='Новые от маркетинга',
        line=dict(color='#82ca9d')
    ))
    fig_users.add_trace(go.Scatter(
        x=[r['month'] for r in results],
        y=[r['base_growth'] for r in results],
        name='Органический рост',
        line=dict(color='#ffc658')
    ))
    
    fig_users.update_layout(
        title='Рост пользователей',
        xaxis_title='Месяц',
        yaxis_title='Количество',
        height=500
    )
    st.plotly_chart(fig_users, use_container_width=True)
    
    # Turnover
    fig_turnover = go.Figure()
    fig_turnover.add_trace(go.Scatter(
        x=[r['month'] for r in results],
        y=[r['turnover'] for r in results],
        name='Оборот',
        line=dict(color='#8884d8')
    ))
    
    fig_turnover.update_layout(
        title='Общий оборот',
        xaxis_title='Месяц',
    except Exception as e:
        log_error(e, context="Error in main application")
        st.error(f"Произошла ошибка в приложении: {str(e)}")

        yaxis_title='Сумма (₽)',
        height=500
    )
    st.plotly_chart(fig_turnover, use_container_width=True)

if __name__ == "__main__":
    main()
