import streamlit as st #top-to-botton rerun model
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import time
import google.generativeai as genai

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
option = st.sidebar.selectbox("Choose Option", ["A", "B", "C"])
st.sidebar.write(f"You selected: {option}")

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
@st.cache_data #reused dont need to rerun everytime
def load(file):
    return pd.read_excel(file)
file=st.file_uploader(label="# **Order**",type="xlsx")
if file is not None:
    order=load(file)
    order["total price"] = pd.to_numeric(order["total price"])
    tr=order["total price"].sum().round(2)
    oc=len(order)
    st.metric(label="Total Revenue", value=f"₹{tr}", delta=f"{oc} Orders")
    order["order date"]=pd.to_datetime(order["order date"]).dt.date
    order = order.set_index("order date")
    daily_sales = order.groupby("order date")["total price"].sum()
    st.line_chart(daily_sales)
    fig, ax = plt.subplots()
    ax.plot(daily_sales)
    ax.set_title("Sales Trend")
    st.pyplot(fig)
    disc = order.groupby("order date")["discount"].sum()
    fig = px.line(disc)
    st.plotly_chart(fig)

name = st.text_input("ENTER YOUR NAME: ")
if name and st.checkbox("I agree to terms") and st.button("submit"):
    st.chat_message("assistant").write(f"Hello {name}! This is demo analytics")
    st.session_state["username"] = name
choice = st.radio("Select gender", ["Male", "Female", "Other"])
st.write("You selected:", choice)
country = st.selectbox("Choose country", ["India", "USA", "UK"])
st.write(country)
bio = st.text_area("Write about yourself")
st.write(bio)
age = st.slider("Select Age", 0, 100)
range_val = st.slider("Select Salary", 10000, 500000, (20000, 80000))
st.write(age,range_val)
import datetime
date = st.date_input("Select date")
age = (date.today().year - date.year)
st.write(f"You are **{age} years old**")
if "count" not in st.session_state:
    st.session_state.count = 0
st.session_state.count += 1 # the key "count" wont be cleared after rerun
st.write(f"Rerun count: {st.session_state.count}")

container1 = st.container ()#group UI elements #static
with container1:
    st.title("Hello!")
    st.write("This is grouped content")
    

placeholder = st.empty() #replace the content | a single slot that updates #dynamic

for i in range(5):
    placeholder.write(f"Updating value: {i}")

col1, col2 = st.columns(2)
with col1:
    st.header("Left")
    st.write("Left content")
with col2:
    st.header("Right")
    st.write("Right content")

tab1, tab2 = st.tabs(["Data", "Visualization"]) #switch btw diff views without reloading page
with tab1:
    st.write("Show dataset here")
with tab2:
    st.write("Show charts here")

with st.expander("See Details"):
    st.write("Hidden content")

name = st.text_input("Enter ur name:")
if not name:
    st.warning("Please enter your name!")
    st.stop() #script stops here with warning instead of full rerun
    #st.rerun() #manual refresh trigger
st.success(f"Welcome {name}")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login screen
if not st.session_state.logged_in: #if user not logged in
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.rerun() #rerun whole after login
        else:
            st.error("Invalid credentials")
    st.stop() #prevent dashboard from showing before login in
st.success("Welcome to dashboard!")

with st.form("User Info"): #batch i/p together and only trigger execution when clicks submit | no rerun when user types
    input1 = st.text_input("Name")
    input2 = st.number_input("Age")   
    submit = st.form_submit_button("Submit")
if submit:
    st.write(input1, input2)

if st.button("Save"):
    with st.spinner("saving..."):
        time.sleep(5)
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.05)
        progress.progress(1+i)
    st.toast("Saved!") #pop-up notifcation

api=st.secrets["AI_API"] #Api stored in streamlit/secrets.toml
genai.configure(api_key=api)
@st.cache_resource
def load_model():
    return genai.GenerativeModel("gemini-flash-latest")
model = load_model()
st.title("AI CHAT")
qn=st.chat_input("Ask your qn: ")
if qn:
    st.chat_message("user").write(qn)
    response = model.generate_content(qn)
    st.chat_message("assistant").write(response.text)



