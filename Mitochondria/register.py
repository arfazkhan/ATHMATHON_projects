import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Set your Google API key here
API_KEY = "AIzaSyCHhAtUIg_sq6BeKgLbSv5y_xZM-al_psE"

# Configure Google API
os.environ["GOOGLE_API_KEY"] = API_KEY
genai.configure(api_key=API_KEY)

# Function to load OpenAI model and get responses
def get_gemini_response(image, input_prompt):
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content([image, input_prompt])
    return response

def ver():
    # Counter for generating unique keys
    key_counter = 0

    # Input prompt
    email = st.text_input("Email", key=f"email_input_{key_counter}")

    name = st.text_input("Username", key=f"username_input_{key_counter}")
    key_counter += 1
    password = st.text_input("Password", type="password", key=f"password_input_{key_counter}")
    key_counter += 1
    password1 = st.text_input("Confirm Password", type="password", key=f"confirm_password_input_{key_counter}")

    if password != password1:
        st.warning("Passwords do not match.")
        return

    if not name or not password or not password1:
        st.warning("Please fill in all the fields.")
        return

    # File upload
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    image = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

    # Button to generate response
    submit_button = st.button("VERIFY NOW")
    
    # Assume you have a function that converts an image to a textual description
def image_to_text(image_path):
    # ... image processing and conversion to text ...
    return description

# Load an image and convert it to text
image_path = "path_to_your_image.jpg"
image_description = image_to_text(image_path)

# Use the image description as an input prompt
response = get_gemini_response(image_description, "additional input prompt")
    
    input_prompt1 = """ evaluate the provided image. If it looks like a doctor's certificate, respond with 'The account will be available soon.' If not, advise 'Please recheck your certificate.'"""

    # If button is clicked
    if submit_button:
        if image is not None:
            response = get_gemini_response(image, input_prompt1)
            st.subheader("Your condition is")
            st.warning(response)
            print(response)
        else:
            st.warning("Please upload an image before generating response.")

ver()