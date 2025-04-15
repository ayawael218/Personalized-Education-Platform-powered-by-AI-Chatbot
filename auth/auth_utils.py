import os
from supabase import create_client, Client

# Supabase credentials (can be stored as environment variables for security)
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-supabase-url.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-anon-or-service-role-key")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def supabase_sign_up(email: str, password: str):
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        if response.get("user"):
            return 200, response
        else:
            return 400, {"message": "Sign-up failed. Try again."}
    except Exception as e:
        return 500, {"message": str(e)}

def supabase_sign_in(email: str, password: str):
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if response.get("user"):
            return 200, response
        else:
            return 401, {"message": "Invalid credentials."}
    except Exception as e:
        return 500, {"message": str(e)}
