"""
pages/projects.py
-------------------
WHAT THIS FILE DOES:
Renders the Projects page: a form to create projects, and a
professional card-based list of existing projects with edit/delete.

WHY IT EXISTS:
Gives users a place to manage projects, which tasks are organized under.

HOW IT CONNECTS TO OTHER FILES:
- Called from app.py when the user selects "Projects" in the sidebar.
- Uses database/projects.py for all CRUD operations.
- Uses database/users.py to populate the "Project Manager" dropdown.
"""

import streamlit as st
from datetime import date

from config import PROJECT_STATUSES
from database.projects import (
    create_project, get_all_projects, update_project, delete_project,
)
from database.users import get_all_users


STATUS_ICON = {
    "Planning": "🗓️",
    "Active": "🟢",
    "Completed": "✅",
    "On Hold": "⏸️",
}


def render():
    st.title("📁 Projects")

    users = get_all_users()
    user_options = {u["username"]: u["id"] for u in users}

    with st.expander("➕ Create Project", expanded=False):
        with st.form("create_project_form", clear_on_submit=True):
            name = st.text_input("Project Name")
            description = st.text_area("Description")

            c1, c2 = st.columns(2)
            with c1:
                start = st.date_input("Start Date", value=date.today())
                status = st.selectbox("Status", PROJECT_STATUSES, index=0)
            with c2:
                end = st.date_input("End Date", value=date.today())
                manager_username = st.selectbox(
                    "Project Manager", options=list(user_options.keys()) or ["No users yet"]
                )

            if st.form_submit_button("Create Project"):
                if not name.strip():
                    st.error("Project name cannot be empty.")
                elif not user_options:
                    st.error("You need at least one user to assign as manager.")
                else:
                    ok = create_project(
                        project_name=name,
                        description=description,
                        start_date=start,
                        end_date=end,
                        status=status,
                        manager_id=user_options[manager_username],
                    )
                    if ok:
                        st.success(f"Project '{name}' created successfully!")
                        st.rerun()
                    else:
                        st.error("Something went wrong while creating the project.")

    st.markdown("### All Projects")

    projects = get_all_projects()
    if not projects:
        st.info("No projects yet — create your first project above.")
        return

    for p in projects:
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                icon = STATUS_ICON.get(p["status"], "📁")
                st.markdown(f"#### {icon} {p['project_name']}")
                st.write(p.get("description") or "_No description_")
                st.caption(
                    f"📅 {p['start_date']} → {p['end_date']}  |  "
                    f"👤 Manager: {p.get('manager_name') or 'Unassigned'}  |  "
                    f"Status: **{p['status']}**"
                )
            with c2:
                with st.popover("Manage"):
                    proj_names = list(user_options.keys())
                    current_manager = p.get("manager_name")
                    idx = proj_names.index(current_manager) if current_manager in proj_names else 0

                    new_name = st.text_input("Project Name", value=p["project_name"], key=f"pname_{p['id']}")
                    new_desc = st.text_area("Description", value=p.get("description") or "", key=f"pdesc_{p['id']}")
                    new_start = st.date_input("Start Date", value=p["start_date"], key=f"pstart_{p['id']}")
                    new_end = st.date_input("End Date", value=p["end_date"], key=f"pend_{p['id']}")
                    new_status = st.selectbox(
                        "Status", PROJECT_STATUSES,
                        index=PROJECT_STATUSES.index(p["status"]),
                        key=f"pstatus_{p['id']}",
                    )
                    new_manager = st.selectbox("Manager", proj_names, index=idx, key=f"pmgr_{p['id']}")

                    b1, b2 = st.columns(2)
                    with b1:
                        if st.button("Save", key=f"psave_{p['id']}"):
                            ok = update_project(
                                project_id=p["id"],
                                project_name=new_name,
                                description=new_desc,
                                start_date=new_start,
                                end_date=new_end,
                                status=new_status,
                                manager_id=user_options[new_manager],
                            )
                            if ok:
                                st.success("Project updated!")
                                st.rerun()
                            else:
                                st.error("Update failed.")
                    with b2:
                        if st.button("Delete", key=f"pdel_{p['id']}"):
                            ok = delete_project(p["id"])
                            if ok:
                                st.success("Project deleted.")
                                st.rerun()
                            else:
                                st.error("Delete failed.")
