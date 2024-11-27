import streamlit as st
import pandas as pd
from utils.database import get_database
from utils.helpers import map_month_names

def run():
    st.subheader("View All Records")
    db = get_database()
    collection = db["bank"]

    records = list(collection.find().sort([("Year", 1), ("Month", 1)]))
    if records:
        df = pd.DataFrame(records)
        df["_id"] = df["_id"].astype(str)
        df = map_month_names(df)
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No records found in the database.")
