"""
ai/knowledge_base.py
---------------------
WHAT THIS FILE DOES:
Stores a simple, easy-to-edit dictionary of "how do I..." instructions
for using TaskFlow. This is the source of truth for HelpFlow's
APPLICATION_HELP answers.

WHY IT EXISTS:
Separating this content from the AI logic (ai/assistant.py) means a
non-technical teammate can update instructions just by editing plain
Python strings below - no need to touch the AI code.

WHAT'S INSIDE:
- KNOWLEDGE_BASE: a dict where each key is a short topic name
  (e.g. "create_task") and the value is the plain-English instructions
  plus a list of example phrases that should match that topic.

HOW IT CONNECTS TO OTHER FILES:
- ai/intent.py and ai/assistant.py both read from KNOWLEDGE_BASE to
  find the best-matching topic for a user's question.
"""

KNOWLEDGE_BASE = {
    "create_task": {
        "answer": (
            "To create a task: open the **Tasks** page from the sidebar, "
            "click **Create Task**, fill in the title, description, project, "
            "priority, status, assigned user and due date, then click "
            "**Create Task** to save it."
        ),
        "keywords": [
            "create task", "add task", "new task", "make a task",
            "how do i create a task", "how to create task",
        ],
    },
    "edit_task": {
        "answer": (
            "To edit a task: go to the **Tasks** page, find the task in the "
            "table, and click **Edit**. Update any field you need and save "
            "your changes."
        ),
        "keywords": [
            "edit task", "update task", "modify task", "change task details",
            "how do i update a task", "how do i edit a task",
        ],
    },
    "delete_task": {
        "answer": (
            "To delete a task: go to the **Tasks** page, find the task in "
            "the table, and click **Delete**. This action cannot be undone, "
            "so double-check before confirming."
        ),
        "keywords": [
            "delete task", "remove task", "how do i delete a task",
        ],
    },
    "update_status": {
        "answer": (
            "To change a task's status: open the **Tasks** page (or **My "
            "Tasks**), find the task, and use the status dropdown or the "
            "**Update Status** control to switch it between Pending, In "
            "Progress, Completed, or Cancelled."
        ),
        "keywords": [
            "change status", "update status", "mark as complete",
            "mark task complete", "how do i change task status",
            "how can i change task status",
        ],
    },
    "create_project": {
        "answer": (
            "To create a project: open the **Projects** page from the "
            "sidebar, fill in the project name, description, start date, "
            "end date, status and project manager, then submit the form."
        ),
        "keywords": [
            "create project", "new project", "add project",
            "how do i create a project",
        ],
    },
    "view_my_tasks": {
        "answer": (
            "To see the tasks assigned to you, open the **My Tasks** page "
            "from the sidebar. You can filter by status, priority, project, "
            "or due date."
        ),
        "keywords": [
            "my tasks", "tasks assigned to me", "view my tasks",
            "what tasks are assigned to me",
        ],
    },
    "dashboard_help": {
        "answer": (
            "The **Dashboard** page gives you an overview of all tasks: "
            "total tasks, pending, in progress, completed and overdue "
            "counts, plus a status chart, recent tasks, and upcoming "
            "deadlines."
        ),
        "keywords": [
            "dashboard", "overview", "what does the dashboard show",
        ],
    },
    "assign_task": {
        "answer": (
            "To assign a task to someone, open the **Tasks** page, create "
            "or edit a task, and choose the person's name from the "
            "**Assigned User** dropdown."
        ),
        "keywords": [
            "assign task", "assign a task", "how do i assign a task",
        ],
    },
    "search_filter_tasks": {
        "answer": (
            "You can search and filter tasks on the **Tasks** or **My "
            "Tasks** pages using the filter controls for status, priority, "
            "project and due date at the top of the page."
        ),
        "keywords": [
            "search tasks", "filter tasks", "find a task",
        ],
    },
}
