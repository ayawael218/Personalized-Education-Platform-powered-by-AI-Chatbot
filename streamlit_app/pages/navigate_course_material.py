# this page for navigating course materials
import streamlit as st
import pandas as pd
from auth.auth_utils import supabase_get_user_courses

# Load course data
def load_courses(file_path="streamlit_app/data/cleaned_udemy_course_data.csv"):
    try:
        # Attempt to load the dataset
        df = pd.read_csv(file_path)
        # Ensure required columns exist
        required_columns = ['course_title', 'url', 'descriptions']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Dataset is missing required columns.")
        return df[required_columns]
    except FileNotFoundError:
        st.error("Course dataset not found. Please ensure the file exists at the specified path.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading the course data: {e}")
        return None


# Navigate Course Materials Page
def navigate_course_materials_page():
    st.title("Navigate Course Materials")
    st.write("Select a course to view its materials.")

    # Check if user is logged in
    if "user_email" not in st.session_state or not st.session_state.user_email:
        st.warning("Please log in to access your added courses.")
        return

    # Get user-added courses from Supabase
    email = st.session_state.user_email
    user_courses = supabase_get_user_courses(email)

    if not user_courses:
        st.info("You have not added any courses yet. Add courses from the 'Add Course' page.")
        return

    # Convert user courses to a DataFrame
    user_courses_df = pd.DataFrame(user_courses)

    # Merge with the full course dataset to get detailed information
    courses_df = load_courses()
    if courses_df is None:
        st.warning("Unable to load course data. Please contact the administrator.")
        return

    # Join user-added courses with full course details
    user_courses_with_details = pd.merge(
        user_courses_df, courses_df, left_on="course_title", right_on="course_title", how="inner"
    )

    # Select a course
    course_titles = user_courses_with_details['course_title'].tolist()
    selected_course = st.selectbox("Your Added Courses", course_titles)

    # Get course details
    try:
        course_details = user_courses_with_details[user_courses_with_details['course_title'] == selected_course].iloc[0]
        
        # Handle URL and Description
        course_url = course_details['url'] if 'url' in course_details else "URL not available"
        course_description = course_details['descriptions'] if 'descriptions' in course_details else "No description available."

        # Display course details
        st.subheader(f"Course: {selected_course}")
        st.markdown(f"**Description:** {course_description}")
        st.markdown(f"[Course Link]({course_url})")  # Clickable link to the course

        # Display course materials (keeping it blank for now)
        st.subheader("Course Materials")

        # Videos Section (blank for now)
        st.markdown("### Videos")
        st.write("No videos available for this course.") 

        # Quizzes Section (blank for now)
        st.markdown("### Quizzes")
        st.write("No quizzes available for this course.")  

    except IndexError:
        st.error("Selected course not found in the dataset. Please try again.")
