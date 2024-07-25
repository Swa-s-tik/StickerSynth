import streamlit as st
import requests
import io
from PIL import Image
import os
import time

# Load environment variables
load_dotenv()

# Streamlit app configuration
st.set_page_config(page_title="Sticker Generator", page_icon="🎨")

# Hugging Face API setup
API_BASE_URL = "https://api-inference.huggingface.co/models/"
headers = {"Authorization": f"Bearer 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"}

# List of models to try
MODELS = [
    "prompthero/openjourney-v4",
    "stabilityai/stable-diffusion-2",
    "runwayml/stable-diffusion-v1-5"
]

def generate_sticker(prompt, max_retries=3):
    """
    Generate a sticker using Hugging Face Inference API based on the input text.
    Tries multiple models if one fails.
    """
    for model in MODELS:
        api_url = API_BASE_URL + model
        for attempt in range(max_retries):
            try:
                response = requests.post(api_url, headers=headers, json={"inputs": prompt})
                response.raise_for_status()
                image = Image.open(io.BytesIO(response.content))
                return image
            except requests.RequestException as e:
                st.warning(f"Error with model {model}, attempt {attempt + 1}: {str(e)}")
                if attempt == max_retries - 1 and model == MODELS[-1]:
                    st.error("All models and retries failed. Please try again later.")
                    return None
                time.sleep(2)  # Wait for 2 seconds before retrying
    return None

# Streamlit UI
st.title("Sticker Generator")

# User input
user_input = st.text_input("Enter text for your sticker:", "")

# Submit button
if st.button("Generate Sticker"):
    if user_input:
        with st.spinner("Generating your sticker... This may take a minute."):
            sticker = generate_sticker(user_input)
        
        if sticker:
            st.image(sticker, caption="Your generated sticker", use_column_width=True)
        else:
            st.error("Failed to generate sticker. Please try again later.")
    else:
        st.warning("Please enter some text for your sticker.")

# Add some information about the app
st.markdown("""
---
This app uses the Hugging Face Inference API with multiple text-to-image models to generate stickers based on your input text.
Enter any text, and we'll create a unique sticker for you!
""")
