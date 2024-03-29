import streamlit as st
import requests
import numpy as np
import os

# Try to get API_URL from environment variables, if not found set to a default value
try:
    API_URL = os.environ["API_URL"]
except KeyError:
    st.error("API_URL environment variable is not set.")
    st.stop()

# Try to get the Bearer token from environment variables, if not found set to a default value
try:
    BEARER_TOKEN = os.environ["BEARER_TOKEN"]
except KeyError:
    st.error("BEARER_TOKEN environment variable is not set.")
    st.stop()

headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json"
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Streamlit app
st.title("Songlabai")

# Input prompt from the user
user_prompt = st.text_input("Enter your prompt:", "")

# Input form
duration = st.number_input("Duration (in seconds)", min_value=10)

# Generate audio based on the user's prompt
if st.button("Generate Audio"):
    if user_prompt and duration:
        st.text("Generating audio...")
        response = query({"inputs": {"prompt": user_prompt, "duration": int(duration)}})
        audio = np.array(response[0]['generated_audio'], dtype=np.float32)
        sample_rate = response[0]['sample_rate']
        st.audio(audio, format="audio/wav", sample_rate=sample_rate)
