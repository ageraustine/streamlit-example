import streamlit as st
import requests
import numpy as np
import os
from pydub import AudioSegment

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

# Streamlit app title
st.title("Songlabai")

genres = [
    "Pop", "Rock", "Hip Hop", "Jazz", "Blues",
    "Country", "Classical", "Electronic", "Reggae",
    "Folk", "R&B", "Metal", "Punk", "Indie",
    "Dance", "World", "Gospel", "Soul", "Funk",
    "Ambient", "Techno", "Disco", "House", "Trance",
    "Dubstep"
]

genre = st.selectbox("Select Genre:", genres)

energy_levels = ["Low", "Medium", "High"]
energy_level = st.radio("Energy Level:", energy_levels)

description = st.text_input("Description:", "")

# Duration input
duration = st.slider("Duration (in seconds):", min_value=15, max_value=90, value=30, step=1)

# Generate audio based on the user's prompt
if st.button("Generate Audio"):
    prompt = f"{genre}, Energy: {energy_level}, Description: {description}"
    
    st.text("Generating audio...")
    response = requests.post(API_URL, headers=headers, json={"inputs": {"prompt": prompt, "duration": duration}})
    audio = np.array(response.json()[0]['generated_audio'], dtype=np.float32)
    sample_rate = response.json()[0]['sample_rate']
    st.audio(audio, format="audio/wav", sample_rate=sample_rate, start_time=0)

    # Post-processing options
    st.sidebar.title("Post-processing Options")

    apply_stereo = st.sidebar.checkbox("Apply Stereo Effect")
    reverse = st.sidebar.checkbox("Reverse Audio")
    change_speed = st.sidebar.checkbox("Change Speed")

    if change_speed:
        speed_factor = st.sidebar.slider("Speed Factor:", min_value=0.1, max_value=2.0, value=1.0, step=0.1)

    # Apply selected post-processing
    if apply_stereo or reverse or change_speed:
        st.text("Applying post-processing...")
        
        # Convert audio to pydub AudioSegment
        audio_segment = AudioSegment(audio.tobytes(), frame_rate=sample_rate, sample_width=audio.itemsize, channels=1)
        
        # Apply selected post-processing
        if apply_stereo:
            audio_segment = audio_segment.pan(-0.5).overlay(audio_segment.pan(0.5))
        
        if reverse:
            audio_segment = audio_segment.reverse()
        
        if change_speed:
            audio_segment = audio_segment.speedup(playback_speed=speed_factor)
        
        # Play the processed audio
        st.audio(audio_segment.raw_data, format="audio/wav", start_time=0)
