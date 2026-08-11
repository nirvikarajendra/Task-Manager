import streamlit as st
from api import register_user, login_user
from components.auth import init_session_state

st.set_page_config(page_title="Task Manager", page_icon="📋", layout="centered")

init_session_state()

if st.session_state.logged_in and st.session_state.token:
    st.success("You're already logged in.")
    if st.button("Go to Dashboard →", type="primary"):
        st.switch_page("pages/dashboard.py")
    st.stop()

st.title("📋 Task Manager")
st.caption("Organize your tasks, powered by AI")
st.divider()


f1, f2, f3 = st.columns(3)

with f1:
    with st.container(border=True):
        st.markdown("### ✅")
        st.markdown("**Track Tasks**")
        st.caption("Priority & due dates, all in one place")

with f2:
    with st.container(border=True):
        st.markdown("### 🗑️")
        st.markdown("**Stay Organized**")
        st.caption("Edit or delete tasks in one click")

with f3:
    with st.container(border=True):
        st.markdown("### 🤖")
        st.markdown("**AI Assistant**")
        st.caption("Create or search tasks by just asking")

st.write("")
st.divider()

_, mid, _ = st.columns([1, 2, 1])

with mid:
    st.markdown("**Already have an account?**")
    login_clicked = st.button("Log In", type="primary", use_container_width=True)

    st.markdown("**New here?**")
    register_clicked = st.button("Register", use_container_width=True)


@st.dialog("Login")
def login_dialog():
    email = st.text_input(label="Email")
    password = st.text_input(label="Password", type="password")

    if st.button("Submit", key="login_submit", type="primary"):
        if not all([email, password]):
            st.warning("Please fill in all fields.")
            return
        login_user({"email": email, "password": password})


@st.dialog("Register")
def registration_dialog():
    email = st.text_input(label="Email")
    username = st.text_input(label="Username")
    first_name = st.text_input(label="First Name")
    last_name = st.text_input(label="Last Name")
    password = st.text_input(label="Password", type="password")

    if st.button("Submit", key="register_submit", type="primary"):
        if not all([email, username, first_name, last_name, password]):
            st.warning("Please fill in all fields.")
            return

        payload = {
            "email": email,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
        }
        register_user(payload)
        st.info("Now log in using the Log In button.")


if login_clicked:
    login_dialog()

if register_clicked:
    registration_dialog()