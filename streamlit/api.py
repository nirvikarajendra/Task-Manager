import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_BASE_URL = os.getenv("API_URL")

def check_session_expired(response):
    if response.status_code == 401:
        st.session_state.logged_in = False
        st.session_state.token = None
        st.warning("Session expired. Please log in again.")
        st.switch_page("app.py")
        return True
    return False

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
        response = requests.post(f"{API_BASE_URL}/auth/login", json=payload)
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the server.")
        return

    if response.status_code == 200:
        data = response.json()
        st.session_state.token = data["token"]
        st.session_state.logged_in = True
        st.success(data["message"])
        st.switch_page("pages/dashboard.py")
    else:
        error_detail = response.json().get("detail", "Login failed.")
        st.error(error_detail)


def get_user(token):
    try:
        response = requests.get(f"{API_BASE_URL}/user/me", headers={"Authorization": f"Bearer {token}"})
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the server.")
        return
    
    if check_session_expired(response):
        return
    
    if response.status_code == 200:
        return response.json()
    else:
        error_detail = response.json().get("detail", "User not found.")
        st.error(error_detail)


def update_password(payload, token):
    try:
        response = requests.put(f"{API_BASE_URL}/user/password", json=payload, headers={"Authorization": f"Bearer {token}"})
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the server.")
        return

    if check_session_expired(response):
            return
    
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        error_detail = response.json().get("detail", "Password update failed.")
        st.error(error_detail)


def create_task(payload, token):
    try:
        response = requests.post(f"{API_BASE_URL}/task", json=payload, headers={"Authorization": f"Bearer {token}"})
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the server.")
        return
    
    if check_session_expired(response):
        return
    
    if response.status_code == 201:
        st.success("Task created successfully!")
        st.rerun()
    else:
        error_detail = response.json().get("detail", "Task creation failed")
        st.error(error_detail)


def get_tasks(token):
    try:
        response = requests.get(f"{API_BASE_URL}/task", headers={"Authorization": f"Bearer {token}"})
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the server.")
        return []

    if check_session_expired(response):
        return
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return []
    else:
        error_detail = response.json().get("detail", "Failed to get tasks")
        st.error(error_detail)
        return []


def get_task_by_id(task_id, token):
    try:
        response = requests.get(f"{API_BASE_URL}/task/{task_id}", headers={"Authorization": f"Bearer {token}"})
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the server.")
        return
    
    if check_session_expired(response):
        return
    
    if response.status_code == 200:
        return response.json()
    else:
        error_detail = response.json().get("detail", "Task not found.")
        st.error(error_detail)


def update_task(task_id, payload, token):
    try:
        response = requests.put(f"{API_BASE_URL}/task/{task_id}", json=payload, headers={"Authorization": f"Bearer {token}"})
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the server.")
        return
    
    if check_session_expired(response):
        return
    
    if response.status_code == 200:
        st.success("Task updated successfully!")
        st.rerun()
    else:
        error_detail = response.json().get("detail", "Task update failed")
        st.error(error_detail)


def delete_task(task_id, token):
    try:
        response = requests.delete(f"{API_BASE_URL}/task/{task_id}", headers={"Authorization": f"Bearer {token}"})
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the server.")
        return

    if check_session_expired(response):
            return
    
    if response.status_code == 204:
        st.success("Task deleted successfully!")
        st.rerun()
    else:
        error_detail = response.json().get("detail", "Task delete failed")
        st.error(error_detail)