import streamlit as st
from api import get_tasks, delete_task
from components.task_dialog import create_task_dialog, edit_task_dialog
from components.auth import logout, require_auth
import datetime

require_auth() 

PRIORITY_LABELS = {1: "Low", 2: "Medium", 3: "Medium", 4: "High", 5: "Critical"}

with st.sidebar:
    if st.button("Log out", use_container_width=True):
        logout()

st.title("📋 Task Manager Dashboard")

if st.button("➕ New Task", type="primary"):
    create_task_dialog()

def format_due(iso_date):
    return datetime.datetime.fromisoformat(iso_date).strftime("%b %d, %Y")

st.divider()

tasks = get_tasks(st.session_state.token)

if not tasks:
    st.info("No tasks yet. Create one to get started.")
else:
    for task in tasks:
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([4, 2, 1, 1])

            status = "✅ Done" if task["complete"] else "🕓 Pending"
            priority = PRIORITY_LABELS.get(task["priority"], task["priority"])

            c1.subheader(task["title"])
            c1.caption(task["description"])

            c2.caption(f"Due: {format_due(task['due_date'])}")
            c2.caption(f"Priority: {priority}")
            c2.caption(status)

            if c3.button("Edit", key=f"edit_{task['id']}"):
                edit_task_dialog(task)

            if c4.button("Delete", key=f"delete_{task['id']}"):
                delete_task(task["id"], st.session_state.token)