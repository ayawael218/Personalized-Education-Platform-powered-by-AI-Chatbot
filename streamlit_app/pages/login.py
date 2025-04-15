import streamlit as st
from auth.auth_utils import supabase_sign_in

def login_page():
    st.title("Login")

    # User input for email and password
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Call the sign-in function
        status_code, response = supabase_sign_in(email, password)

        if status_code == 200:
            # Successful login
            st.session_state.authenticated = True
            st.session_state.page = "Chatbot"
            st.success("Login successful! Redirecting to chatbot...")
            st.rerun()  # Redirect to Chatbot page after successful login
        else:
            # Handle login error
            st.error(f"Sign-in failed: {response.get('message', 'Unknown error')}")
            print(f"Supabase error: {response}")  # Log the error to console
            st.session_state.authenticated = False  # Ensure authentication is set to False

