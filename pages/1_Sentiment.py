import streamlit as st
import pandas as pd
from utils.plots import plot_sentiment_distribution, plot_topic_vs_sentiment
from utils.load_model import predict_sentiment
from utils.auth import get_authenticator

# --- AUTHENTICATION ---
authenticator = get_authenticator()
name, authentication_status, username = authenticator.login(location="main")

if authentication_status != True:
    st.stop()

authenticator.logout("Logout", "sidebar")

# --- Page Config ---
st.set_page_config(page_title="Sentiment Analysis", layout="wide")
st.title("🧠 Sentiment Analysis: Dashboard & Predictor")

# --- Load Data ---
@st.cache_data
def load_data():
    return pd.read_csv("data/cleaned_reviews.csv")

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Options")
sentiment_filter = st.sidebar.selectbox("Filter by Sentiment", ["All", "positive", "neutral", "negative"])
topic_filter = st.sidebar.selectbox("Filter by Topic", ["All"] + sorted(df['review_topic'].dropna().unique().tolist()))

filtered_df = df.copy()
if sentiment_filter != "All":
    filtered_df = filtered_df[filtered_df['sentiment'] == sentiment_filter]
if topic_filter != "All":
    filtered_df = filtered_df[filtered_df['review_topic'] == topic_filter]

# --- Dashboard Section ---
st.subheader("📊 Dashboard")
plot_sentiment_distribution(filtered_df)
plot_topic_vs_sentiment(filtered_df)

# --- Prediction Section ---
st.subheader("🤖 Predict Sentiment from Review")
user_input = st.text_area("Enter a review message:")

if st.button("Predict"):
    if user_input.strip():
        predicted = predict_sentiment(user_input)
        st.success(f"Predicted Sentiment: **{predicted.upper()}**")
    else:
        st.warning("Please enter some text.")
