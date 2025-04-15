import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables 

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Redirect user to GitHub OAuth authorization page
def oauth_login(provider):
    url = f"{SUPABASE_URL}/auth/v1/authorize"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

    # Request to redirect user to GitHub OAuth page
    response = requests.get(url, headers=headers, params={"provider": provider})
    
    if response.status_code == 200:
        print("Redirect user to: ", response.text)
    else:
        print("Error initiating OAuth:", response.status_code, response.text)

# Function to handle the OAuth response (after user authorizes via GitHub)
def handle_oauth_redirect(authorization_code, redirect_uri):
    url = f"{SUPABASE_URL}/auth/v1/token"
    payload = {
        "grant_type": "authorization_code",
        "code": authorization_code,  # This will be the code returned by GitHub
        "redirect_uri": redirect_uri,
    }

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # This will contain user session data
    else:
        print(f"Error fetching token: {response.status_code}")
        return None
