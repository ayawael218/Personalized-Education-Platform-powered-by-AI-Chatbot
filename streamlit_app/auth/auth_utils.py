import os
from dotenv import load_dotenv
import requests

# Load environment variables 
load_dotenv()  

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

# Function to sign up with email and password
def supabase_sign_up(email, password):
    url = f"{SUPABASE_URL}/auth/v1/signup"
    payload = {
        "email": email,
        "password": password
    }
    headers = {
        "apikey": SUPABASE_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.status_code, response.json()

# Function to sign in with email and password
def supabase_sign_in(email, password):
    url = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"
    payload = {
        "email": email,
        "password": password
    }
    headers = {
        "apikey": SUPABASE_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.status_code, response.json()
