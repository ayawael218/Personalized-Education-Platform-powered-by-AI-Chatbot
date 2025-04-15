import streamlit as st
from auth.auth_utils import supabase_sign_up

def sign_up_page():
    st.title("Sign Up")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        status_code, response = supabase_sign_up(email, password)
        if status_code == 200:
            st.success("Sign-up successful! You can now log in.")
        else:
            st.error(f"Sign-up failed: {response['message']}")
