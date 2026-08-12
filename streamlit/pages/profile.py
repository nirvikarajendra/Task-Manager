import streamlit as st
from api import update_password, get_user
from components.auth import require_auth

require_auth()

token = st.session_state.token

user = get_user(token)

if user:
    st.title("My Profile")

    col1, col2 = st.columns(2) 
    with col1: 
        st.text_input( "First Name", value=user.get("first_name", ""), disabled=True ) 
        st.text_input( "Username", value=user.get("username", ""), disabled=True ) 
        st.text_input( "Email", value=user.get("email", ""), disabled=True ) 
    with col2: 
        st.text_input( "Last Name", value=user.get("last_name", ""), disabled=True ) 
        st.text_input( "Role", value=user.get("role", ""), disabled=True ) 
        status = "Active" if user.get("is_active") else "Inactive" 
        st.text_input( "Account Status", value=status, disabled=True ) 
    st.divider() 


@st.dialog("Update Password")
def update_password_dialog(token):

    current_password = st.text_input("Current Password", type='password')
    new_password = st.text_input("New Password", type='password')
    confirm_password = st.text_input("Confirm New Password", type='password')

    if st.button("Submit", key='change_password'):

        if not current_password or not new_password or not confirm_password:
            st.warning("Please fill in all fields.")
            return
        
        if new_password != confirm_password:
            st.error("New passwords do not match.")
            return
        
        payload = {
                "password" : current_password,
                "new_password" : confirm_password
        }

        update_password(payload, token) 

if st.button("Change Password"):
    update_password_dialog(token)