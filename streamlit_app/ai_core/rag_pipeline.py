import google.generativeai as genai
from qdrant_client_instance import get_qdrant_client
from sentence_transformers import SentenceTransformer
from data_prepration.qdrant import retrieve_courses

# Initialize LLM and embedding model
genai.configure(api_key="AIzaSyBZ9E4RG96F90hTvjZbD0hdc9E7Sm_nOk0")
llm = genai.GenerativeModel('gemini-2.0-flash')
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def rag_response(user_query,embedded_query=None,client=None,top_k=3,return_context_only=False):
    if client is None:
        client = get_qdrant_client()

    if embedded_query is None:
        embedded_query = embedding_model.encode(user_query)

    relevant_courses = retrieve_courses(client, embedded_query, top_k=top_k)
    context_str = "\n\n".join([
        f"Title: {course['course_title']}\nDescription: {course['descriptions']}\nURL: {course['url']}"
        for course in relevant_courses
    ])

    if return_context_only:
        return context_str

    prompt = f"""
You're an intelligent educational assistant helping users with learning goals. Use the courses below to respond to the query.

Courses:
{context_str}

User query:
{user_query}

Respond concisely, helpfully, and clearly.
"""
    response = llm.generate_content(prompt)
    return response.text.strip()


