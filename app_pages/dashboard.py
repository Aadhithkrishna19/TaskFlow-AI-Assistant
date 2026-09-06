"""
pages/dashboard.py
-------------------
WHAT THIS FILE DOES:
Renders the Dashboard page: KPI stat cards, a task-status pie chart,
a table of recent tasks, the current user's assigned tasks, and
upcoming deadlines.

WHY IT EXISTS:
Gives users a one-glance overview of the whole TaskFlow workspace.

HOW IT CONNECTS TO OTHER FILES:
- Called from app.py when the user selects "Dashboard" in the sidebar.
- Uses database/tasks.py for statistics and task lists.
- Uses utils/ui.py for stat cards, utils/task_utils.py for dataframes.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta

from database.tasks import get_task_statistics, get_all_tasks, get_user_tasks
from utils.ui import render_stat_card
from utils.task_utils import tasks_to_dataframe


def render():
    st.title("📊 TaskFlow Dashboard")

    stats = get_task_statistics()

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        render_stat_card("Total Tasks", stats["total"])
    with col2:
        render_stat_card("Pending", stats["pending"], color="#F5A623")
    with col3:
        render_stat_card("In Progress", stats["in_progress"], color="#1E5FBF")
    with col4:
        render_stat_card("Completed", stats["completed"], color="#2E7D32")
    with col5:
        render_stat_card("Overdue", stats["overdue"], color="#EB5757")

    st.markdown("### ")
    chart_col, recent_col = st.columns([1, 1.4])

    with chart_col:
        st.subheader("Task Status Breakdown")
        status_data = pd.DataFrame(
            {
                "Status": ["Pending", "In Progress", "Completed", "Cancelled"],
                "Count": [
                    stats["pending"],
                    stats["in_progress"],
                    stats["completed"],
                    stats["cancelled"],
                ],
            }
        )
        if status_data["Count"].sum() > 0:
            fig = px.pie(
                status_data,
                names="Status",
                values="Count",
                color="Status",
                color_discrete_map={
                    "Pending": "#F5A623",
                    "In Progress": "#1E5FBF",
                    "Completed": "#2E7D32",
                    "Cancelled": "#9E9E9E",
                },
                hole=0.45,
            )
            fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No task data yet. Create some tasks to see the chart.")

    with recent_col:
        st.subheader("Recent Tasks")
        all_tasks = get_all_tasks()
        recent = all_tasks[:6]
        if recent:
            df = tasks_to_dataframe(recent)
            st.dataframe(
                df[["title", "project_name", "priority", "status", "due_date"]],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No tasks yet — create your first task on the Tasks page.")

    st.markdown("### ")
    my_col, deadline_col = st.columns(2)

    with my_col:
        st.subheader("My Assigned Tasks")
        user_id = st.session_state.get("user_id")
        my_tasks = get_user_tasks(user_id) if user_id else []
        if my_tasks:
            df = tasks_to_dataframe(my_tasks[:6])
            st.dataframe(
                df[["title", "project_name", "priority", "status", "due_date"]],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("You have no assigned tasks.")

    with deadline_col:
        st.subheader("Upcoming Deadlines (next 7 days)")
        all_tasks = get_all_tasks()
        upcoming = [
            t for t in all_tasks
            if t.get("due_date") and date.today() <= t["due_date"] <= date.today() + timedelta(days=7)
            and t.get("status") not in ("Completed", "Cancelled")
        ]
        if upcoming:
            df = tasks_to_dataframe(upcoming)
            st.dataframe(
                df[["title", "project_name", "priority", "due_date"]],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No upcoming deadlines in the next 7 days.")
