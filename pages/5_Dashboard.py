import streamlit as st
import streamlit.components.v1 as components
from utils.auth import get_authenticator

# --- AUTHENTICATION ---
authenticator = get_authenticator()
name, authentication_status, username = authenticator.login(location="main")

if authentication_status != True:
    st.stop()

authenticator.logout("Logout", "sidebar")

st.set_page_config(page_title="Power BI Dashboard", page_icon="images/images__1_-removebg-preview.png", layout="wide")
st.title("📥 Power BI Dashboard")

components.html(
    """
    <iframe src="https://app.powerbi.com/view?r=eyJrIjoiNzM0NDdkY2ItZjM2Yy00OTQzLWE0OGYtYTkyMmJiMDAxM2YzIiwidCI6Ijk5ZWViMDA5LWU3YTItNDdiNi05ZGVkLTAyOGNkY2MzMDBlNiIsImMiOjEwfQ%3D%3D" width="100%" height="600px" style="border:none;"></iframe>
    """,
    height=600,
)

if st.button("Go to Dashboard"):
    st.markdown("Redirecting... [Click here](https://app.powerbi.com/view?r=eyJrIjoiNzM0NDdkY2ItZjM2Yy00OTQzLWE0OGYtYTkyMmJiMDAxM2YzIiwidCI6Ijk5ZWViMDA5LWU3YTItNDdiNi05ZGVkLTAyOGNkY2MzMDBlNiIsImMiOjEwfQ%3D%3D)", unsafe_allow_html=True)