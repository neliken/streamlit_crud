import streamlit as st
from utils.database import get_database
from bson.objectid import ObjectId

def run():
    st.subheader("Delete Record")
    db = get_database()
    collection = db["bank"]

    record_id = st.text_input("Enter Record ID to Delete")
    if st.button("Delete Record"):
        result = collection.delete_one({"_id": ObjectId(record_id)})
        if result.deleted_count > 0:
            st.success("Record deleted successfully.")
        else:
            st.warning("Record not found.")
