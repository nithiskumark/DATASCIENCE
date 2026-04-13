import streamlit as st
import requests

st.markdown("<h1 style='text-align:center; color:purple;'>Learn FASTAPI</h1>",unsafe_allow_html=True)
st.subheader("Sum of 2 numbers")
col1, col2 = st.columns(2)

with col1:
    x = st.number_input("Enter X")

with col2:
    y = st.number_input("Enter Y")

if st.button("SUM"):
    response = requests.post(
        "http://127.0.0.1:8000/sum",
        json={"x":x,"y":y}

    )

    result = response.json()
    st.success(f"Result: {result['result']}")

st.subheader("Multiplication of 3 numbers")
a = st.number_input("Enter a: ",max_value=5000,min_value=0)
b = st.number_input("Enter b: ")
c = st.number_input("Enter c: ")

if st.button("Multiply"):
    response = requests.post(
        "http://127.0.0.1:8000/mul",
        json={"a":a, "b":b, "c":c}
    )
    result=response.json()
    st.success(f"Result: {result["result"]}")






