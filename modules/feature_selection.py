import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import VarianceThreshold
# import shap
import seaborn as sns
import matplotlib.pyplot as plt
from utils.data_loader import load_data

def run():
    st.title("Feature Importance and Selection")

    # Load data
    data = load_data()

    if data.empty:
        st.warning("No data available.")
        return

    # Dataset preview
    st.subheader("Dataset Preview")
    st.write(data.head())

    # User input for target and features
    st.subheader("Feature Selection Settings")
    target_col = st.selectbox("Select Target Column", options=data.columns)
    feature_cols = st.multiselect(
        "Select Feature Columns", options=[col for col in data.columns if col != target_col]
    )

    if not feature_cols or not target_col:
        st.warning("Please select a target and at least one feature column.")
        return

    X = data[feature_cols]
    y = data[target_col]

    # Feature Selection Methods
    st.subheader("Feature Selection Methods")

    # 1. Model-Based Selection (Linear Regression)
    if st.checkbox("Model-Based Selection (Linear Regression)"):
        model = LinearRegression()
        model.fit(X, y)
        importance = pd.DataFrame({
            "Feature": feature_cols,
            "Coefficient": model.coef_
        }).sort_values(by="Coefficient", ascending=False)
        st.write(importance)
        st.bar_chart(importance.set_index("Feature"))

    # 2. Gradient Boosting Feature Importance
    if st.checkbox("Gradient Boosting Feature Importance"):
        rf_model = GradientBoostingRegressor(random_state=42)
        rf_model.fit(X, y)
        importance = pd.DataFrame({
            "Feature": feature_cols,
            "Importance": rf_model.feature_importances_
        }).sort_values(by="Importance", ascending=False)
        st.write(importance)
        st.bar_chart(importance.set_index("Feature"))

    # 3. Filter Methods (Variance Threshold)
    if st.checkbox("Filter Methods (Low Variance Features)"):
        threshold = st.slider("Variance Threshold", 0.0, 1.0, 0.1)
        selector = VarianceThreshold(threshold=threshold)
        selector.fit(X)
        low_variance_features = [col for col, var in zip(feature_cols, selector.variances_) if var < threshold]
        st.write("Low Variance Features:", low_variance_features)
        st.write("Feature Variances:", pd.DataFrame(selector.variances_, index=feature_cols, columns=["Variance"]))

    # 4. Pearson Correlation
    if st.checkbox("Pearson Correlation"):
        st.write("Correlation Matrix")
        correlation_matrix = data[feature_cols + [target_col]].corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
        st.pyplot(plt)
