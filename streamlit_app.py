import streamlit as st
import requests

API_URL = "https://j7q348ccukmo1z0o.us-east-1.aws.endpoints.huggingface.cloud"

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
            st.text(response)
            audio = response.generated_audio
            st.audio(audio, format="audio/mp3", sample_rate=response.sample_rate)