from pymongo import MongoClient
import streamlit as st

def get_database():
    client = MongoClient(st.secrets["MONGO_URI"])
    db = client["project"]
    return db
