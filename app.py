import streamlit as st
import base64
import nltk
from transformers import pipeline
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import deque

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Load chatbot model
chatbot = pipeline("text-generation", model="distilgpt2")

# Function to handle chatbot responses
def healthcare_chatbot(user_input):
    user_input = user_input.lower()
    
    if "symptom" in user_input:
        return "Please consult a doctor for accurate medical advice."
    elif "appointment" in user_input:
        return "Would you like to schedule an appointment with the doctor?"
    elif "medication" in user_input:
        return "It's important to take prescribed medicines regularly. If you have concerns, consult your doctor."
    else:
        response = chatbot(user_input, max_length=100, num_return_sequences=1)
        return response[0]['generated_text']

# Function to set background image
def set_background(image_file):
    with open(image_file, "rb") as image:
        encoded_string = base64.b64encode(image.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string.decode()});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to set sidebar background image
def set_sidebar_background(image_file):
    with open(image_file, "rb") as image:
        encoded_string = base64.b64encode(image.read())
    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] {{
            background-image: url(data:image/png;base64,{encoded_string.decode()});
            background-size: cover;
        }}
        [data-testid="stSidebar"] * {{
            color: white;  /* Adjust text color based on your image for better readability */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Streamlit app function
def main():
    # Set page config
    st.set_page_config(page_title="Health Assistant", page_icon="🩺", layout="wide")

    # Add the background image for the main app
    set_background("green_leaf_theme.jpg")
    
    # Add the background image for the sidebar
    set_sidebar_background("sidebar_image.jpg")
    
    # Disclaimer message
    st.markdown(
        """
        **Disclaimer:** Please do not enter any sensitive or personal information into this application.
        The information provided here is for informational purposes only and is not a substitute for professional medical advice.
        """,
        unsafe_allow_html=True
    )

    # History of user inputs
    with st.sidebar:
        st.title("Previous Inputs")
        if 'history' not in st.session_state:
            st.session_state.history = deque(maxlen=5)
        
        for i, input_text in enumerate(st.session_state.history):
            st.write(f"{i+1}. {input_text}")

    st.title("Healthcare Assistant Chatbot")
    user_input = st.text_input("How can I assist you today?")
    
    # Submit and Clear response buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        submit = st.button("Submit")
    with col2:
        clear_response = st.button("Clear Last Response")

    # Display response if Submit button is clicked
    if submit:
        if user_input:
            st.write("**User:**", user_input)
            st.session_state.history.appendleft(user_input)
            with st.spinner("Processing your query, please wait..."):
                response = healthcare_chatbot(user_input)
            st.session_state['last_response'] = response
        else:
            st.warning("Please enter a message to get a response.")
    
    # Clear last response if Clear Last Response button is clicked
    if clear_response:
        st.session_state.pop('last_response', None)
        st.write("Last response cleared.")

    # Display the last response if it exists
    if 'last_response' in st.session_state:
        st.success("**Healthcare Assistant:** " + st.session_state['last_response'])

if __name__ == "__main__":
    main()
