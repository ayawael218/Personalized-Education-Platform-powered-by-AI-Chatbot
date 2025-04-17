# this page for signing up new users
import streamlit as st
from auth.auth_utils import supabase_sign_up

def sign_up_page():
    st.title("Sign Up")

    # User input fields
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    # Sign-up button
    if st.button("Sign Up", key="signup_submit_button"):
        status_code, response = supabase_sign_up(email, password)

        if status_code == 200:
            st.success("Sign-up successful! You can now log in.")
        else:
            error_message = response.get("message", "An unexpected error occurred.")
            st.error(f"Sign-up failed: {error_message}")
