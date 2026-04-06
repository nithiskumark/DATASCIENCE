import streamlit as st

st.title("📊 Dashboard")
st.write("This is dashboard page")
name = st.session_state.get("username")
st.query_params = {"page": "dashboard", "user": name}

