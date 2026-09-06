"""
pages/my_tasks.py
-------------------
WHAT THIS FILE DOES:
Renders the "My Tasks" page: shows only tasks assigned to the
currently logged-in user, with filtering by status, priority, project
and due date.

WHY IT EXISTS:
Gives each user a focused view of just their own work, separate from
the full company-wide Tasks page.

HOW IT CONNECTS TO OTHER FILES:
- Called from app.py when the user selects "My Tasks" in the sidebar.
- Uses database/tasks.py -> get_user_tasks(user_id).
- Uses utils/task_utils.py for dataframe conversion.
"""

import streamlit as st

from config import TASK_STATUSES, TASK_PRIORITIES
from database.tasks import get_user_tasks
from utils.task_utils import tasks_to_dataframe


def render():
    st.title("🙋 My Tasks")

    user_id = st.session_state.get("user_id")
    my_tasks = get_user_tasks(user_id) if user_id else []

    if not my_tasks:
        st.info("You have no tasks assigned to you yet.")
        return

    project_names = sorted({t["project_name"] for t in my_tasks if t.get("project_name")})

    f1, f2, f3, f4 = st.columns(4)
    with f1:
        filter_status = st.selectbox("Status", ["All"] + TASK_STATUSES)
    with f2:
        filter_priority = st.selectbox("Priority", ["All"] + TASK_PRIORITIES)
    with f3:
        filter_project = st.selectbox("Project", ["All"] + project_names)
    with f4:
        sort_by_due = st.checkbox("Sort by due date", value=True)

    filtered = my_tasks
    if filter_status != "All":
        filtered = [t for t in filtered if t["status"] == filter_status]
    if filter_priority != "All":
        filtered = [t for t in filtered if t["priority"] == filter_priority]
    if filter_project != "All":
        filtered = [t for t in filtered if t["project_name"] == filter_project]
    if sort_by_due:
        filtered = sorted(filtered, key=lambda t: (t["due_date"] is None, t["due_date"]))

    if not filtered:
        st.info("No tasks match your filters.")
        return

    df = tasks_to_dataframe(filtered)
    st.dataframe(
        df[["title", "project_name", "priority", "status", "due_date"]],
        use_container_width=True,
        hide_index=True,
    )
