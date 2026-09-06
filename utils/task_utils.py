
import pandas as pd


def tasks_to_dataframe(task_rows):
    """Converts a list of task dicts into a pandas DataFrame for display."""
    if not task_rows:
        return pd.DataFrame(
            columns=["id", "title", "project_name", "priority", "status", "due_date"]
        )
    return pd.DataFrame(task_rows)


STATUS_COLORS = {
    "Pending": "#F5A623",       # amber
    "In Progress": "#1E5FBF",   # blue
    "Completed": "#2E7D32",     # green
    "Cancelled": "#9E9E9E",     # gray
}

PRIORITY_COLORS = {
    "Low": "#6FCF97",
    "Medium": "#F5A623",
    "High": "#EB5757",
    "Critical": "#B71C1C",
}


def status_badge_color(status: str) -> str:
    """Returns a hex color to represent a task status badge."""
    return STATUS_COLORS.get(status, "#9E9E9E")


def priority_badge_color(priority: str) -> str:
    """Returns a hex color to represent a task priority badge."""
    return PRIORITY_COLORS.get(priority, "#9E9E9E")


def validate_task_fields(title: str, due_date) -> str:
    """
    Validates the minimum required fields for creating/editing a task.

    Returns:
        An error message string if something is invalid, or an empty
        string "" if everything looks good.
    """
    if not title or not title.strip():
        return "Task title cannot be empty."
    if due_date is None:
        return "Please select a due date."
    return ""
