import streamlit as st
from utils.auth import get_authenticator

st.set_page_config(page_title="E-Commerce Analytics", page_icon="images/images__1_-removebg-preview.png", layout="wide")

authenticator = get_authenticator()
name, authentication_status, username = authenticator.login(location="main")

if authentication_status != True:
    st.stop()

authenticator.logout("Logout", "sidebar")

# --- Main Dashboard ---
st.title("📦 E-Commerce Customer Satisfaction Dashboard")

# --- Add Logo ---
st.image("images/images__1_-removebg-preview.png", width=300)  # Adjust width as needed

st.markdown("""
Welcome to the Olist E-Commerce Analytics App!

Use the sidebar to navigate between:
- **Sentiment Analysis**
- **Delivery Performance**
- **Customer Behavior**
- **Product Insights**
""")
