
import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv() 

API_BASE_URL = os.getenv("API_URL")

#auth api's
def register_user(payload):
    try:
        response = requests.post(f"{API_BASE_URL}/auth/register", json=payload)
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the server.")
        return

    if response.status_code == 201:
        data = response.json()
        st.success(f"{data['message']} (user_id: {data['user_id']})")
    else:
                
        error_detail = response.json().get("detail", "Registration failed.")
        st.error(error_detail)

def login_user(payload):
    try:
        response = requests.post(f'{API_BASE_URL}/auth/login', json=payload)
    except requests.exceptions.ConnectionError:
            st.error("Could not connect to the server.")
            return
            
    if response.status_code == 200:
        data = response.json()
        st.success(f"{data['message']} (token: {data['token']})")
        st.session_state.token = data['token']
    else:
        error_detail = response.json().get("detail", "Login failed.")
        st.error(error_detail)


"""
    #user api's
    def get_user(): 

    def update_password()

    #task api's
    def get_task()
        
    def get_tasks()

    def create_task()
        
    def update_task()
        
    def delete_task()

"""