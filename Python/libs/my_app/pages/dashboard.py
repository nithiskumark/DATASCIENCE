import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from prophet import Prophet
import matplotlib.pyplot as plt

st.set_page_config(page_title="Data Science App", layout="wide")

st.title("📊 Smart ML + Timeseries")
name = st.session_state.get("username")
st.query_params = {"page": "dashboard", "user": name}

@st.cache_data
def load_data(file):
    return pd.read_excel(file)


uploaded_file = st.file_uploader("Upload your Orders file", type=["xlsx"], key="file_uploader")

if uploaded_file is None:
    st.info("Please upload a Excel file to continue.")
    st.stop()

df = load_data(uploaded_file)

st.subheader("Sample of your data")
st.dataframe(df.head())
st.subheader("Null values in given data")
st.table(df.isna().sum().to_dict())

df = df.dropna()
st.subheader("After removing Null values")
st.text(f"{df.shape} Rows x COlumns")

num_cols = df.select_dtypes(include=[np.number]).columns
cat_cols = df.select_dtypes(exclude=[np.number]).columns
date_cols = df.select_dtypes(include=['datetime', 'datetimetz']).columns
if len(date_cols) == 0:
    for col in df.columns:
        try:
            pd.datetime(df[col], errors='raise')
            df[date_cols]=pd.to_datetime(df[date_cols])
            date_cols.append(col)
        except:
            pass

st.subheader("Column Types")
st.table({
    "Numerical": num_cols,
    "Categorical": cat_cols,
    "Date": date_cols
})

st.subheader("Top 10")

selected_cat = st.selectbox("Select Category", cat_cols)

st.bar_chart(df[selected_cat].value_counts().sort_values(ascending=True).head(10))

typ = ["Numeric", "Timeseries"]
typ = st.selectbox("Dataset type", typ)
if typ == "Numeric":
    X = st.multiselect("select Features", num_cols)
    y = st.selectbox("Select target", num_cols)
    model = LinearRegression()
    if X and y:
        X = df[X]
        y = df[y]
        model.fit(X,y)
        st.success("Model Trained!")
        input = []
        for col in X:
            val = st.number_input(f"Enter {col}")
            input.append(val)

        if st.button("Predict"):
            pred = model.predict([input])
            st.write("Prediction: ", pred)

if typ == "Timeseries":
    ds = st.selectbox("Select features", date_cols)
    y = st.selectbox("Select target", num_cols)
    model = Prophet()
    if ds and y:
        prop = df[[ds,y]]
        prop = prop.rename(columns={
        ds: "ds",
        y: "y"})
        st.subheader("Sample input")
        st.dataframe(prop.tail())
        prop["ds"] =pd.to_datetime(prop["ds"])
        model.fit(prop)
        st.success("Model Trained!")
        periods = st.slider("Days to Forecast", 1, 365, 30)
        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)
        st.subheader("Forecast")
        st.write(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail())
        fig = model.plot(forecast)
        st.pyplot(fig)

    








