import streamlit as st
from api import create_task, update_task


@st.dialog("Create Task")
def create_task_dialog():
    st.subheader("Add Task")

    title = st.text_input(label="Title")
    description = st.text_input(label="Description")
    priority = st.number_input("Priority", min_value=1, max_value=5, value=1, step=1)
    complete = st.radio(label="Task completed", options=["No", "Yes"])
    due_date = st.date_input(label="Due Date")

    if st.button("Create Task", key="create_task_submit", type="primary"):
        if not title or not description:
            st.warning("Please fill in all fields.")
            return

        payload = {
            "title": title,
            "description": description,
            "priority": priority,
            "complete": complete == "Yes",
            "due_date": due_date.isoformat(),
        }

        create_task(payload, st.session_state.token)


@st.dialog("Edit Task")
def edit_task_dialog(task):

    title = st.text_input(label="Title", value=task["title"])
    description = st.text_input(label="Description", value=task["description"])
    priority = st.number_input(
        "Priority", min_value=1, max_value=5, value=task["priority"], step=1
    )
    complete = st.radio(
        label="Task completed",
        options=["No", "Yes"],
        index=1 if task["complete"] else 0,
    )
    due_date = st.date_input(label="Due Date", value=task["due_date"])

    if st.button("Save Changes", key=f"update_task_submit_{task['id']}", type="primary"):
        if not title or not description:
            st.warning("Please fill in all fields.")
            return

        payload = {
            "title": title,
            "description": description,
            "priority": priority,
            "complete": complete == "Yes",
            "due_date": due_date.isoformat(),
        }

        update_task(task["id"], payload, st.session_state.token)