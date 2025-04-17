# This file for LangChain 3 flows (course recommendation, course Q&A, and career coaching) and extracting course name/topic from query
from ai_core.rag_pipeline import rag_response
from sentence_transformers import SentenceTransformer
from qdrant_client_instance import get_qdrant_client
import google.generativeai as genai
import re

# Initialize the embedding model and Qdrant client
client = get_qdrant_client()
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
llm = genai.GenerativeModel('gemini-2.0-flash')

# Function to safely generate content using LLM with error handling for any errors in generating
def safe_generate_content(prompt):
    try:
        response = llm.generate_content(prompt)
        # check if response is not None and has text attribute
        if response and hasattr(response, 'text'):
            return response.text.strip()  # Ensure text attribute exists
        else:
            return "No response generated or unexpected response format."
    except Exception as e:
        return f"Error generating response: {str(e)}"


# Flow 1: Course Recommendation & Course Details Retrieval based on the user's query
def course_recommendation_flow(query):
    embedded_query = embedding_model.encode(query)
    # Retrieve top 3 relevant courses
    return rag_response(query, embedded_query=embedded_query, client=client, top_k=3)


# Flow 2: Q&A About a Specific Course in the Dataset
def course_qa_flow(course_name, query):
    # Get details of the course and formulate context
    embedded_query = embedding_model.encode(query)
    context_str = rag_response(query, embedded_query=embedded_query, client=client, top_k=3, return_context_only=True)
    
    # Generate a more focused response based on course content
    prompt = f"""
    You're a helpful assistant providing information about the course '{course_name}'. 
    The course details are:
    {context_str}
    Now, answer the following question about this course: {query}
    """
    return safe_generate_content(prompt)


# Flow 3: Career Coaching - What’s After a Specific Course
def career_coaching_flow(course_name):
    # Get relevant courses and career paths based on the course name
    query = f"What careers can I pursue after taking {course_name}?"
    embedded_query = embedding_model.encode(query)
    context_str = rag_response(query, embedded_query=embedded_query, client=client, top_k=5, return_context_only=True)

    # Use the LLM to give career advice based on course context
    prompt = f"""
    You're a career coach. Based on the following course details, suggest potential career paths and next steps after completing the course '{course_name}'.
    Course Details: 
    {context_str}
    Suggest the best career options after completing this course.
    """
    return safe_generate_content(prompt)


# Helper function to extract course name/topic from query
def extract_course_name_from_query(query):
    # Check for course names in single quotes
    match = re.search(r"'(.*?)'", query)
    if match:
        return match.group(1).strip()
    # Look for known subjects in the query
    subjects = ["marketing", "data science", "python", "machine learning", "ai",
                "finance", "cybersecurity", "design", "cloud computing", "excel"]
    # convert query to lowercase for case-insensitive matching
    query_lower = query.lower()
    # apply for all subjects in query
    for subject in subjects:
        if subject in query_lower:
            return subject
    return None