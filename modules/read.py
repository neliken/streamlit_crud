import streamlit as st
import pandas as pd
from utils.database import get_database
from utils.helpers import map_month_names

def run():
    st.subheader("View All Records")
    db = get_database()
    collection = db["economic_data"]

    # Sidebar for filters
    st.sidebar.header("Filters")

    # Load data from MongoDB
    records = list(collection.find().sort([("Year", 1), ("Month", 1)]))
    if records:
        df = pd.DataFrame(records)
        df["_id"] = df["_id"].astype(str)
        df = map_month_names(df)

        # Sidebar filters
        years = sorted(df["Year"].unique())
        selected_year = st.sidebar.multiselect("Select Year", options=years, default=[])

        quarters = sorted(df["Quarter"].unique())
        selected_quarter = st.sidebar.multiselect("Select Quarter", options=quarters, default=[])

        # Dynamically update months based on selected quarters
        if selected_quarter:
            filtered_months = df[df["Quarter"].isin(selected_quarter)]["Month"].unique()
            months = sorted(filtered_months)
        else:
            months = sorted(df["Month"].unique())

        selected_month = st.sidebar.multiselect("Select Month", options=months, default=[])

        # Apply filters
        filtered_df = df[
            ((df["Year"].isin(selected_year)) | (len(selected_year) == 0)) &
            ((df["Quarter"].isin(selected_quarter)) | (len(selected_quarter) == 0)) &
            ((df["Month"].isin(selected_month)) | (len(selected_month) == 0))
        ]

        # Display filtered data
        st.dataframe(filtered_df, use_container_width=True)

        # Display record count
        st.write(f"Total Records: {len(filtered_df)}")
    else:
        st.warning("No records found in the database.")
