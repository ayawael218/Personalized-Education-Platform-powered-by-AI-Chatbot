from ai_core.langchain_flows import course_recommendation_response,answer_course_question,career_coaching_response,extract_course_name_from_query

from monitoring.agentops_logger import log_user_query, log_llm_response, log_error, end_session

# List of possible intents
INTENTS = {
    "qa": ["what is", "describe", "explain", "tell me about"],
    "career_coaching": ["career", "job", "path", "opportunity", "after completing"],
    "course_recommendation": ["recommend", "suggest", "beginner course", "what courses", "course on", "learning path"]
}

# In-memory conversation context store
conversation_context = {}

# Main router: Handles user query, detects intent, manages context, routes to the correct flow
def handle_conversation(query, session_id, client, model):
    global conversation_context

    try:
        # 1. Classify the intent
        intent = classify_intent(query)
        print(f"[Agent] Identified Intent: {intent}")

        # 2. Handle context (course name memory)
        course_name = handle_context(query, intent, session_id)
        print(f"[Agent] Resolved Course Name: {course_name}")

        # 3. Route query
        if intent == "qa":
            response = answer_course_question(query, client, model)
        elif intent == "career_coaching":
            response = career_coaching_response(query, client, model)
        elif intent == "course_recommendation":
            response = course_recommendation_response(query, client, model)
        else:
            response = "I'm sorry, I didn't understand your query. Could you please clarify?"

        return response

    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        print(f"[Agent Error] {error_msg}")
        log_error(error_msg, session_id)  
        return error_msg

    finally:
        # Optionally end session
        end_session(session_id)


def classify_intent(query):
    """
    Classify the intent of the user query based on predefined keywords.
    """
    query_lower = query.lower()
    for intent, keywords in INTENTS.items():
        if any(keyword in query_lower for keyword in keywords):
            return intent
    return "unknown"


def handle_context(query, intent, session_id):
    """
    Maintain course-related context across user turns.
    """
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
