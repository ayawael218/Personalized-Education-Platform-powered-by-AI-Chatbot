from .rag_pipeline import rag_response  
from data_prepration.qdrant import retrieve_courses  
import re
from qdrant_client_instance import get_qdrant_client
import google.generativeai as genai
from sentence_transformers import SentenceTransformer

client = get_qdrant_client()
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function for course recommendation
def course_recommendation_response(query, client , model):
    embedded_query = model.encode(query)
    relevant_courses = retrieve_courses(client, embedded_query, top_k=3)
    context = "\n".join(
        [
            f"Course Title: {course['title']}\n"
            f"Description: {course['description']}\n"
            f"Level: {course['level']}\n"
            f"Subject: {course['subject']}\n"
            f"URL: {course['url']}"
            for course in relevant_courses
        ]
    )
    response = rag_response(query)  # Use RAG pipeline
    return response

# Function to answer course-related questions
def answer_course_question(query, client , model):
    # Extract course name or topic from query
    course_name = extract_course_name_from_query(query)
    if not course_name:
        return "Sorry, I couldn't identify the course name from your query."
    
    # Retrieve course details and generate a response
    embedded_query = model.encode(query)
    relevant_courses = retrieve_courses(client, embedded_query, top_k=1)

    if not relevant_courses:
        return "Sorry, I couldn't find any course matching your query."
    
    course = relevant_courses[0]
    context = f"""
    Course Title: {course['title']}
    Description: {course['description']}
    Level: {course['level']}
    Subject: {course['subject']}
    URL: {course['url']}
    """
    response = rag_response(query)  # Use RAG pipeline
    return response

# Function for career coaching
def career_coaching_response(query,client , model):
    # Extract course name or topic from query
    course_name = extract_course_name_from_query(query)
    if not course_name:
        return "Sorry, I couldn't identify the course name from your query."
    
    # Retrieve course details and generate a response
    embedded_query = model.encode(query)
    relevant_courses = retrieve_courses(client, embedded_query, top_k=1)

    if not relevant_courses:
        return "Sorry, I couldn't find any course matching your query."
    
    course = relevant_courses[0]
    context = f"""
    Course Title: {course['title']}
    Subject: {course['subject']}
    Description: {course['description']}
    """
    prompt = f"""
    User Query: {query}
    Course Details:
    {context}
    Generate career coaching advice for someone who has completed this course. Include:
    - Potential job roles
    - Industries where this knowledge is applicable
    - Next steps for career advancement
    - Skills gained from the course
    """
    response = rag_response(prompt)  # Use RAG pipeline
    return response

# Helper function to extract course name/topic from query
def extract_course_name_from_query(query):
    # Check for course names in single quotes
    match = re.search(r"'(.*?)'", query)
    if match:
        return match.group(1).strip()
    # Fallback: Look for known subjects in the query
    subjects = ["marketing", "data science", "python", "machine learning", "ai",
                "finance", "cybersecurity", "design", "cloud computing", "excel"]
    query_lower = query.lower()
    for subject in subjects:
        if subject in query_lower:
            return subject
    return None