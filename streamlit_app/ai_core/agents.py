from ai_core.langchain_flows import course_recommendation_flow, course_qa_flow, career_coaching_flow, extract_course_name_from_query
from monitoring.agentops_logger import log_user_query, log_llm_response, log_error, end_session

# List of possible intents (can be expanded)
INTENTS = {
    "qa": ["what is", "describe", "explain", "tell me about"],
    "career_coaching": ["career", "job", "path", "opportunity", "after completing"],
    "course_recommendation": ["recommend", "suggest", "beginner course", "what courses", "course on", "learning path"]
}

# In-memory conversation context store
conversation_context = {}

# Handles user query, detects intent, manages context, routes to the correct flow
def handle_conversation(query, session_id, client, model):
    global conversation_context

    try:
        # Classify the intent
        intent = classify_intent(query)
        print(f"[Agent] Identified Intent: {intent}")

        # Handle context (course name memory)
        course_name = handle_context(query, intent, session_id)
        print(f"[Agent] Resolved Course Name: {course_name}")

        # Route query based on intent
        if intent == "qa":
            # Call the Q&A flow for a specific course
            response = course_qa_flow(course_name, query)  # Use the updated flow
        elif intent == "career_coaching":
            # Call the Career Coaching flow for a specific course
            response = career_coaching_flow(course_name)  # Use the updated flow
        elif intent == "course_recommendation":
            # Call the Course Recommendation flow
            response = course_recommendation_flow(query)  # Use the updated flow
        else:
            response = "I'm sorry, I didn't understand your query. Could you please clarify?"

        # Log the response from LLM
        log_llm_response(response, session_id)
        return response

    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        print(f"[Agent Error] {error_msg}")
        log_error(error_msg, session_id)  
        return error_msg

    finally:
        end_session(session_id)


# Classify the intent of the user query based on predefined keywords
def classify_intent(query):
    query_lower = query.lower()
    for intent, keywords in INTENTS.items():
        if any(keyword in query_lower for keyword in keywords):
            return intent
    return "unknown"

# Maintain course-related context across user turns
def handle_context(query, intent, session_id):
    global conversation_context
    course_name = extract_course_name_from_query(query)

    if intent in ["qa", "career_coaching", "course_recommendation"]:
        if course_name:
            conversation_context[session_id] = {
                "last_course_name": course_name,
                "last_intent": intent
            }
        elif session_id in conversation_context:
            course_name = conversation_context[session_id].get("last_course_name")

    return course_name
