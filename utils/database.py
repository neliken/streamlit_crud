from pymongo import MongoClient
import streamlit as st

# Securely load MongoDB URI
def get_database():
    client = MongoClient(st.secrets["MONGO_URI"])
    db = client["database"]
    return db
