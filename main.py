import streamlit as st
import plotly.graph_objects as go
from models.financial_model import FinancialModel
from utils.config import initialize_session_state
from utils.presets import load_preset

st.set_page_config(
    page_title="Loyalty Program Financial Modeling",
    page_icon="📊",
    layout="wide"
)

def main():
    initialize_session_state()
    
    st.title("Loyalty Program Financial Modeling")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.subheader("Scenario Selection")
        preset_options = ["Custom", "Pessimistic", "Standard", "Optimistic"]
        selected_preset = st.selectbox("Choose Scenario", preset_options)
        
        if selected_preset != "Custom":
            load_preset(selected_preset.lower())
    
    with col1:
        st.subheader("Financial Overview")
        model = FinancialModel()
        results = model.calculate_financials()
        
        # Revenue Chart
        fig_revenue = go.Figure()
        fig_revenue.add_trace(go.Scatter(
            x=results['months'],
            y=results['total_revenue'],
            name='Total Revenue',
            line=dict(color='#2ecc71')
        ))
        fig_revenue.update_layout(
            title='Projected Revenue',
            xaxis_title='Month',
            yaxis_title='Amount ($)',
            height=400
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
        
        # Expenses Chart
        fig_expenses = go.Figure()
        fig_expenses.add_trace(go.Scatter(
            x=results['months'],
            y=results['total_expenses'],
            name='Total Expenses',
            line=dict(color='#e74c3c')
        ))
        fig_expenses.update_layout(
            title='Projected Expenses',
            xaxis_title='Month',
            yaxis_title='Amount ($)',
            height=400
        )
        st.plotly_chart(fig_expenses, use_container_width=True)
        
        # Key Metrics
        st.subheader("Key Metrics")
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        
        with metrics_col1:
            st.metric("2-Year Revenue", f"${results['total_revenue'][-1]:,.2f}")
            
        with metrics_col2:
            st.metric("2-Year Expenses", f"${results['total_expenses'][-1]:,.2f}")
            
        with metrics_col3:
            profit = results['total_revenue'][-1] - results['total_expenses'][-1]
            st.metric("2-Year Profit", f"${profit:,.2f}")

if __name__ == "__main__":
    main()
