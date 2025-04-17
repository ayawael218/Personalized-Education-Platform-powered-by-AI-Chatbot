# this page for the chatbot interface (to be enhanced later)
import streamlit as st
from ai_core.agents import handle_conversation
from sentence_transformers import SentenceTransformer
from qdrant_client_instance import get_qdrant_client
from data_prepration.qdrant import retrieve_courses

# Initialize model and Qdrant client
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
qdrant_client = get_qdrant_client()

# Chatbot page with multi-turn conversation
def chatbot_page():
    st.title("AI-Powered Chatbot")
    st.write("Ask questions about courses or get career coaching based on your interests.")

    # Initialize session state for chat history
    if "chat_history" not in st.session_state:
        # Each message is a dict: {"role": "user"/"bot", "content": "..."}
        st.session_state.chat_history = []  

    # Input from user
    user_input = st.text_input("You:", key="user_input")

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Send") and user_input.strip():
            # Add user input to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            # Get bot response
            response = handle_conversation(
                query=user_input,
                session_id="default",
                client=qdrant_client,
                model=embedding_model
            )

            # Add bot response to chat history
            st.session_state.chat_history.append({"role": "bot", "content": response})

    with col2:
        if st.button("Clear Chat"):
            st.session_state.chat_history = []

    # Display the chat thread
    st.subheader("Chat")
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**Bot:** {msg['content']}")
