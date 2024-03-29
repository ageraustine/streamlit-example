import streamlit as st
import requests
import numpy as np
import os

API_URL =  os.environ["API_URL"]

headers = {
	"Authorization": "Bearer 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",
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
            response = query({"inputs": {"prompt":user_prompt,"duration":int(duration)}})
            audio = np.array(response[0]['generated_audio'])
	    audio = np.float32(audio)
            sample_rate = response[0]['sample_rate']
            st.audio(audio, format="audio/mp3", sample_rate=sample_rate)
