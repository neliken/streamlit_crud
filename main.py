import streamlit as st
from modules import create, read, update, delete

def main():
    st.sidebar.title("CRUD App")
    menu = ["Read", "Create", "Update", "Delete"]
    choice = st.sidebar.selectbox("Select Operation", menu)

    if choice == "Create":
        create.run()
    elif choice == "Read":
        read.run()
    elif choice == "Update":
        update.run()
    elif choice == "Delete":
        delete.run()

if __name__ == "__main__":
    main()
