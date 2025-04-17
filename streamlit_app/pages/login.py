# this page for user login for both email/password and Github login
import streamlit as st
from auth.auth_utils import supabase_sign_in

def login_page():
    st.title("Login")

    # User input fields
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    # Login button
    if st.button("Login", key="login_submit_button"):
        status_code, response = supabase_sign_in(email, password)

        if status_code == 200:
            # Successful login
            st.session_state.authenticated = True
            st.session_state.user_email = email
            st.success("Login successful!")
            st.session_state.page = "Home"
            st.rerun()
        else:
            # Login failed
            st.error(f"Login failed: {response.get('message', 'Unknown error')}")
