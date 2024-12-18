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
                if scenario_name in PRESETS:
                    # Directly update session state with all preset values
                    for key, value in PRESETS[scenario_name].items():
                        st.session_state[key] = value
                    log_info(f"Applied preset {scenario_name} with values: {PRESETS[scenario_name]}")
                else:
                    log_warning(f"Preset not found: {scenario_name}")
                    continue
                
                # Calculate financials
                data = model.calculate_financials()
                results[scenario_name] = data
                
                # Extract key metrics
                final_month = data[-1]
                final_revenue = final_month['revenue']
                final_expenses = final_month['expenses']
                final_profit = final_month['profit']
                # Calculate total operational expenses
                total_operational_expenses = sum(month['expenses'] for month in data)
                total_profit = sum(month['profit'] for month in data)
                
                # Add initial and preparatory investments
                initial_investment = st.session_state.get('initial_investment', 10000000)
                preparatory_expenses = st.session_state.get('preparatory_expenses', 21000000)
                total_investment = total_operational_expenses + initial_investment + preparatory_expenses
                log_info(f"Scenario {scenario_name}: Total investment = {total_investment} (operational: {total_operational_expenses}, initial: {initial_investment}, preparatory: {preparatory_expenses})")
                
                # Calculate ROI including all investments
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
        
        # Add investment parameters
        st.subheader("Параметры инвестиций")
        col1, col2 = st.columns(2)
        
        # Store previous values
        prev_investment = st.session_state.get('initial_investment', 10000000)
        prev_expenses = st.session_state.get('preparatory_expenses', 21000000)
        
        with col1:
            initial_investment = st.number_input(
                "Начальные инвестиции (₽)",
                min_value=1000000,
                max_value=65000000,
                value=prev_investment,
                step=1000000,
                help="Объем начальных инвестиций на запуск проекта",
                key='initial_investment_input',
                on_change=None
            )
            
        with col2:
            preparatory_expenses = st.number_input(
                "Расходы на подготовительный этап (₽)",
                min_value=1000000,
                max_value=39000000,
                value=prev_expenses,
                step=1000000,
                help="Расходы на подготовительный этап перед запуском (~$300K)",
                key='preparatory_expenses_input',
                on_change=None
            )
        
        # Update session state and trigger rerun if values changed
        if initial_investment != prev_investment:
            st.session_state['initial_investment'] = initial_investment
            st.rerun()
            
        if preparatory_expenses != prev_expenses:
            st.session_state['preparatory_expenses'] = preparatory_expenses
            st.rerun()
        
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
                mode='lines+markers',
                line=dict(width=2),
                marker=dict(size=6),
                hovertemplate=f"Выручка: %{{y:,.0f}} ₽<extra></extra>"
            ))
        fig_revenue.update_layout(
            showlegend=True,
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=600,
            xaxis=dict(
                title='Месяц',
                showgrid=True,
                gridwidth=1,
                gridcolor='#f0f0f0',
                tickformat=',d',
                zeroline=False
            ),
            yaxis=dict(
                title='Выручка (₽)',
                showgrid=True,
                gridwidth=1,
                gridcolor='#f0f0f0',
                tickformat=',.0f',
                zeroline=False
            ),
            hovermode='x unified',
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial"
            ),
            margin=dict(l=50, r=50, t=30, b=50),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
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
                mode='lines+markers',
                line=dict(width=2),
                marker=dict(size=6),
                hovertemplate=f"Прибыль: %{{y:,.0f}} ₽<extra></extra>"
            ))
        fig_profit.update_layout(
            showlegend=True,
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=600,
            xaxis=dict(
                title='Месяц',
                showgrid=True,
                gridwidth=1,
                gridcolor='#f0f0f0',
                tickformat=',d',
                zeroline=False
            ),
            yaxis=dict(
                title='Прибыль (₽)',
                showgrid=True,
                gridwidth=1,
                gridcolor='#f0f0f0',
                tickformat=',.0f',
                zeroline=False
            ),
            hovermode='x unified',
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial"
            ),
            margin=dict(l=50, r=50, t=30, b=50),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(fig_profit, use_container_width=True)
        
    except Exception as e:
        log_error(e, context="Error in scenario analysis page")
        st.error(f"Произошла ошибка при анализе сценариев: {str(e)}")

if __name__ == "__main__":
    scenario_analysis_page()
