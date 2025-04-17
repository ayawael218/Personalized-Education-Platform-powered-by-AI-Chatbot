# this page for viewing all courses (to be enhanced later)
import streamlit as st
import pandas as pd

# Load course data
def load_courses(file_path="streamlit_app/data/cleaned_udemy_course_data.csv"):
    try:
        df = pd.read_csv(file_path)
        required_columns = ['course_title', 'subject', 'level', 'url', 'is_paid']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Dataset is missing required columns.")
        return df[required_columns]
    except FileNotFoundError:
        st.error("Course dataset not found. Please ensure the file exists at the specified path.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading the course data: {e}")
        return None


# View Courses Page
def view_courses_page():
    st.title("View Courses")
    st.write("Browse and filter available courses below.")

    # Load course data
    courses_df = load_courses()
    if courses_df is None:
        st.warning("Unable to load course data. Please contact the administrator.")
        return

    # Sidebar Filters
    st.sidebar.header("Filters")
    # filter courses by subject , level and paid/free
    subjects = ["All"] + sorted(courses_df['subject'].unique().tolist())
    selected_subject = st.sidebar.selectbox("Subject", subjects)

    levels = ["All"] + sorted(courses_df['level'].unique().tolist())
    selected_level = st.sidebar.selectbox("Level", levels)

    is_paid_options = ["All", "Free", "Paid"]
    selected_is_paid = st.sidebar.selectbox("Paid/Free", is_paid_options)

    # Apply filters
    filtered_courses = courses_df.copy()
    if selected_subject != "All":
        filtered_courses = filtered_courses[filtered_courses['subject'] == selected_subject]
    if selected_level != "All":
        filtered_courses = filtered_courses[filtered_courses['level'] == selected_level]
    if selected_is_paid == "Free":
        filtered_courses = filtered_courses[filtered_courses['is_paid'] == False]
    elif selected_is_paid == "Paid":
        filtered_courses = filtered_courses[filtered_courses['is_paid'] == True]

    # Display filtered courses
    st.write(f"Showing {len(filtered_courses)} courses:")
    if len(filtered_courses) > 0:
        for _, row in filtered_courses.iterrows():
            col1, col2 = st.columns([3, 2])
            with col1:
                st.write(f"**{row['course_title']}**")
                st.caption(f"Subject: {row['subject']} | Level: {row['level']}")
            with col2:
                st.markdown(f"[Go to Course]({row['url']})", unsafe_allow_html=True)
    else:
        st.info("No courses match the selected filters.")
