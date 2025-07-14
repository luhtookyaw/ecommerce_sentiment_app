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

st.set_page_config(page_title="Product Analysis", layout="wide")
st.title("📦 Product Category Insights")

# --- Load Data ---
@st.cache_data
def load_data():
    items = pd.read_csv("data/olist_order_items_dataset.csv")
    products = pd.read_csv("data/olist_products_translated.csv")
    reviews = pd.read_csv("data/reviews_with_topic.csv")
    orders = pd.read_csv("data/olist_orders_dataset.csv")
    return items, products, reviews, orders

items, products, reviews, orders = load_data()

# --- Merge Data ---
merged = items.merge(products, on="product_id", how="left")
merged = merged.merge(orders[["order_id", "customer_id"]], on="order_id", how="left")
merged = merged.merge(reviews[["order_id", "review_score", "sentiment"]], on="order_id", how="left")

# --- Plot 1: Top-Selling Categories ---
st.subheader("🏆 Top-Selling Product Categories")

top_categories = (
    merged["product_category_name"]
    .value_counts()
    .head(15)
    .reset_index()
)
top_categories.columns = ["Category", "Order Count"]

fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(data=top_categories, x="Order Count", y="Category", palette="crest", ax=ax1)
st.pyplot(fig1)

# --- Plot 2: Avg Review Score by Category ---
st.subheader("⭐ Average Review Score by Category")

avg_score = (
    merged.groupby("product_category_name")["review_score"]
    .mean()
    .dropna()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
)
avg_score.columns = ["Category", "Avg Review Score"]

fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(data=avg_score, x="Avg Review Score", y="Category", palette="YlGn", ax=ax2)
st.pyplot(fig2)

# --- Plot 3: Sentiment Distribution by Category ---
st.subheader("📊 Sentiment Distribution by Category")

category_sentiment = (
    merged.groupby(["product_category_name", "sentiment"])
    .size()
    .reset_index(name="count")
)

# Only top categories
top_cats = top_categories["Category"].tolist()
category_sentiment = category_sentiment[category_sentiment["product_category_name"].isin(top_cats)]

fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.barplot(
    data=category_sentiment,
    x="product_category_name",
    y="count",
    hue="sentiment",
    ax=ax3
)
ax3.set_xlabel("Product Category")
ax3.set_ylabel("Count")
ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45, ha="right")
st.pyplot(fig3)
