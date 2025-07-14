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

st.set_page_config(page_title="Delivery Performance", layout="wide")
st.title("🚚 Delivery Performance Dashboard")

# --- Load Data ---
@st.cache_data
def load_orders_data():
    orders = pd.read_csv("data/olist_orders_dataset.csv", parse_dates=[
        "order_purchase_timestamp", "order_approved_at",
        "order_delivered_carrier_date", "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ])
    items = pd.read_csv("data/olist_order_items_dataset.csv")
    products = pd.read_csv("data/olist_products_translated.csv")
    return orders, items, products

orders, items, products = load_orders_data()

# --- Merge for Delivery Delay Analysis ---
merged = orders.merge(items, on='order_id', how='left')
merged = merged.merge(products[['product_id', 'product_category_name']], on='product_id', how='left')

# --- Calculate Delivery Delays ---
merged = merged[merged['order_delivered_customer_date'].notna()]
merged['actual_delivery_days'] = (merged['order_delivered_customer_date'] - merged['order_purchase_timestamp']).dt.days
merged['estimated_delivery_days'] = (merged['order_estimated_delivery_date'] - merged['order_purchase_timestamp']).dt.days
merged['delivery_delay'] = merged['actual_delivery_days'] - merged['estimated_delivery_days']

# --- Filter Options ---
st.sidebar.header("📦 Filter Options")
selected_category = st.sidebar.selectbox("Select Category", ["All"] + sorted(merged['product_category_name'].dropna().unique().tolist()))

filtered = merged.copy()
if selected_category != "All":
    filtered = filtered[filtered['product_category_name'] == selected_category]

# --- Plot 1: Delivery Delay by Category ---
st.subheader("📊 Top 20 Average Delivery Delay by Product Category")

delay_by_cat = (
    merged.groupby('product_category_name')['delivery_delay']
    .mean()
    .sort_values()
    .reset_index()
    .dropna()
)

# Show only top 20 categories
delay_by_cat = delay_by_cat.head(20)

fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(data=delay_by_cat, x='delivery_delay', y='product_category_name', ax=ax1, palette="coolwarm")
ax1.set_xlabel("Average Delay (days)")
ax1.set_ylabel("Product Category")
st.pyplot(fig1)

# --- Plot 2: Actual vs Estimated Delivery Days ---
st.subheader("📈 Actual vs Estimated Delivery Time (in Days)")

fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.histplot(filtered['actual_delivery_days'], label='Actual', kde=True, color='green', bins=30)
sns.histplot(filtered['estimated_delivery_days'], label='Estimated', kde=True, color='orange', bins=30)
ax2.set_xlabel("Delivery Days")
ax2.legend()
st.pyplot(fig2)

# --- Plot 3: Delay Distribution ---
st.subheader("⏱️ Delivery Delay Distribution")

fig3, ax3 = plt.subplots(figsize=(8, 4))
sns.histplot(filtered['delivery_delay'], bins=30, kde=True, color='purple')
ax3.axvline(0, color='red', linestyle='--', label='On-Time')
ax3.set_xlabel("Delay (days)")
ax3.set_ylabel("Order Count")
ax3.legend()
st.pyplot(fig3)
