# core/settings.py

import streamlit as st

# Retrieve your API key from Streamlit secrets or environment variables
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
