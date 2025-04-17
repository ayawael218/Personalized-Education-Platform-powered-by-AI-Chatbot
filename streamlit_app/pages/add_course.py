# this page for adding courses to the user's profile
import streamlit as st
import pandas as pd
from auth.auth_utils import supabase_add_course

# Load course data with specific columns
def load_courses(file_path="streamlit_app/data/cleaned_udemy_course_data.csv"):
    try:
        df = pd.read_csv(file_path)
        required_columns = ['course_title', 'subject', 'level', 'url']
        # check if cols exists
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Dataset is missing required columns.")
        return df[required_columns]
    # handle erros
    except FileNotFoundError:
        st.error("Course dataset not found. Please ensure the file exists at the specified path.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading the course data: {e}")
        return None


# Add Course Page
def add_course_page():
    st.title("Add Course")
    st.write("Select a course from the list below to add it to your profile.")

    # Load course data
    courses_df = load_courses()
    if courses_df is None:
        st.warning("Unable to load course data. Please contact the administrator.")
        return

    # Course selection
    course_titles = courses_df['course_title'].tolist()
    selected_course = st.selectbox("Available Courses", course_titles)

    if st.button("Add Course"):
        # Authentication check
        if not st.session_state.get("authenticated", False):
            st.warning("Please log in to add a course.")
            return

        email = st.session_state.get("user_email", None)
        if not email:
            st.warning("User email not found. Please log in again.")
            return

        # Get selected course details
        try:
            course_details = courses_df[courses_df['course_title'] == selected_course].iloc[0]
            course_data = {
                "course_title": course_details['course_title'],
                "subject": course_details['subject'],
                "level": course_details['level'],
                "url": course_details['url']
            }
        except IndexError:
            st.error("Selected course not found. Please try again.")
            return

        # Add course to Supabase
        response = supabase_add_course(email, course_data)

        if response.get("status") == "success":
            st.success(f"Course '{selected_course}' added successfully!")
        else:
            st.error(f"Failed to add course: {response.get('message', 'Unknown error')}")
