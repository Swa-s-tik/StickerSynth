import streamlit as st
import requests
import io
from PIL import Image
import time

# Streamlit app configuration
st.set_page_config(page_title="Sticker Generator", page_icon="🎨", layout="wide")

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

# Custom CSS
st.markdown("""
<style>
    .sticker-card {
        border: 2px solid #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .title-text {
        font-size: 48px;
        font-weight: bold;
        color: #4a4a4a;
        text-align: center;
        margin-bottom: 30px;
    }
    .subtitle-text {
        font-size: 24px;
        color: #6c757d;
        text-align: center;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Streamlit UI
st.markdown('<p class="title-text">🎨 StickerSynth</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Create unique stickers with AI-powered text-to-image generation!</p>', unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="sticker-card">', unsafe_allow_html=True)
    user_input = st.text_input("Enter text for your sticker:", "")
    if st.button("Generate Sticker"):
        if user_input:
            with st.spinner("Generating your sticker... This may take a minute."):
                sticker = generate_sticker(user_input)
            
            if sticker:
                st.success("Sticker generated successfully!")
                st.image(sticker, caption="Your generated sticker", use_column_width=True)
            else:
                st.error("Failed to generate sticker. Please try again later.")
        else:
            st.warning("Please enter some text for your sticker.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="sticker-card">', unsafe_allow_html=True)
    st.subheader("How it works")
    st.write("""
    1. Enter your desired text in the input field.
    2. Click the 'Generate Sticker' button.
    3. Wait for a moment while our AI creates your unique sticker.
    4. Your generated sticker will appear on the left side of the screen.
    """)
    st.subheader("About")
    st.write("""
    This app uses the Hugging Face Inference API with multiple text-to-image models to generate stickers based on your input text.
    We use state-of-the-art AI models to create unique and creative stickers just for you!
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
---
<p style='text-align: center; color: #6c757d;'>
    Created with ❤️ by Your Name | 
    <a href='https://github.com/yourusername' target='_blank'>GitHub</a> | 
    <a href='https://twitter.com/yourusername' target='_blank'>Twitter</a>
</p>
""", unsafe_allow_html=True)
