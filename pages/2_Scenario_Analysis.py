import streamlit as st
import plotly.graph_objects as go
from models.financial_model import FinancialModel

def scenario_analysis_page():
    st.title("Сценарный анализ")
    
    # Определение параметров для каждого сценария
    scenarios = {
        "Пессимистичный": {
            "growth_rate_y1": 0.20,
            "growth_rate_y2": 0.10,
            "points_usage_rate": 0.60,
            "exchange_commission_rate": 0.02,
            "reward_commission_rate": 0.04,
            "partnership_rate": 0.004
        },
        "Стандартный": {
            "growth_rate_y1": 0.30,
            "growth_rate_y2": 0.15,
            "points_usage_rate": 0.70,
            "exchange_commission_rate": 0.03,
            "reward_commission_rate": 0.05,
            "partnership_rate": 0.005
        },
        "Оптимистичный": {
            "growth_rate_y1": 0.40,
            "growth_rate_y2": 0.20,
            "points_usage_rate": 0.80,
            "exchange_commission_rate": 0.04,
            "reward_commission_rate": 0.06,
            "partnership_rate": 0.006
        }
    }
    
    # Рассчитываем результаты для каждого сценария
    results = {}
    for scenario_name, params in scenarios.items():
        # Сохраняем текущие значения
        original_state = {
            key: st.session_state[key] 
            for key in params.keys() 
            if key in st.session_state
        }
        
        # Применяем параметры сценария
        st.session_state.update(params)
        
        # Рассчитываем финансовую модель
        model = FinancialModel()
        results[scenario_name] = model.calculate_financials()
        
        # Восстанавливаем оригинальные значения
        st.session_state.update(original_state)
    
    # График выручки
    st.subheader("Сравнение выручки")
    fig_revenue = go.Figure()
    
    for scenario_name, result in results.items():
        fig_revenue.add_trace(go.Scatter(
            x=[r['month'] for r in result],
            y=[r['revenue'] for r in result],
            name=scenario_name,
            mode='lines'
        ))
    
    fig_revenue.update_layout(
        title='Сравнение выручки по сценариям',
        xaxis_title='Месяц',
        yaxis_title='Выручка (₽)',
        height=500
    )
    st.plotly_chart(fig_revenue, use_container_width=True)
    
    # График прибыли
    st.subheader("Сравнение прибыли")
    fig_profit = go.Figure()
    
    for scenario_name, result in results.items():
        fig_profit.add_trace(go.Scatter(
            x=[r['month'] for r in result],
            y=[r['profit'] for r in result],
            name=scenario_name,
            mode='lines'
        ))
    
    fig_profit.update_layout(
        title='Сравнение прибыли по сценариям',
        xaxis_title='Месяц',
        yaxis_title='Прибыль (₽)',
        height=500
    )
    st.plotly_chart(fig_profit, use_container_width=True)
    
    # Таблица метрик
    st.subheader("Метрики по сценариям")
    metrics_data = []
    
    def format_currency(value):
        return f"₽{value:,.0f}"
    
    for scenario_name, result in results.items():
        # Берем данные последнего месяца
        final_month = result[-1]
        final_revenue = final_month['revenue']
        final_expenses = final_month['expenses']
        final_profit = final_month['profit']
        roi = (final_profit / final_expenses * 100) if final_expenses > 0 else 0
        
        metrics_data.append({
            "Сценарий": scenario_name,
            "Выручка (последний месяц)": format_currency(final_revenue),
            "Расходы (последний месяц)": format_currency(final_expenses),
            "Прибыль (последний месяц)": format_currency(final_profit),
            "ROI": f"{roi:.1f}%"
        })
    
    st.table(metrics_data)

if __name__ == "__main__":
    scenario_analysis_page()
