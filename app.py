import streamlit as st
import nltk
from transformers import pipeline
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

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

# Streamlit app function
def main():
    # Add theme options
    st.set_page_config(page_title="Healthcare Assistant Chatbot", layout="centered")
    st.sidebar.title("Settings")
    theme = st.sidebar.selectbox("Choose Theme", ["Light", "Dark", "Blue"])
    background = st.sidebar.color_picker("Pick a Background Color", "#FFFFFF")
    
    # Apply theme styles
    st.markdown(f"""
        <style>
        body {{background-color: {background}; color: black;}}
        </style>
        """, unsafe_allow_html=True)
    
    if theme == "Dark":
        st.markdown("""
            <style>
            body {color: white;}
            .stTextInput > div > div > input {background-color: #444; color: white;}
            </style>
            """, unsafe_allow_html=True)
    elif theme == "Blue":
        st.markdown("""
            <style>
            body {color: black;}
            </style>
            """, unsafe_allow_html=True)
    
    st.title("Healthcare Assistant Chatbot")
    user_input = st.text_input("How can I assist you today?")
    
    if st.button("Submit"):
        if user_input:
            st.write("**User:**", user_input)
            with st.spinner("Processing your query, please wait..."):
                response = healthcare_chatbot(user_input)
            st.success("**Healthcare Assistant:** " + response)
        else:
            st.warning("Please enter a message to get a response.")

if __name__ == "__main__":
    main()
