# This file contains utility functions for authentication and user management using supabase
import os
from dotenv import load_dotenv
import requests

# Load environment variables 
load_dotenv()  

# supabase credentials
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

    try:
        # make a POST request to the supabase API to sign up the user
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.status_code, response.json()
    # handle any request exceptions
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Sign-up failed: {e}")
        return 400, {"message": "Sign-up failed. Please try again."}


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

    try:
        # make a POST request to the supabase API to sign in the user & retrieve the access token
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        token = data.get('access_token')
        # check if the token is present in the response  
        if token:
            return response.status_code, data
        else:
            return 401, {"message": "Invalid credentials."}
        # handle any request exceptions
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Sign-in failed: {e}")
        return 400, {"message": "Sign-in failed. Please try again."}


# Function to add course to the user's profile
def supabase_add_course(email, course_data):
    url = f"{SUPABASE_URL}/rest/v1/user_courses"
    payload = {
        "email": email,
        "course_title": course_data["course_title"],
        "subject": course_data["subject"],
        "level": course_data["level"],
        "url": course_data["url"]
    }
    headers = {
        "apikey": SUPABASE_KEY,
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    try:
        # make a POST request to the supabase API to add the course to the user's profile
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        # if course is added successfully, return success message
        if response.status_code == 201:
            return {"status": "success", "message": "Course added successfully."}
        # else return error occurred
        else:
            return {"status": "error", "message": response.json().get('message', 'Unknown error occurred.')}
        # handle any request exceptions
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to add course: {e}")
        return {"status": "error", "message": "Failed to add course. Please try again."}
    

# Function to fetch the user's courses from Supabase
def supabase_get_user_courses(email):
    url = f"{SUPABASE_URL}/rest/v1/user_courses?email=eq.{email}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Content-Type": "application/json",
    }
    # make a GET request to the supabase API to fetch the user's courses
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # raise an error for bad responses

        if response.status_code == 200:
            return response.json()
        else:
            return []
        # handle any request exceptions
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch user courses: {e}")
        return []
