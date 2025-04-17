# This page is the home page for our streamlit app
import streamlit as st

def home_page():
    # Custom CSS
    st.markdown("""
        <style>
            .welcome-header {
                font-size: 36px;
                font-weight: bold;
                text-align: center;
                margin-top: 50px;
                color: #333;
            }
            .welcome-subheader {
                font-size: 18px;
                text-align: center;
                margin-bottom: 40px;
                color: #555;
            }
        </style>
    """, unsafe_allow_html=True)

    # Header Texts
    st.markdown(
        '<div class="welcome-header">Welcome to Your Personalized AI Educational Platform</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="welcome-subheader">Explore courses, get career guidance, and interact with an AI-powered chatbot.</div>',
        unsafe_allow_html=True
    )

    # Login and Sign-Up Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login", key="home_login_button_unique", help="Log in to access your account"):
            st.session_state.page = "Login"
            st.rerun()

    with col2:
        if st.button("Sign Up", key="home_signup_button_unique", help="Create a new account"):
            st.session_state.page = "Sign Up"
            st.rerun()

    # GitHub OAuth Button 
    st.markdown('<div class="login-signup-container">', unsafe_allow_html=True)
    if st.button("Login with GitHub", key="github_oauth_button_unique", help="Log in using your GitHub account"):
        st.session_state.page = "Login"  # Placeholder for actual GitHub OAuth implementation
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
