import streamlit as st
from pages.login import login_page
from pages.signup import sign_up_page
from pages.home import home_page
from pages.chatbot import chatbot_page

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Button styling
st.markdown("""
    <style>
        .nav-btn {
            background-color: #f0f0f0;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
            margin: 4px;
            cursor: pointer;
        }
        .nav-btn:hover {
            background-color: #e0e0e0;
        }
        .active-btn {
            background-color: #4CAF50 !important;
            color: white !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Navigation buttons
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.session_state.page == "Home":
        st.markdown("<button class='nav-btn active-btn' disabled>Home</button>", unsafe_allow_html=True)
    else:
        if st.button("Home"):
            st.session_state.page = "Home"
            st.rerun()
with col2:
    if st.session_state.page == "Login":
        st.markdown("<button class='nav-btn active-btn' disabled>Login</button>", unsafe_allow_html=True)
    else:
        if st.button("Login"):
            st.session_state.page = "Login"
            st.rerun()
with col3:
    if st.session_state.page == "Sign Up":
        st.markdown("<button class='nav-btn active-btn' disabled>Sign Up</button>", unsafe_allow_html=True)
    else:
        if st.button("Sign Up"):
            st.session_state.page = "Sign Up"
            st.rerun()
with col4:
    if st.session_state.page == "Chatbot":
        st.markdown("<button class='nav-btn active-btn' disabled>Chatbot</button>", unsafe_allow_html=True)
    else:
        if st.button("Chatbot"):
            st.session_state.page = "Chatbot"
            st.rerun()

# Page routing
if st.session_state.page == "Home":
    home_page()
elif st.session_state.page == "Login":
    login_page()
elif st.session_state.page == "Sign Up":
    sign_up_page()
elif st.session_state.page == "Chatbot":
    if st.session_state.authenticated:
        chatbot_page()
    else:
        st.warning("Please log in to access the chatbot.")
        st.session_state.page = "Login"
        st.rerun()
