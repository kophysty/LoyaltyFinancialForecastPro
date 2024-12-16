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
    
    ### Payroll Expenses
    - **Base Payroll**: Initial monthly payroll expenses
    - **Payroll Growth Rate**: Monthly growth rate of payroll expenses
    
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
