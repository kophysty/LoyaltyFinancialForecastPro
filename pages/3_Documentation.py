import streamlit as st
from utils.translations import get_translation

def documentation_page():
    st.title("Documentation for the Reputation Wallet Financial Model")
    
    st.markdown("""
    ## Financial Model Guide

    ### Key Metrics and Calculation Mechanics

    #### Volumes and Turnover
    - **Gross Merchandise Value (GMV)** = Active users × Average check × 2.5 transactions per month
        - Average check in the standard scenario: 2,800₽
        - Reflects all user transactions at retail outlets
    
    - **Loyalty Program Turnover** = GMV × Cashback rate (12% in the standard scenario)
        - Volume of loyalty points accrued
        - For example: with GMV = 1,000,000₽ and a rate of 12%, the program turnover = 120,000₽ in points

    #### Platform Income
    
    - **Points and Income Mechanics**:
        - Confirmed points:
            * Converted to tokens
            * Do not expire
        - Unconfirmed points:
            * Expire if not confirmed within 2 months
            * After expiration, they are counted as platform income
    
    - **Commission Income**:
        - 3% when exchanging points
        - 4% when accruing rewards
    
    - **Partner Income**:
        - Retail outlet subscriptions (basic/premium)
    
    #### Expenses
    - **Payroll (Payroll)**:
        - First 6 months: covered from initial investments
        - Months 7-12: 2,500,000₽/month
        - After 12 months: 3,500,000₽/month

    - **Marketing Expenses**:
        - First 6 months: fixed budget of 200,000₽/month
        - After 6 months: 5% of revenue
        - Efficiency: 200 new users per 100,000₽

    - **Infrastructure**: 
        - Basic costs of 200,000₽/month
        - Scaling with user growth

    #### ROI and Financial Indicators
    - **ROI Calculation** = (Total operating profit / Total operating expenses) × 100%
        - Operating expenses include:
            * Payroll
            * Marketing
            * Infrastructure
        - Do not include initial investments, as the model evaluates operational efficiency

    #### Taxation
    - **VAT (20%)**:
        - Charged on all types of revenue
        - Includes commissions, subscriptions, and income from expired points
    
    - **Corporate Income Tax (20%)**:
        - Base = Revenue - VAT - Operating expenses
        - Includes income from expired points
        - Features of accounting for expired points:
            * Points become income only after the confirmation period expires (default 2 months)
            * Income from expired points = Unconfirmed points × Expiration percentage
            * Fully included in the taxable base

    ### Scenarios and Their Features

    #### Standard Scenario
    - Initial users: 1,000
    - Conversion to active: 30%
    - Growth rate: 20% (year 1), 15% (year 2)
    - Average check: 2,800₽
    - Cashback rate: 12%

    #### Pessimistic Scenario
    - Initial users: 800
    - Conversion to active: 30%
    - Growth rate: 15% (year 1), 10% (year 2)
    - Average check: 2,500₽
    - Cashback rate: 15%

    #### Optimistic Scenario
    - Initial users: 1,200
    - Conversion to active: 45%
    - Growth rate: 25% (year 1), 15% (year 2)
    - Average check: 3,200₽
    - Cashback rate: 17%

    ### Model Management
    - All parameters are configurable in the Parameter Management section
    - Scenario comparison is available in the Scenario Analysis section
    - Supports the creation and saving of custom scenarios
    """)

if __name__ == "__main__":
    documentation_page()