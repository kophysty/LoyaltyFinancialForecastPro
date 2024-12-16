import streamlit as st
import plotly.graph_objects as go
from utils.config import initialize_session_state
from utils.logging_config import log_error, log_info
from models.financial_model import FinancialModel

# Initialize session state at the start
initialize_session_state()

def main():
    try:
        st.title("Loyalty Program Financial Model")
        
        # Initialize model
        model = FinancialModel()
        data = model.calculate_financials()
        
        if not data:
            st.error("No data available for visualization")
            return
            
        # Display current month metrics
        selected_month = st.selectbox("Select Month", range(1, 25), 23)
        month_data = data[selected_month - 1]
        
        # Create metrics columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Revenue", f"₽{month_data['revenue']:,.2f}")
        
        with col2:
            st.metric("Expenses", f"₽{month_data['expenses']:,.2f}")
            
        with col3:
            st.metric("Profit", f"₽{month_data['profit']:,.2f}")
            
        with col4:
            st.metric("Active Users", f"{month_data['active_users']:,.0f}")
        
        # Display charts
        st.subheader("Revenue and Expenses Over Time")
        fig_revenue = go.Figure()
        fig_revenue.add_trace(go.Scatter(
            x=[d['month'] for d in data],
            y=[d['revenue'] for d in data],
            name='Revenue'
        ))
        fig_revenue.add_trace(go.Scatter(
            x=[d['month'] for d in data],
            y=[d['expenses'] for d in data],
            name='Expenses'
        ))
        fig_revenue.update_layout(
            xaxis_title='Month',
            yaxis_title='Amount (₽)',
            height=500
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
        
        # Display user growth
        st.subheader("User Growth")
        fig_users = go.Figure()
        fig_users.add_trace(go.Scatter(
            x=[d['month'] for d in data],
            y=[d['active_users'] for d in data],
            name='Active Users'
        ))
        fig_users.update_layout(
            xaxis_title='Month',
            yaxis_title='Number of Users',
            height=500
        )
        st.plotly_chart(fig_users, use_container_width=True)
        
        # Display turnover
        st.subheader("Monthly Turnover")
        fig_turnover = go.Figure()
        fig_turnover.add_trace(go.Scatter(
            x=[d['month'] for d in data],
            y=[d['turnover'] for d in data],
            name='Turnover'
        ))
        fig_turnover.update_layout(
            xaxis_title='Month',
            yaxis_title='Amount (₽)',
            height=500
        )
        st.plotly_chart(fig_turnover, use_container_width=True)
        
    except Exception as e:
        log_error(e, context="Error in main application")
        st.error(f"An error occurred in the application: {str(e)}")

if __name__ == "__main__":
    main()