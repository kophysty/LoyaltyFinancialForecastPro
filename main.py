import streamlit as st
import plotly.graph_objects as go
from utils.config import initialize_session_state
from utils.logging_config import log_error, log_info
from models.financial_model import FinancialModel

# Initialize session state at the start
initialize_session_state()

def format_money(amount):
    return "{:,.0f} ₽".format(amount)

def main():
    try:
        st.title("Loyalty Program Financial Model")

        # Parameter Controls
        with st.expander("Base Parameters", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.session_state['initial_users'] = st.number_input(
                    "Initial Users",
                    min_value=500,
                    max_value=5000,
                    value=st.session_state['initial_users'],
                    step=100
                )
                st.session_state['growth_rate_y1'] = st.slider(
                    "Growth Rate Year 1",
                    min_value=0.05,
                    max_value=0.50,
                    value=st.session_state['growth_rate_y1'],
                    format="%.2f"
                )
                st.session_state['avg_check'] = st.number_input(
                    "Average Check (₽)",
                    min_value=1000,
                    max_value=10000,
                    value=int(st.session_state['avg_check']),
                    step=500
                )

            with col2:
                st.session_state['active_conversion'] = st.slider(
                    "Active Conversion Rate",
                    min_value=0.1,
                    max_value=1.0,
                    value=st.session_state['active_conversion'],
                    format="%.2f"
                )
                st.session_state['growth_rate_y2'] = st.slider(
                    "Growth Rate Year 2",
                    min_value=0.05,
                    max_value=0.50,
                    value=st.session_state['growth_rate_y2'],
                    format="%.2f"
                )
                st.session_state['cashback_percent'] = st.slider(
                    "Cashback Percentage",
                    min_value=0.05,
                    max_value=0.40,
                    value=st.session_state['cashback_percent'],
                    format="%.2f"
                )

        with st.expander("Commission Parameters", expanded=False):
            col3, col4 = st.columns(2)
            with col3:
                st.session_state['exchange_commission_rate'] = st.slider(
                    "Exchange Commission Rate",
                    min_value=0.01,
                    max_value=0.10,
                    value=st.session_state['exchange_commission_rate'],
                    format="%.3f"
                )
            with col4:
                st.session_state['reward_commission_rate'] = st.slider(
                    "Reward Commission Rate",
                    min_value=0.01,
                    max_value=0.10,
                    value=st.session_state['reward_commission_rate'],
                    format="%.3f"
                )

        with st.expander("Marketing & Operations", expanded=False):
            col5, col6 = st.columns(2)
            with col5:
                st.session_state['monthly_marketing_budget'] = st.number_input(
                    "Monthly Marketing Budget (₽)",
                    min_value=100000,
                    max_value=5000000,
                    value=st.session_state['monthly_marketing_budget'],
                    step=100000
                )
                st.session_state['burn_rate_fot_1'] = st.number_input(
                    "Year 1 Monthly Payroll (₽)",
                    min_value=1000000,
                    max_value=5000000,
                    value=st.session_state['burn_rate_fot_1'],
                    step=100000
                )
            with col6:
                st.session_state['marketing_efficiency'] = st.number_input(
                    "Marketing Efficiency (users per 100K)",
                    min_value=10,
                    max_value=500,
                    value=st.session_state['marketing_efficiency'],
                    step=10
                )
                st.session_state['burn_rate_fot_2'] = st.number_input(
                    "Year 2 Monthly Payroll (₽)",
                    min_value=1000000,
                    max_value=7000000,
                    value=st.session_state['burn_rate_fot_2'],
                    step=100000
                )
        
        # Initialize model and calculate with current parameters
        model = FinancialModel()
        data = model.calculate_financials()
        
        if not data:
            st.error("No data available for visualization")
            return
            
        # Display current month metrics
        selected_month = st.selectbox("Select Month", range(1, 25), 23)
        month_data = data[selected_month - 1]
        
        # Calculate totals
        total_revenue = sum(d['revenue'] for d in data)
        total_profit = sum(d['profit'] for d in data)
        
        # Create metrics columns with detailed information
        st.markdown("""
        <style>
        .metric-container {
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 15px;
            background-color: white;
            height: 100%;
        }
        .metric-title {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 8px;
        }
        .metric-value {
            font-size: 1.4em;
            font-weight: bold;
            color: #1f1f1f;
            margin-bottom: 8px;
            text-align: right;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .metric-subtitle {
            font-size: 0.8em;
            color: #666;
        }
        .metric-details {
            font-size: 0.8em;
            color: #666;
            margin-top: 8px;
        }
        </style>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">Месячная выручка</div>
                <div class="metric-value">{month_data['revenue']:,.0f} ₽</div>
                <div class="metric-subtitle">Общая за 2 года: {total_revenue:,.0f} ₽</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">Месячные расходы</div>
                <div class="metric-value">{month_data['expenses']:,.0f} ₽</div>
                <div class="metric-details">
                    <div style="text-align: right">ФОТ: {month_data['fot']:,.0f} ₽</div>
                    <div style="text-align: right">Маркетинг: {month_data['marketing']:,.0f} ₽</div>
                    <div style="text-align: right">Налоги: {month_data.get('taxes', 0):,.0f} ₽</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">Месячная прибыль</div>
                <div class="metric-value">{month_data['profit']:,.0f} ₽</div>
                <div class="metric-subtitle">Общая за 2 года: {total_profit:,.0f} ₽</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">Актив. участники</div>
                <div class="metric-value">{month_data['active_users']:,.0f}</div>
                <div class="metric-details">
                    Новых в месяц: +{month_data['total_new_users']:,.0f}<br>
                    Партнеров: {month_data['active_users'] / 100:,.0f}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
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