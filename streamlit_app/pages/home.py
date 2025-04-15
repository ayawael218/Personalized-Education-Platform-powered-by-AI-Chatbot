import streamlit as st

def home_page():
    st.title("Welcome to the AI Chatbot Platform")
    st.markdown("""
        This platform allows you to:
        - **Explore courses** based on your interests
        - Get **career guidance**
        - Interact with an AI-powered **Chatbot**

        ---  
        Use the **navigation buttons at the top** to:
        -  Log in or Sign up
        -  Access the Chatbot *(requires login)*
    """)

    st.info("To get started, click on **Login** or **Sign Up** above.")
