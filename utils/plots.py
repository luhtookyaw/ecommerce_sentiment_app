import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def plot_sentiment_distribution(df):
    fig, ax = plt.subplots()
    sns.countplot(x='sentiment', data=df, ax=ax)
    st.pyplot(fig)

def plot_topic_vs_sentiment(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.countplot(data=df, x='review_topic', hue='sentiment', ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)
