import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.database import get_database

def run():
    st.title("Data Preprocessing")

    db = get_database()
    collection = db["economic_data"]
    records = list(collection.find().sort([("Year", 1), ("Month", 1)]))
    if records:
      data = pd.DataFrame(records)
    else:
      data = pd.DataFrame()

    # Display missing values
    st.subheader("Missing Data Summary")
    missing_values = data.isnull().sum()
    missing_percentage = (missing_values / len(data)) * 100
    missing_summary = pd.DataFrame({
        "Feature": missing_values.index,
        "Missing Count": missing_values.values,
        "Missing Percentage": missing_percentage.values
    })
    st.write(missing_summary)

    # Button to fill missing values
    st.subheader("Handle Missing Data")
    if st.button("Fill Missing Values with Median and Update Database"):
        # Update missing values in dataframe
        for column in data.select_dtypes(include=["float64", "int64"]).columns:
            median_value = data[column].median()
            data[column] = data[column].fillna(median_value)

        # Update missing values in the database
        for index, row in data.iterrows():
            row_id = row["_id"]  # Assuming the `_id` field is the unique identifier
            updated_data = row.to_dict()
            collection.update_one({"_id": row_id}, {"$set": updated_data})

        st.success("All missing values have been filled with the median and updated in the database.")
    else:
        st.info("Click the button above to fill missing values and update the database.")

    # Display updated dataset (if updated)
    st.subheader("Updated Data Preview")
    st.write(data)
