import streamlit as st
from modules import read, create, update, delete, eda, preprocessing, modeling, feature_selection

menu_actions = {
    "View Records": read.run,
    "Add Record": create.run,
    "Edit Record": update.run,
    "Delete Record": delete.run,
    "Preprocessing": preprocessing.run,
    "EDA": eda.run,
    "Feature Selection": feature_selection.run,
    "Modeling": modeling.run
}

def main():
    st.sidebar.title("Prediction App")
    menu = list(menu_actions.keys())
    choice = st.sidebar.selectbox("Select Page", menu)
    menu_actions[choice]()

if __name__ == "__main__":
    main()
