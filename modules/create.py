import streamlit as st
from utils.database import get_database
from utils.helpers import month_dropdown

def run():
    st.subheader("Add New Record")
    db = get_database()
    collection = db["bank"]

    with st.form("add_record_form"):
        year = st.number_input("Year", min_value=1900, max_value=2100, step=1)
        month = st.selectbox("Month", options=month_dropdown(), format_func=lambda x: x[1])[0]
        quarter = st.selectbox("Quarter", options=[1, 2, 3, 4])
        interest_rate_loans = st.number_input("Interest Rate (Loans)", step=0.01)
        interest_rate_deposits = st.number_input("Interest Rate (Deposits)", step=0.01)
        annual_inflation_rate = st.number_input("Annual Inflation Rate", step=0.01)
        usd_mdl_exchange_rate = st.number_input("USD/MDL Exchange Rate", step=0.01)
        unemployment_rate = st.number_input("Unemployment Rate", step=0.01)
        submitted = st.form_submit_button("Add Record")

        if submitted:
            new_record = {
                "Year": year,
                "Month": month,
                "Quarter": quarter,
                "Interest_Rate_Loans": interest_rate_loans,
                "Interest_Rate_Deposits": interest_rate_deposits,
                "Annual_Inflation_Rate": annual_inflation_rate,
                "USD_MDL_Exchange_Rate": usd_mdl_exchange_rate,
                "Unemployment_Rate": unemployment_rate
            }
            result = collection.insert_one(new_record)
            if result.inserted_id:
                st.success(f"Record added successfully with ID: {result.inserted_id}")
