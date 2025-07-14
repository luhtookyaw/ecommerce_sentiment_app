import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.auth import get_authenticator

# --- AUTHENTICATION ---
authenticator = get_authenticator()
name, authentication_status, username = authenticator.login(location="main")

if authentication_status != True:
    st.stop()

authenticator.logout("Logout", "sidebar")

st.set_page_config(page_title="Customer Insights", layout="wide")
st.title("👤 Customer Behavior & Satisfaction Dashboard")

# --- Load Data ---
@st.cache_data
def load_data():
    customers = pd.read_csv("data/olist_customers_dataset.csv")
    orders = pd.read_csv("data/olist_orders_dataset.csv")
    reviews = pd.read_csv("data/reviews_with_topic.csv")
    return customers, orders, reviews

customers, orders, reviews = load_data()

# --- Merge Data ---
orders_reviews = pd.merge(orders, reviews, on="order_id", how="inner")
orders_customers = pd.merge(orders_reviews, customers, on="customer_id", how="inner")

# --- Plot 1: Orders by State ---
st.subheader("📍 Orders by Customer State")
state_counts = orders_customers["customer_state"].value_counts().reset_index()
state_counts.columns = ["State", "Order Count"]

fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(data=state_counts, x="Order Count", y="State", ax=ax1, palette="Blues_d")
st.pyplot(fig1)

# --- Plot 2: Repeat Purchase Rate ---
st.subheader("🔁 Repeat Customer Rate")
repeat_customers = (
    customers.groupby("customer_unique_id")["customer_id"]
    .nunique()
    .reset_index(name="order_count")
)
repeat_rate = (repeat_customers["order_count"] > 1).mean()

st.metric(label="Repeat Customer Rate", value=f"{repeat_rate*100:.2f}%")

fig2, ax2 = plt.subplots()
sns.histplot(repeat_customers["order_count"], bins=10, kde=False, color="teal")
ax2.set_title("Distribution of Orders per Unique Customer")
ax2.set_xlabel("Number of Orders")
ax2.set_ylabel("Number of Customers")
st.pyplot(fig2)

# --- Plot 3: Avg Review Score by State ---
st.subheader("⭐ Average Review Score by State")

avg_score = (
    orders_customers.groupby("customer_state")["review_score"]
    .mean()
    .reset_index()
    .sort_values("review_score", ascending=False)
)

fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.barplot(data=avg_score, x="review_score", y="customer_state", palette="viridis", ax=ax3)
ax3.set_xlabel("Average Review Score")
ax3.set_ylabel("Customer State")
st.pyplot(fig3)
