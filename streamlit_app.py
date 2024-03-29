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

genres = [
    "Pop",
    "Rock",
    "Hip Hop",
    "Jazz",
    "Blues",
    "Country",
    "Classical",
    "Electronic",
    "Reggae",
    "Folk",
    "R&B",
    "Metal",
    "Punk",
    "Indie",
    "Dance",
    "World",
    "Gospel",
    "Soul",
    "Funk",
    "Ambient",
    "Techno",
    "Disco",
    "House",
    "Trance",
    "Dubstep"
]
# Streamlit app
st.title("Komposer")
genre = st.selectbox("Select Genre:", genres)

energy_levels = ["Low", "Medium", "High"]
energy_level = st.radio("Energy Level:", energy_levels)

description = st.text_input("Description:", "")


# Generate audio based on the user's prompt
if st.button("Generate Audio"):
    prompt = f"{genre}, Energy: {energy_level}, Description: {description}"
    duration = st.slider("Duration (in seconds):", min_value=10, max_value=300, value=60, step=1)
    
    st.text("Generating audio...")
    response = query({"inputs": {"prompt": prompt, "duration": duration}})
    audio = np.array(response[0]['generated_audio'], dtype=np.float32)
    sample_rate = response[0]['sample_rate']
    st.audio(audio, format="audio/wav", sample_rate=sample_rate)
