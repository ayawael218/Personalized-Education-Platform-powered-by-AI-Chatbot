import streamlit as st
from ai_core.agents import handle_conversation
from sentence_transformers import SentenceTransformer
from qdrant_client_instance import get_qdrant_client
from data_prepration.qdrant import retrieve_courses

# Initialize the embedding model and Qdrant client
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
qdrant_client = get_qdrant_client()

def chatbot_page():
    """
    Renders the chatbot interface using Streamlit.
    """
    st.title("AI-Powered Chatbot")
    st.write("Ask questions about courses or get career coaching based on your interests.")

    # Text input with key to maintain state across reruns
    query = st.text_input("Ask me anything:", key="user_query")

    # Initialize session state for chat response
    if "chat_response" not in st.session_state:
        st.session_state.chat_response = ""

    # Process the query if the submit button is clicked and query is not empty
    if st.button("Submit"):
        if query.strip():
            response = handle_conversation(query=query, session_id="default", client=qdrant_client, model=embedding_model)
            st.session_state.chat_response = response
        else:
            st.warning("Please enter a query")

    # Display the chat response, preserving it across reruns
    if st.session_state.chat_response:
        st.subheader("Response:")
        st.write(st.session_state.chat_response)
