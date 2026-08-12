import os
from google import genai
from api import create_task, get_tasks
import streamlit as st

client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

def make_tools(token: str):

    def create_task_tool(title: str, description: str, due_date: str, priority: int = 1) -> str:
        """Creates a new task.

        Args:
            title: The task title.
            description: The task description.
            due_date: Due date in YYYY-MM-DD format. Must be today's date or any date
                in the future. If the user doesn't specify a date, default to today.
                Always resolve relative dates (e.g. "tomorrow", "next Friday") using
                the current date provided in the system instructions — never guess a
                past or arbitrary year.
            priority: Priority from 1 (low) to 5 (critical).
        """
        payload = {
            "title": title,
            "description": description,
            "priority": priority,
            "complete": False,
            "due_date": due_date,
        }
        create_task(payload, token)
        return f"Created task '{title}'."

    def search_tasks_tool(query: str) -> str:
        """Searches the user's tasks by keyword.

        Args:
            query: Keyword to search for in task titles/descriptions.
        """
        tasks = get_tasks(token) or []
        if not tasks:
            return "The user has no tasks yet."

        if not query.strip():
            return "\n".join(f"- {t['title']} (due {t['due_date']})" for t in tasks)

        q = query.lower()
        matches = [
            t for t in tasks
            if q in t["title"].lower() or q in t["description"].lower()
        ]

        if matches:
            return "\n".join(f"- {t['title']} (due {t['due_date']})" for t in matches)

        all_tasks_text = "\n".join(
            f"- {t['title']}: {t['description']} (due {t['due_date']})" for t in tasks
        )
        return (
            f"No exact match for '{query}'. Here are all the user's tasks — "
            f"pick any that seem related to what they're asking about:\n{all_tasks_text}"
        )
    return [create_task_tool, search_tasks_tool]


def run_bot(prompt: str, token: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
        config={"tools": make_tools(token)},
    )
    return response.text