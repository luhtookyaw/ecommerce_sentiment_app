import streamlit as st
import pandas as pd
from utils.plots import plot_sentiment_distribution, plot_topic_vs_sentiment
from utils.load_model import predict_sentiment

# Load cleaned data
df = pd.read_csv("data/cleaned_reviews.csv")

st.title("E-Commerce Customer Satisfaction Dashboard & Sentiment Predictor")

# Sidebar filter
sentiment_filter = st.sidebar.selectbox("Filter by Sentiment", ["All", "positive", "neutral", "negative"])
topic_filter = st.sidebar.selectbox("Filter by Topic", ["All"] + sorted(df['review_topic'].unique().tolist()))

filtered_df = df.copy()
if sentiment_filter != "All":
    filtered_df = filtered_df[filtered_df['sentiment'] == sentiment_filter]
if topic_filter != "All":
    filtered_df = filtered_df[filtered_df['review_topic'] == topic_filter]

st.subheader("📊 Dashboard")
plot_sentiment_distribution(filtered_df)
plot_topic_vs_sentiment(filtered_df)

st.subheader("🤖 Predict Sentiment from Review")
user_input = st.text_area("Enter a review message:", "")
if st.button("Predict"):
    if user_input.strip():
        predicted = predict_sentiment(user_input)
        st.success(f"Predicted Sentiment: **{predicted.upper()}**")
    else:
        st.warning("Please enter some text.")
