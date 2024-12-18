import json
import plotly.graph_objects as go
from utils.config import initialize_session_state
from utils.logging_config import log_error, log_info
from models.financial_model import FinancialModel
from utils.presets import PRESETS
from utils.translations import get_translation
import streamlit as st

# Set page config at the very start
st.set_page_config(
    page_title="Финансовая модель Кошелька Репутации",
    page_icon="💰",
    layout="wide"
)

def init_app():
    """Initialize application state"""
    # Set language if not set
    if 'language' not in st.session_state:
        st.session_state['language'] = 'ru'
    
    # Set current scenario if not set
    if 'current_scenario' not in st.session_state:
        st.session_state['current_scenario'] = 'standard'
    
    # Always load preset values for current scenario
    scenario = st.session_state['current_scenario']
    if scenario in PRESETS:
        preset_data = PRESETS[scenario].copy()
        for key, value in preset_data.items():
            st.session_state[key] = value
    
    # Initialize any missing parameters with defaults
    initialize_session_state()

# Initialize application state
init_app()

def format_money(amount):
    return "{:,.0f} ₽".format(amount)

def main():
    try:
        # Language selector in sidebar
        with st.sidebar:
            selected_lang = st.selectbox(
                "",  # Empty label for cleaner look
                options=['ru', 'en'],
                format_func=lambda x: 'Русский' if x == 'ru' else 'English',
                index=0 if st.session_state['language'] == 'ru' else 1,
                key='language'
            )
            st.divider()
            
        # Main title
        st.title("Финансовая модель Кошелька Репутации")
        
        t = lambda key: get_translation(key, selected_lang)

        # Load custom presets if they exist
        try:
            with open('custom_presets.json', 'r') as f:
                custom_presets = json.load(f)
        except FileNotFoundError:
            custom_presets = {}

        # Combine default and custom scenarios
        scenario_names = {
            "standard": "Стандартный",
            "pessimistic": "Пессимистичный",
            "optimistic": "Оптимистичный",
            **{name: f"Пользовательский: {name}" for name in custom_presets.keys()}
        }
        
        # Get the current scenario from session state or default to 'standard'
        current_scenario = st.session_state.get('current_scenario', 'standard')

        # Base Parameters
        with st.expander("Базовые параметры", expanded=False):
            st.session_state['initial_users'] = st.number_input(
                "Начальное количество пользователей",
                min_value=500,
                max_value=5000,
                value=st.session_state['initial_users'],
                step=100,
                key="init_users_input"
            )
            st.session_state['growth_rate_y1'] = st.slider(
                "Темп роста 1й год",
                min_value=0.05,
                max_value=0.50,
                value=st.session_state['growth_rate_y1'],
                format="%.2f",
                key="growth_y1_slider"
            )
            st.session_state['growth_rate_y2'] = st.slider(
                "Темп роста 2й год",
                min_value=0.05,
                max_value=0.50,
                value=st.session_state['growth_rate_y2'],
                format="%.2f",
                key="growth_y2_slider"
            )
            st.session_state['avg_check'] = st.number_input(
                "Средний чек",
                min_value=1000,
                max_value=10000,
                value=int(st.session_state['avg_check']),
                step=500,
                key="avg_check_input"
            )

        # Commission Parameters
        with st.expander("Комиссии", expanded=False):
            st.session_state['exchange_commission_rate'] = st.slider(
                "Комиссия обмена",
                min_value=0.01,
                max_value=0.10,
                value=st.session_state['exchange_commission_rate'],
                format="%.3f",
                help="Комиссия, взимаемая при обмене баллов лояльности",
                key="exchange_commission_slider"
            )
            
            st.session_state['reward_commission_rate'] = st.slider(
                "Комиссия начисления",
                min_value=0.01,
                max_value=0.10,
                value=st.session_state['reward_commission_rate'],
                format="%.3f",
                help="Комиссия, взимаемая при начислении вознаграждений",
                key="reward_commission_slider"
            )

        with st.expander("Marketing & Operations", expanded=False):
            col5, col6 = st.columns(2)
            with col5:
                st.session_state['marketing_spend_rate'] = st.slider(
                    "Затраты на маркетинг (% от дохода)",
                    min_value=0.0,
                    max_value=25.0,
                    value=float(st.session_state.get('marketing_spend_rate', 0.05) * 100),
                    step=0.5,
                    format="%.1f%%",
                    help="Процент от дохода, направляемый на маркетинг",
                    key="marketing_rate_slider"
                ) / 100
            with col6:
                st.session_state['marketing_efficiency'] = st.number_input(
                    "Marketing Efficiency (users per 100K)",
                    min_value=10,
                    max_value=500,
                    value=st.session_state['marketing_efficiency'],
                    step=10
                )
        
        # Initialize model and calculate with current parameters
        model = FinancialModel()
        data = model.calculate_financials()
        
        if not data:
            st.error("No data available for visualization")
            return
            
        # Display scenario and month selection in one row
        col_scenario, col_month = st.columns(2)
        with col_scenario:
            selected_scenario = st.selectbox(
                "Сценарий",
                options=list(scenario_names.keys()),
                format_func=lambda x: scenario_names[x],
                key='scenario_selector',
                index=list(scenario_names.keys()).index(current_scenario)
            )
            # Apply selected scenario if it changed
            if selected_scenario != current_scenario:
                st.session_state['current_scenario'] = selected_scenario
                if selected_scenario in PRESETS:
                    # Update all parameters from preset
                    for key, value in PRESETS[selected_scenario].items():
                        st.session_state[key] = value
                    st.rerun()
                elif selected_scenario in custom_presets:
                    # Update all parameters from custom preset
                    for key, value in custom_presets[selected_scenario].items():
                        st.session_state[key] = value
                    st.rerun()
                    
        with col_month:
            selected_month = st.selectbox("Месяц", range(1, 25), 23)
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
            min-height: 180px;
            display: flex;
            flex-direction: column;
        }
        .metric-title {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 8px;
            flex: 0 0 auto;
        }
        .metric-value {
            font-size: 1.2em;
            font-weight: bold;
            color: #1f1f1f;
            margin-bottom: 8px;
            text-align: right;
            word-wrap: break-word;
            overflow-wrap: break-word;
            flex: 0 0 auto;
        }
        .metric-subtitle {
            font-size: 0.8em;
            color: #666;
            margin-top: auto;
            padding-top: 8px;
            border-top: 1px solid #f0f0f0;
        }
        .metric-details {
            font-size: 0.8em;
            color: #666;
            margin-top: 8px;
            flex: 1 1 auto;
        }
        </style>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">Месячная выручка</div>
                <div class="metric-value">{month_data['revenue']:,.0f} ₽</div>
                <div class="metric-details">
                    <div style="text-align: right">Объём покупок (GMV): {month_data['purchase_volume']:,.0f} ₽</div>
                    <div style="text-align: right">Оборот программы: {month_data['loyalty_turnover']:,.0f} ₽</div>
                </div>
                <div class="metric-subtitle">Общая за 2 года: {total_revenue:,.0f} ₽</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">Месячные расходы</div>
                <div class="metric-value">{month_data['expenses']:,.0f} ₽</div>
                <div class="metric-details">
                    <div style="text-align: right">Операционные: {month_data['operational_expenses']:,.0f} ₽</div>
                    <div style="text-align: right">Маркетинг: {month_data['marketing']:,.0f} ₽</div>
                    <div style="text-align: right">Налоги: {month_data['taxes']:,.0f} ₽</div>
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
        st.subheader("Выручка, расходы и прибыль")
        fig_revenue = go.Figure()

        # Prepare data for traces
        months = [d['month'] for d in data]
        traces_data = [
            ('Выручка', [d['revenue'] for d in data], '#8884d8'),
            ('Маркетинг', [d['marketing'] for d in data], '#82ca9d'),
            ('ФОТ', [d['fot'] for d in data], '#ff7300'),
            ('Налоги', [d.get('taxes', 0) for d in data], '#d88884'),
            ('Чистая прибыль', [d['profit'] for d in data], '#ffc658')
        ]

        # Add traces with customized hover template
        for name, values, color in traces_data:
            fig_revenue.add_trace(go.Scatter(
                x=months,
                y=values,
                name=name,
                mode='lines+markers',
                line=dict(color=color, width=2),
                marker=dict(size=6, color=color),
                hovertemplate=f"{name}: %{{y:,.0f}} ₽<extra></extra>"
            ))

        # Update layout with improved styling
        fig_revenue.update_layout(
            showlegend=True,
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=600,  # Increased height
            xaxis=dict(
                title='Месяц',
                showgrid=True,
                gridwidth=1,
                gridcolor='#f0f0f0',
                tickformat=',d',
                zeroline=False
            ),
            yaxis=dict(
                title='Сумма (₽)',
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
            margin=dict(l=50, r=50, t=30, b=50),  # Reduced top margin
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
        
        # Placeholder for future extensions
        st.markdown("")
        
        # График структуры выручки
        st.subheader("Структура выручки")
        fig_revenue_structure = go.Figure()

        # Подготовка данных для графика
        months = [d['month'] for d in data]
        revenue_components = [
            ('Комиссии обмена/начисления', [d['commission_revenue'] - d.get('expired_points_income', 0) for d in data], '#8884d8'),
            ('Неизрасходованные баллы', [d.get('expired_points_income', 0) for d in data], '#4B0082'),
            ('Премиум сервисы', [d['premium_revenue'] for d in data], '#ffc658'),
            ('Доп. доходы', [d['additional_revenue'] for d in data], '#ff7300')
        ]

        # Добавление слоев на график
        for name, values, color in revenue_components:
            fig_revenue_structure.add_trace(go.Scatter(
                x=months,
                y=values,
                name=name,
                mode='lines',
                line=dict(width=0),
                stackgroup='one',
                fillcolor=color,
                hovertemplate=f"{name}: %{{y:,.0f}} ₽<extra></extra>"
            ))

        # Настройка внешнего вида
        fig_revenue_structure.update_layout(
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
                title='Сумма (₽)',
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
        st.plotly_chart(fig_revenue_structure, use_container_width=True)

        # Display user growth
        st.subheader("Рост пользователей")
        fig_users = go.Figure()

        # Add traces for different types of growth
        fig_users.add_trace(go.Scatter(
            x=[d['month'] for d in data],
            y=[d['active_users'] for d in data],
            name='Активные пользователи',
            mode='lines+markers',
            line=dict(color='#8884d8', width=2),
            marker=dict(size=6),
            hovertemplate='Активные пользователи: %{y:,.0f}<extra></extra>'
        ))

        fig_users.add_trace(go.Scatter(
            x=[d['month'] for d in data],
            y=[d['new_users'] for d in data],
            name='Новые от маркетинга',
            mode='lines+markers',
            line=dict(color='#82ca9d', width=2),
            marker=dict(size=6),
            hovertemplate='Новые от маркетинга: %{y:,.0f}<extra></extra>'
        ))

        fig_users.add_trace(go.Scatter(
            x=[d['month'] for d in data],
            y=[d['base_growth'] for d in data],
            name='Органический рост',
            mode='lines+markers',
            line=dict(color='#ffc658', width=2),
            marker=dict(size=6),
            hovertemplate='Органический рост: %{y:,.0f}<extra></extra>'
        ))

        # Add partner growth
        fig_users.add_trace(go.Scatter(
            x=[d['month'] for d in data],
            y=[d['active_users'] / 100 for d in data],  # Partners are 1/100 of active users
            name='Партнеры',
            mode='lines+markers',
            line=dict(color='#ff7300', width=2),
            marker=dict(size=6),
            hovertemplate='Партнеры: %{y:,.0f}<extra></extra>'
        ))

        # Update layout with improved styling
        fig_users.update_layout(
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
                title='Количество пользователей',
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
        st.plotly_chart(fig_users, use_container_width=True)
        
        # Display turnover
        st.subheader("Объём покупок (GMV) и оборот программы")
        fig_turnover = go.Figure()
        fig_turnover.add_trace(go.Scatter(
            x=[d['month'] for d in data],
            y=[d['purchase_volume'] for d in data],
            name='Объём покупок (GMV)',
            mode='lines+markers',
            line=dict(color='#8884d8', width=2),
            marker=dict(size=6),
            hovertemplate='Объём покупок: %{y:,.0f} ₽<extra></extra>'
        ))
        
        fig_turnover.add_trace(go.Scatter(
            x=[d['month'] for d in data],
            y=[d['loyalty_turnover'] for d in data],
            name='Оборот программы лояльности',
            mode='lines+markers',
            line=dict(color='#82ca9d', width=2),
            marker=dict(size=6),
            hovertemplate='Оборот программы: %{y:,.0f} ₽<extra></extra>'
        ))
        
        # Update layout with improved styling
        fig_turnover.update_layout(
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
                title='Сумма (₽)',
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
        st.plotly_chart(fig_turnover, use_container_width=True)
        
    except Exception as e:
        log_error(e, context="Error in main application")
        st.error(f"An error occurred in the application: {str(e)}")

if __name__ == "__main__":
    main()