from data_prepration.qdrant import retrieve_courses
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import google.generativeai as genai

# Configure the Gemini API key
genai.configure(api_key="AIzaSyBZ9E4RG96F90hTvjZbD0hdc9E7Sm_nOk0")
model = genai.GenerativeModel('gemini-2.0-flash')

# Function to generate a response using the RAG pipeline
def rag_response(user_query):
    # Retrieve relevant courses from Qdrant locally
    relevant_courses = retrieve_courses(user_query, top_k=3)
    
    # Format the retrieved courses into a context string
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
    
    # Create a prompt for the LLM
    prompt = f"""
    User Query: {user_query}
    Relevant Courses:
    {context}
    Generate a concise and helpful response based on the above information.
    """
    
    # Generate a response using the LLM
    response = model.generate_content(prompt)
    return response.text

# Function to inspect embeddings by calculating cosine similarities with the first embedding
def inspect_embeddings(embeddings_matrix):
    if embeddings_matrix.size == 0:
        print("Embeddings matrix is empty.")
        return
    
    # Compare the first embedding with a few others
    sample_embedding = embeddings_matrix[0].reshape(1, -1)
    similarities = cosine_similarity(sample_embedding, embeddings_matrix[:5])  # Compare with first 5 embeddings
    
    print("Cosine Similarities with the First Embedding:")
    for i, sim in enumerate(similarities[0]):
        print(f"Course {i}: {sim}")