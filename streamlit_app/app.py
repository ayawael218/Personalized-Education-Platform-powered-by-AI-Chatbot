# this the main entry point for the streamlit app
import streamlit as st
from pages.home import home_page
from pages.login import login_page
from pages.signup import sign_up_page
from pages.chatbot import chatbot_page
from pages.add_course import add_course_page
from pages.view_courses import view_courses_page
from pages.navigate_course_material import navigate_course_materials_page

# Page configuration
st.set_page_config(page_title="AI Chatbot Platform", layout="wide")

# Initialize session state variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
            font-family: 'Arial', sans-serif;
            color: #333;
        }
        .sidebar .sidebar-content {
            background-color: #ffffff;
            color: #333;
        }
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
        .login-signup-button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 15px 30px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .login-signup-button:hover {
            background-color: #45a049;
        }
    </style>
""", unsafe_allow_html=True)

# Helper function to render a navigation button
def render_nav_button(label, key, page_name):
    is_active = st.session_state.page == page_name
    if is_active:
        st.markdown(f"<button class='nav-btn active-btn' disabled>{label}</button>", unsafe_allow_html=True)
    else:
        st.markdown(f"<button class='nav-btn'>{label}</button>", unsafe_allow_html=True)
        if st.button(label, key=key):
            st.session_state.page = page_name
            st.rerun()

# Navigation UI
nav_cols = st.columns(8)

with nav_cols[0]:
    render_nav_button("Home", "home_button", "Home")

with nav_cols[1]:
    render_nav_button("Login", "login_button", "Login")

with nav_cols[2]:
    render_nav_button("Sign Up", "signup_button", "Sign Up")

if st.session_state.authenticated:
    with nav_cols[3]:
        render_nav_button("Chatbot", "chatbot_button", "Chatbot")
    with nav_cols[4]:
        render_nav_button("Add Course", "add_course_button", "Add Course")
    with nav_cols[5]:
        render_nav_button("View Courses", "view_courses_button", "View Courses")
    with nav_cols[6]:
        render_nav_button("Navigate Course Materials", "navigate_course_materials_button", "Navigate Course Materials")
    with nav_cols[7]:
        if st.button("Logout", key="logout_button"):
            st.session_state.authenticated = False
            st.session_state.page = "Home"
            st.success("You have been logged out.")
            st.rerun()

# Page Routing
def ensure_authentication():
    if not st.session_state.authenticated:
        st.warning("Please log in to continue.")
        st.session_state.page = "Login"
        st.rerun()

# 
page = st.session_state.page

# render the selected page
if page == "Home":
    home_page()
elif page == "Login":
    login_page()
elif page == "Sign Up":
    sign_up_page()
elif page == "Chatbot":
    ensure_authentication()
    chatbot_page()
elif page == "Add Course":
    ensure_authentication()
    add_course_page()
elif page == "View Courses":
    ensure_authentication()
    view_courses_page()
elif page == "Navigate Course Materials":
    ensure_authentication()
    navigate_course_materials_page()
else:
    st.error("Page not found.")
