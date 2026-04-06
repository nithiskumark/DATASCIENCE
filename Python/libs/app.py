import streamlit as st #top-to-botton rerun model
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Data Science App",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={"About": "Nothing"}
)
st.title("App is Running...")
st.header("Sales Analysis")
st.subheader("Overview")
st.sidebar.title("Navigation")
st.sidebar.write("Welcome!")

df = pd.DataFrame({
    "Product": ["A", "B"],
    "Sales": [100, 200]
})

st.text("Sales data")  #raw text alone
st.write(df) #autodetect datatypes / smart rendering
st.markdown("""
            # Data Analysis
            -Analysis of sales data using $eda$
            **Nithis**
            """)

code='''
def sum(a, b):
    return a+b'''
st.code(code,language='python')

st.latex(r"\sum_{i=1}^{n} i^2") #maths
st.caption("Data updated hourly")

if st.button("click me"):
    st.write("Butoon clicked")

st.markdown(
    "<h3 style='color:red;'>Important</h3>",
    unsafe_allow_html=True
)

st.markdown(
    '<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQINKy32YNOikp5GtdfhzA3ta6bZpqhAFvJkQ&s" width="200">',
    unsafe_allow_html=True
)
st.image("https://cdn-icons-png.flaticon.com/512/5530/5530389.png",width=200)

data = {
    "name": "Nithis",
    "age": 25,
    "skills": ["ML", "Python"]
}
st.json(data)
st.dataframe(df, use_container_width=True)
st.table(df)
st.metric(label="Revenue", value="₹300", delta="+5%")
edited_df = st.data_editor(df)
tr = edited_df["Sales"].sum()
st.metric(label="Total Revenue", value=f"₹{tr}", delta=f"+{tr-300}%")

data= pd.DataFrame(
    np.random.randn(20,2),
    columns=["Sales", "Profit"]
)
st.line_chart(data)
st.altair_chart(data)
st.bar_chart(data)
file=st.file_uploader("## **Order**")
if file is not None:
    order = pd.read_excel(file)
    tr=order["total price"].sum().round(2)
    oc=len(order)
    st.metric(label="Total Revenue", value=f"₹{tr}", delta=f"{oc} Orders")
    order["order date"]=pd.to_datetime(order["order date"]).dt.date
    order = order.set_index("order date")
    daily_sales = order.groupby("order date")["total price"].sum()
    st.line_chart(daily_sales)
    
