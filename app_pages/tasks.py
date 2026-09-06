"""
pages/tasks.py
---------------
WHAT THIS FILE DOES:
Renders the full Task Management page: a form to create tasks, a
filterable table of all tasks, and edit/delete/status-update controls.

WHY IT EXISTS:
This is the core CRUD (create/read/update/delete) page for tasks.

HOW IT CONNECTS TO OTHER FILES:
- Called from app.py when the user selects "Tasks" in the sidebar.
- Uses database/tasks.py for all task CRUD operations.
- Uses database/projects.py and database/users.py to populate dropdowns.
- Uses utils/task_utils.py for validation and dataframe conversion.
"""

import streamlit as st
from datetime import date

from config import TASK_STATUSES, TASK_PRIORITIES
from database.tasks import (
    create_task, get_all_tasks, update_task, delete_task, update_task_status,
)
from database.projects import get_all_projects
from database.users import get_all_users
from utils.task_utils import tasks_to_dataframe, validate_task_fields


def render():
    st.title("✅ Tasks")

    projects = get_all_projects()
    users = get_all_users()
    project_options = {p["project_name"]: p["id"] for p in projects}
    user_options = {u["username"]: u["id"] for u in users}

    with st.expander("➕ Create Task", expanded=False):
        with st.form("create_task_form", clear_on_submit=True):
            title = st.text_input("Task Title")
            description = st.text_area("Description")

            c1, c2 = st.columns(2)
            with c1:
                project_name = st.selectbox(
                    "Project", options=list(project_options.keys()) or ["No projects yet"]
                )
                priority = st.selectbox("Priority", TASK_PRIORITIES, index=1)
            with c2:
                assigned_username = st.selectbox(
                    "Assigned User", options=list(user_options.keys()) or ["No users yet"]
                )
                status = st.selectbox("Status", TASK_STATUSES, index=0)

            due = st.date_input("Due Date", value=date.today())

            submitted = st.form_submit_button("Create Task")
            if submitted:
                error = validate_task_fields(title, due)
                if error:
                    st.error(error)
                elif not project_options or not user_options:
                    st.error("You need at least one project and one user before creating a task.")
                else:
                    success = create_task(
                        title=title,
                        description=description,
                        project_id=project_options[project_name],
                        assigned_to=user_options[assigned_username],
                        priority=priority,
                        status=status,
                        due_date=due,
                    )
                    if success:
                        st.success(f"Task '{title}' created successfully!")
                        st.rerun()
                    else:
                        st.error("Something went wrong while creating the task.")

    st.markdown("### All Tasks")

    f1, f2, f3 = st.columns(3)
    with f1:
        filter_status = st.selectbox("Filter by Status", ["All"] + TASK_STATUSES)
    with f2:
        filter_priority = st.selectbox("Filter by Priority", ["All"] + TASK_PRIORITIES)
    with f3:
        filter_project = st.selectbox("Filter by Project", ["All"] + list(project_options.keys()))

    all_tasks = get_all_tasks()

    if filter_status != "All":
        all_tasks = [t for t in all_tasks if t["status"] == filter_status]
    if filter_priority != "All":
        all_tasks = [t for t in all_tasks if t["priority"] == filter_priority]
    if filter_project != "All":
        all_tasks = [t for t in all_tasks if t["project_name"] == filter_project]

    if not all_tasks:
        st.info("No tasks match your filters yet.")
        return

    df = tasks_to_dataframe(all_tasks)
    st.dataframe(
        df[["id", "title", "project_name", "assigned_to_name", "priority", "status", "due_date"]],
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### Manage a Task")
    task_titles = {f"#{t['id']} — {t['title']}": t["id"] for t in all_tasks}
    selected_label = st.selectbox("Select a task to edit / delete / update", list(task_titles.keys()))
    selected_id = task_titles[selected_label]
    selected_task = next(t for t in all_tasks if t["id"] == selected_id)

    tab_edit, tab_status, tab_delete = st.tabs(["✏️ Edit", "🔄 Update Status", "🗑️ Delete"])

    with tab_edit:
        with st.form(f"edit_task_{selected_id}"):
            new_title = st.text_input("Task Title", value=selected_task["title"])
            new_desc = st.text_area("Description", value=selected_task.get("description") or "")

            c1, c2 = st.columns(2)
            with c1:
                current_project = selected_task.get("project_name")
                proj_names = list(project_options.keys())
                proj_index = proj_names.index(current_project) if current_project in proj_names else 0
                new_project_name = st.selectbox("Project", proj_names, index=proj_index, key=f"proj_{selected_id}")
                new_priority = st.selectbox(
                    "Priority", TASK_PRIORITIES,
                    index=TASK_PRIORITIES.index(selected_task["priority"]),
                    key=f"prio_{selected_id}",
                )
            with c2:
                current_user = selected_task.get("assigned_to_name")
                user_names = list(user_options.keys())
                user_index = user_names.index(current_user) if current_user in user_names else 0
                new_assigned_username = st.selectbox("Assigned User", user_names, index=user_index, key=f"user_{selected_id}")
                new_status = st.selectbox(
                    "Status", TASK_STATUSES,
                    index=TASK_STATUSES.index(selected_task["status"]),
                    key=f"status_{selected_id}",
                )

            new_due = st.date_input("Due Date", value=selected_task.get("due_date") or date.today(), key=f"due_{selected_id}")

            if st.form_submit_button("Save Changes"):
                error = validate_task_fields(new_title, new_due)
                if error:
                    st.error(error)
                else:
                    ok = update_task(
                        task_id=selected_id,
                        title=new_title,
                        description=new_desc,
                        project_id=project_options[new_project_name],
                        assigned_to=user_options[new_assigned_username],
                        priority=new_priority,
                        status=new_status,
                        due_date=new_due,
                    )
                    if ok:
                        st.success("Task updated successfully!")
                        st.rerun()
                    else:
                        st.error("Something went wrong while updating the task.")

    with tab_status:
        quick_status = st.selectbox(
            "New Status", TASK_STATUSES,
            index=TASK_STATUSES.index(selected_task["status"]),
            key=f"quickstatus_{selected_id}",
        )
        if st.button("Update Status", key=f"btnstatus_{selected_id}"):
            ok = update_task_status(selected_id, quick_status)
            if ok:
                st.success(f"Status updated to {quick_status}.")
                st.rerun()
            else:
                st.error("Could not update status.")

    with tab_delete:
        st.warning(f"This will permanently delete task '{selected_task['title']}'.")
        if st.button("Confirm Delete", key=f"btndelete_{selected_id}"):
            ok = delete_task(selected_id)
            if ok:
                st.success("Task deleted.")
                st.rerun()
            else:
                st.error("Could not delete task.")
