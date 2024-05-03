import streamlit as st
import time
import os
from PIL import Image
# Make sure you import the correct library/module for Google Generative AI
import google.generativeai as genai
def ver():
# Set your Google API key here
    API_KEY = "AIzaSyB6gfvX21wsMuWfl9696C1Hh38zSo446b0"

    # Configure Google API
    os.environ["GOOGLE_API_KEY"] = API_KEY
    genai.configure(api_key=API_KEY)

    # Function to load OpenAI model and get responses
    def get_gemini_response(input_text, image, input_prompt):
        model = genai.GenerativeModel('gemini-pro-vision')
        if input_text != "":
            response = model.generate_content([input_text, image, input_prompt])
        else:
            response = model.generate_content([image, input_prompt])
        return response.text

    # Initialize Streamlit app
    # st.set_page_config(page_title="IT'S-MED.Ai")
    # st.header("S_CANCER")

    # # Display popup message
    # popup_placeholder = st.empty()
    # popup_placeholder.info("Welcome to IT'S-MED.Ai! This app provides information about medical conditions. Please upload an image and enter specific doubts to get started.")

    # # Delay to close the popup message
    # time.sleep(5)  # Adjust the duration as needed

    # # Clear the popup message
    # popup_placeholder.empty()

    # Input prompt
    input_text = st.text_input("USERNAME ", key="input")
    input_text2 = st.text_input("PASSWORD ", key="password")
    input_text3 = st.text_input("CONFIRM PASSWORD ", key="con")



    # File upload
    uploaded_file = st.file_uploader("UPLOAD THE CERTIFICATE...", type=["jpg", "jpeg", "png"])
    image = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

    # Button to generate response
    submit_button = st.button(" VERIFY")
    input_prompt1 = """Hello! Please evaluate the provided image. If it's a doctor's certificate, respond with 'The account will be available soon.' If not, kindly advise 'Please recheck your certificate.' Thank you!
    ."""

    # If button is clicked
    if submit_button:
        if image is not None:
            response = get_gemini_response(input_text, image, input_prompt1)
            st.subheader("RESUL IS:")
            st.write(response)
            print(response)
        else:
            st.warning("Please upload an image before generating response.")


ver()
