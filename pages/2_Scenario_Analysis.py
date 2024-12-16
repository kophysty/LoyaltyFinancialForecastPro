import streamlit as st
import plotly.graph_objects as go
from models.financial_model import FinancialModel

def scenario_analysis_page():
    st.title("Scenario Analysis")
    
    # Create financial models for each scenario
    models = {
        "Pessimistic": FinancialModel(),
        "Standard": FinancialModel(),
        "Optimistic": FinancialModel()
    }
    
    # Calculate results for each scenario
    results = {}
    for scenario, model in models.items():
        if scenario == "Pessimistic":
            st.session_state.update({
                "commission_rate": 0.015,
                "transaction_growth_rate": 0.03,
                "subscriber_growth_rate": 0.05
            })
        elif scenario == "Optimistic":
            st.session_state.update({
                "commission_rate": 0.025,
                "transaction_growth_rate": 0.07,
                "subscriber_growth_rate": 0.1
            })
        results[scenario] = model.calculate_financials()
    
    # Revenue Comparison
    st.subheader("Revenue Comparison")
    fig_revenue = go.Figure()
    
    for scenario, result in results.items():
        fig_revenue.add_trace(go.Scatter(
            x=result['months'],
            y=result['total_revenue'],
            name=f"{scenario} Revenue",
            mode='lines'
        ))
    
    fig_revenue.update_layout(
        title='Revenue Scenarios Comparison',
        xaxis_title='Month',
        yaxis_title='Revenue ($)',
        height=500
    )
    st.plotly_chart(fig_revenue, use_container_width=True)
    
    # Profit Comparison
    st.subheader("Profit Comparison")
    fig_profit = go.Figure()
    
    for scenario, result in results.items():
        profits = [r - e for r, e in zip(result['total_revenue'], result['total_expenses'])]
        fig_profit.add_trace(go.Scatter(
            x=result['months'],
            y=profits,
            name=f"{scenario} Profit",
            mode='lines'
        ))
    
    fig_profit.update_layout(
        title='Profit Scenarios Comparison',
        xaxis_title='Month',
        yaxis_title='Profit ($)',
        height=500
    )
    st.plotly_chart(fig_profit, use_container_width=True)
    
    # Scenario Metrics Table
    st.subheader("Scenario Metrics")
    metrics_data = []
    
    for scenario, result in results.items():
        final_revenue = result['total_revenue'][-1]
        final_expenses = result['total_expenses'][-1]
        final_profit = final_revenue - final_expenses
        roi = (final_profit / final_expenses) * 100
        
        metrics_data.append({
            "Scenario": scenario,
            "Final Revenue": f"${final_revenue:,.2f}",
            "Final Expenses": f"${final_expenses:,.2f}",
            "Final Profit": f"${final_profit:,.2f}",
            "ROI": f"{roi:.1f}%"
        })
    
    st.table(metrics_data)

if __name__ == "__main__":
    scenario_analysis_page()
