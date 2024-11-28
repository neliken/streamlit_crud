import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
from utils.data_loader import load_data

def run():
    st.title("Modeling and Predictions")

    # Load data
    data = load_data()

    if data.empty:
        st.error("No data available. Please ensure the database is populated.")
        return

    # Feature and Target Selection
    st.sidebar.header("Feature and Target Selection")
    features = st.sidebar.multiselect(
        "Select Features",
        options=data.columns,
        default=['Interest_Rate_Deposits', 'Annual_Inflation_Rate', 'USD_MDL_Exchange_Rate', 'Unemployment_Rate']
    )
    target = st.sidebar.selectbox(
        "Select Target",
        options=data.columns,
        index=data.columns.tolist().index('Interest_Rate_Loans')
    )

    if not features or not target:
        st.warning("Please select at least one feature and a target variable.")
        return

    X = data[features]
    y = data[target]

    # Split data
    st.sidebar.header("Train-Test Split")
    test_size = st.sidebar.slider("Test Set Percentage", min_value=10, max_value=50, step=5, value=20) / 100
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    # Model Selection
    st.sidebar.header("Model Selection")
    model_choice = st.sidebar.selectbox("Choose a Model", ["Gradient Boosting", "Random Forest", "Linear Regression"])

    # Train the model with default parameters (Before Tuning)
    if model_choice == "Gradient Boosting":
        model_default = GradientBoostingRegressor()
    elif model_choice == "Random Forest":
        model_default = RandomForestRegressor()
    elif model_choice == "Linear Regression":
        model_default = LinearRegression()

    model_default.fit(X_train, y_train)
    y_pred_default = model_default.predict(X_test)
    mse_default = mean_squared_error(y_test, y_pred_default)
    mae_default = mean_absolute_error(y_test, y_pred_default)
    r2_default = r2_score(y_test, y_pred_default)

    # Hyperparameter Tuning
    st.sidebar.header("Model Hyperparameters")
    if model_choice == "Gradient Boosting":
        n_estimators = st.sidebar.slider("Number of Estimators", 50, 500, step=50, value=100)
        learning_rate = st.sidebar.slider("Learning Rate", 0.01, 0.5, step=0.01, value=0.1)
        max_depth = st.sidebar.slider("Max Depth", 1, 10, step=1, value=3)

        model_tuned = GradientBoostingRegressor(
            n_estimators=n_estimators, learning_rate=learning_rate, max_depth=max_depth, random_state=42
        )

    elif model_choice == "Random Forest":
        n_estimators = st.sidebar.slider("Number of Estimators", 50, 500, step=50, value=100)
        max_depth = st.sidebar.slider("Max Depth", 1, 20, step=1, value=10)

        model_tuned = RandomForestRegressor(
            n_estimators=n_estimators, max_depth=max_depth, random_state=42
        )

    elif model_choice == "Linear Regression":
        model_tuned = LinearRegression()  # No tuning parameters for Linear Regression

    # Train and evaluate the tuned model
    model_tuned.fit(X_train, y_train)
    y_pred_tuned = model_tuned.predict(X_test)
    mse_tuned = mean_squared_error(y_test, y_pred_tuned)
    mae_tuned = mean_absolute_error(y_test, y_pred_tuned)
    r2_tuned = r2_score(y_test, y_pred_tuned)

    # Compare Before and After Tuning
    st.subheader("Performance Comparison")
    comparison = pd.DataFrame({
        "Metric": ["Mean Squared Error", "Mean Absolute Error", "R² Score"],
        "Before Tuning": [mse_default, mae_default, r2_default],
        "After Tuning": [mse_tuned, mae_tuned, r2_tuned]
    })
    st.write(comparison)

    # Feature Importance (if applicable)
    if hasattr(model_tuned, "feature_importances_"):
        st.subheader("Feature Importance (After Tuning)")
        feature_importance = pd.DataFrame({
            "Feature": features,
            "Importance": model_tuned.feature_importances_
        }).sort_values(by="Importance", ascending=False)

        st.write(feature_importance)

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(feature_importance["Feature"], feature_importance["Importance"], color='skyblue')
        ax.set_title("Feature Importance")
        ax.set_ylabel("Importance Score")
        ax.set_xticks(range(len(feature_importance["Feature"])))
        ax.set_xticklabels(feature_importance["Feature"], rotation=45)
        st.pyplot(fig)

    # Scatterplot of Predictions After Tuning
    st.subheader("Predictions vs Actual (After Tuning)")
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(y_test, y_pred_tuned, alpha=0.7, label="Predictions")
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", lw=2, label="Ideal Fit")
    ax.set_title("Predictions vs Actual")
    ax.set_xlabel("Actual")
    ax.set_ylabel("Predicted")
    ax.legend()
    st.pyplot(fig)

     # Prepare input data for the next year
    st.subheader("Predict for the Next Year")
    last_year = data['Year'].max()  # Find the latest year in the dataset
    next_year = last_year + 1

    st.write(f"Predicting values for the year: {next_year}")

    # Allow users to input feature values for the next year
    input_data = {}
    for feature in features:
        input_value = st.number_input(f"Enter {feature} for {next_year}", value=float(data[feature].mean()))
        input_data[feature] = input_value

    # Predict button
    if st.button("Predict Next Year Values"):
        input_df = pd.DataFrame([input_data])  # Create a DataFrame for the input data
        prediction = model_tuned.predict(input_df)[0]  # Predict using the trained model
        st.success(f"The predicted {target} value for {next_year} is: {prediction:.2f}")
