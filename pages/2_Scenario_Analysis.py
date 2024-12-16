import streamlit as st
import plotly.graph_objects as go
from models.financial_model import FinancialModel
from utils.presets import PRESETS
from utils.logging_config import log_error, log_warning, log_info

def format_currency(value):
    return f"₽{value:,.2f}"

def backup_state():
    """Create a backup of current session state values"""
    log_info("Creating session state backup")
    backup = {}
    for key in st.session_state:
        if isinstance(st.session_state[key], (int, float, str, bool)):
            backup[key] = st.session_state[key]
    return backup

def restore_state(backup):
    """Restore session state from backup"""
    log_info("Restoring session state from backup")
    for key, value in backup.items():
        if key in st.session_state:
            st.session_state[key] = value

def scenario_analysis_page():
    st.title("Анализ сценариев")
    
    try:
        # Initialize model
        model = FinancialModel()
        
        # Display scenario selection
        scenarios = ["pessimistic", "standard", "optimistic"]
        selected_scenarios = st.multiselect(
            "Выберите сценарии для сравнения",
            scenarios,
            default=scenarios,
            format_func=lambda x: {"pessimistic": "Пессимистичный", 
                                 "standard": "Стандартный", 
                                 "optimistic": "Оптимистичный"}[x]
        )
        
        if not selected_scenarios:
            st.warning("Пожалуйста, выберите хотя бы один сценарий для анализа")
            return
        
        # Calculate metrics for each scenario
        results = {}
        metrics_data = []
        
        for scenario_name in selected_scenarios:
            try:
                # Backup current state
                state_backup = backup_state()
                
                # Load scenario preset
                required_keys = [
                    'commission_rate', 'monthly_transaction_volume', 'transaction_growth_rate',
                    'initial_subscribers', 'subscriber_growth_rate', 'subscription_price',
                    'base_ad_revenue', 'ad_revenue_growth_rate', 'base_payroll',
                    'payroll_growth_rate', 'base_marketing_spend', 'marketing_growth_rate',
                    'base_infrastructure_cost', 'infrastructure_growth_rate'
                ]
                
                for key in required_keys:
                    if key in PRESETS[scenario_name]:
                        st.session_state[key] = PRESETS[scenario_name][key]
                    else:
                        log_warning(f"Missing preset key: {key} in scenario {scenario_name}")
                
                # Calculate financials
                data = model.calculate_financials()
                results[scenario_name] = data
                
                # Extract key metrics
                final_month = data[-1]
                final_revenue = final_month['revenue']
                final_expenses = final_month['expenses']
                final_profit = final_month['profit']
                total_investment = sum(month['expenses'] for month in data)
                total_profit = sum(month['profit'] for month in data)
                roi = (total_profit / total_investment * 100) if total_investment > 0 else 0
                
                # Store metrics
                metrics_data.append({
                    "Сценарий": {"pessimistic": "Пессимистичный", 
                                "standard": "Стандартный", 
                                "optimistic": "Оптимистичный"}[scenario_name],
                    "Выручка (последний месяц)": format_currency(final_revenue),
                    "Расходы (последний месяц)": format_currency(final_expenses),
                    "Прибыль (последний месяц)": format_currency(final_profit),
                    "ROI": f"{roi:.1f}%"
                })
                
                # Restore original state
                restore_state(state_backup)
                
            except Exception as e:
                log_error(e, context=f"Error in scenario: {scenario_name}")
                st.error(f"Ошибка при расчете сценария {scenario_name}: {str(e)}")
                continue
        
        if not results:
            log_warning("No scenario results calculated")
            st.warning("Не удалось рассчитать ни один сценарий")
            return
        
        # Display metrics table
        st.subheader("Сравнение метрик")
        st.table(metrics_data)
        
        # Plot comparisons
        st.subheader("Графики сравнения")
        
        # Revenue comparison
        fig_revenue = go.Figure()
        for scenario_name in results:
            scenario_data = results[scenario_name]
            fig_revenue.add_trace(go.Scatter(
                x=[d['month'] for d in scenario_data],
                y=[d['revenue'] for d in scenario_data],
                name={"pessimistic": "Пессимистичный", 
                     "standard": "Стандартный", 
                     "optimistic": "Оптимистичный"}[scenario_name],
                mode='lines'
            ))
        fig_revenue.update_layout(
            title='Сравнение выручки по сценариям',
            xaxis_title='Месяц',
            yaxis_title='Выручка (₽)',
            height=500
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
        
        # Profit comparison
        fig_profit = go.Figure()
        for scenario_name in results:
            scenario_data = results[scenario_name]
            fig_profit.add_trace(go.Scatter(
                x=[d['month'] for d in scenario_data],
                y=[d['profit'] for d in scenario_data],
                name={"pessimistic": "Пессимистичный", 
                     "standard": "Стандартный", 
                     "optimistic": "Оптимистичный"}[scenario_name],
                mode='lines'
            ))
        fig_profit.update_layout(
            title='Сравнение прибыли по сценариям',
            xaxis_title='Месяц',
            yaxis_title='Прибыль (₽)',
            height=500
        )
        st.plotly_chart(fig_profit, use_container_width=True)
        
    except Exception as e:
        log_error(e, context="Error in scenario analysis page")
        st.error(f"Произошла ошибка при анализе сценариев: {str(e)}")

if __name__ == "__main__":
    scenario_analysis_page()
