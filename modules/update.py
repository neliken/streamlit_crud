import streamlit as st
from utils.database import get_database
from utils.helpers import month_dropdown
from bson.objectid import ObjectId

def run():
    st.subheader("Update Record")
    db = get_database()
    collection = db["economic_data"]

    record_id = st.text_input("Enter Record ID to Update")
    if record_id:
        record = collection.find_one({"_id": ObjectId(record_id)})
        if record:
            with st.form("update_record_form"):
                year = st.number_input("Year", value=record["Year"], min_value=1900, max_value=2100, step=1)
                month = st.selectbox("Month", options=month_dropdown(), index=record["Month"] - 1, format_func=lambda x: x[1])[0]
                quarter = st.selectbox("Quarter", options=[1, 2, 3, 4], index=record["Quarter"] - 1)
                interest_rate_loans = st.number_input("Interest Rate (Loans)", value=record["Interest_Rate_Loans"], step=0.01)
                interest_rate_deposits = st.number_input("Interest Rate (Deposits)", value=record["Interest_Rate_Deposits"], step=0.01)
                annual_inflation_rate = st.number_input("Annual Inflation Rate", value=record["Annual_Inflation_Rate"], step=0.01)
                usd_mdl_exchange_rate = st.number_input("USD/MDL Exchange Rate", value=record["USD_MDL_Exchange_Rate"], step=0.01)
                unemployment_rate = st.number_input("Unemployment Rate", value=record["Unemployment_Rate"], step=0.01)
                submitted = st.form_submit_button("Update Record")

                if submitted:
                    updated_record = {
                        "Year": year,
                        "Month": month,
                        "Quarter": quarter,
                        "Interest_Rate_Loans": interest_rate_loans,
                        "Interest_Rate_Deposits": interest_rate_deposits,
                        "Annual_Inflation_Rate": annual_inflation_rate,
                        "USD_MDL_Exchange_Rate": usd_mdl_exchange_rate,
                        "Unemployment_Rate": unemployment_rate
                    }
                    result = collection.update_one({"_id": ObjectId(record_id)}, {"$set": updated_record})
                    if result.modified_count > 0:
                        st.success("Record updated successfully.")