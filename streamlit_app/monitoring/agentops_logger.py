import agentops
from datetime import datetime

# Initialize AgentOps 
agentops.init(api_key="ff9c5c0c-6bb2-46fa-9e4e-9f78c22a258b")

# Starts a new AgentOps session
def start_session(session_id):
    log_event(event_type="session_start", details={"session_id": session_id})

#  Logs a custom event using AgentOps
def log_event(event_type, details=None):
    try:
        timestamp = datetime.now().isoformat()
        agentops.record_event(
            event_type=event_type,
            timestamp=timestamp,
            metadata=details
        )
        print(f"[AGENTOPS LOGGED] {event_type} at {timestamp}")
    except Exception as e:
        print(f"Failed to log event to AgentOps: {str(e)}")

def log_user_query(query, session_id):
    log_event("user_query", {"query": query, "session_id": session_id})

def log_llm_response(response, session_id, intent=None):
    log_event("llm_response", {"response": response, "session_id": session_id, "intent": intent})

def log_error(error_message, session_id):
    log_event("error", {"error_message": error_message, "session_id": session_id})

def end_session(session_id):
    agentops.end_session()
    print(f"[AGENTOPS] Session '{session_id}' ended and uploaded.")
