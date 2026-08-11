import streamlit as st
from api import register_user, login_user


st.subheader("Task Manager")

col1, col2 = st.columns(2)

with col1:
    register_clicked = st.button("Register")

with col2:
    login_clicked = st.button("Login")


@st.dialog("Register")
def registration_dialog():
    with st.container():
        email = st.text_input(label="Email Id")
        username = st.text_input(label="Username")
        first_name = st.text_input(label="First Name")
        last_name = st.text_input(label="Last Name")
        password = st.text_input(label="Password", type="password")
        
        if st.button("Submit", key="register_submit"):
            if not all([email, username, first_name, last_name, password]):
                st.warning("Please fill in all fields.")
                return
            
            payload = {
                "email": email,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "password": password
            }
            
            register_user(payload)

@st.dialog("Login")
def login_dialog():
    with st.container():
        email = st.text_input(label="Email Id")
        password = st.text_input(label="Password", type="password")

        if st.button("Submit", key="login_submit"):
            if not all([email, password]):
                st.warning("Please fill in all fields.")
                return
            
            payload = {
                "email": email,
                "password": password
            }
            login_user(payload)


if register_clicked:
    registration_dialog()

if login_clicked:
    login_dialog()