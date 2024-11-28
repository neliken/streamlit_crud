import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from utils.data_loader import load_data

def run():
    st.title("Exploratory Data Analysis")

    # Load data
    data = load_data()

    # Correlation heatmap
    st.subheader("Correlation Heatmap")
    # Exclude specific columns (Year, Month, Quarter) before calculating the correlation matrix
    excluded_columns = ['Year', 'Month', 'Quarter']
    numeric_data = data.drop(columns=excluded_columns, errors='ignore')  # Drop only if the columns exist
    correlation_matrix = numeric_data.corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    st.pyplot(plt)

    # Scatterplot: Interest Rates
    st.subheader("Interest Rates Scatterplot")
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=data, x='Interest_Rate_Loans', y='Interest_Rate_Deposits')
    st.pyplot(plt)
