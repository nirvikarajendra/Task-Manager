import streamlit as st


def init_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "token" not in st.session_state:
        st.session_state.token = None


def require_auth():
    init_session_state()
    if not st.session_state.logged_in or not st.session_state.token:
        st.warning("Please login first.")
        st.stop()


def logout():
    st.session_state.logged_in = False
    st.session_state.token = None
    st.switch_page("app.py")