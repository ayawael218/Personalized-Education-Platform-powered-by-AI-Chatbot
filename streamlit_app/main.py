import logging
import os
from sentence_transformers import SentenceTransformer
from pipeline import prepare_or_load_data
from data_prepration.qdrant import retrieve_courses, ensure_courses_collection
from ai_core.rag_pipeline import rag_response
from ai_core.agents import handle_conversation
from monitoring.agentops_logger import start_session, log_user_query, log_llm_response, end_session
from qdrant_client_instance import get_qdrant_client

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Constants
INPUT_FILE = "/Sprints-BootCamp-Dec2024/Graduation Project/streamlit_app/data/udemy_course_data.csv"
OUTPUT_FILE = "/Sprints-BootCamp-Dec2024/Graduation Project/streamlit_app/data/cleaned_udemy_course_data.csv"
METADATA_FILE = "course_metadata.csv"
EMBEDDINGS_FILE = "course_embeddings.npy"

# Helper function to ensure Qdrant collection exists
def ensure_collection(client, vector_size):
    ensure_courses_collection(client, vector_size)

# Test Data Preparation
def test_data_preparation():
    logging.info("Testing data preparation...")

    # Prepare or load the data
    df, embeddings_matrix = prepare_or_load_data(INPUT_FILE, OUTPUT_FILE)

    # Ensure Qdrant collection exists
    client = get_qdrant_client()
    ensure_collection(client, embeddings_matrix.shape[1])  # Ensure collection is created

    # Verify metadata and embeddings files
    verify_file(METADATA_FILE, "Metadata")
    verify_file(EMBEDDINGS_FILE, "Embeddings")

    logging.info("Data preparation completed.")

# Helper function to verify file existence
def verify_file(file_path, file_type):
    if os.path.exists(file_path):
        logging.info(f"{file_type} file '{file_path}' created successfully.")
    else:
        logging.error(f"{file_type} file '{file_path}' not found!")

#  Function to test Querying the database and retrieve relevant courses
def test_qdrant_retrieval():
    logging.info("Testing Qdrant retrieval...")

    client = get_qdrant_client()
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Ensure Qdrant collection exists
    ensure_collection(client, 384)  # 384 is the vector size for MiniLM

    query = "What are some beginner courses on Python?"
    relevant_courses = retrieve_courses(client, query, model, top_k=3)

    if relevant_courses:
        logging.info("Retrieved Courses:")
        for course in relevant_courses:
            logging.info(f"Title: {course['title']}, Description: {course['description']}")
    else:
        logging.warning("No courses retrieved from Qdrant.")

# Function to verify that the RAG pipeline works
def test_rag_pipeline():
    logging.info("Testing RAG pipeline...")
    query = "What are some beginner courses on Python?"
    response = rag_response(query)
    logging.info(f"RAG Response: {response}")

# Function to test conversation handling and logging
def test_agents():
    logging.info("Testing Agents...")

    session_id = "user_123"
    start_session(session_id)

    # Test multiple queries
    test_queries = [
        "What are some beginner courses on Python?",
        "Can you tell me more about the first course?",
        "What career opportunities are available after completing this course?"
    ]
    
    for query in test_queries:
        log_user_query(query, session_id)
        response = handle_conversation(query, session_id, get_qdrant_client(), SentenceTransformer("all-MiniLM-L6-v2"))
        log_llm_response(response, session_id)
        logging.info(f"Conversation Response: {response}")

    end_session(session_id)


if __name__ == "__main__":
    try:
        test_data_preparation()
        test_qdrant_retrieval()
        test_rag_pipeline()
        test_agents()
        logging.info("All tests completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred during testing: {str(e)}")
