
from datetime import date
from database.connection import get_connection, close_connection


def create_task(title, description, project_id, assigned_to, priority, status, due_date):
    """Inserts a new task row. Returns True/False for success."""
    connection = get_connection()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO tasks
                (title, description, project_id, assigned_to, priority, status, due_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (title, description, project_id, assigned_to, priority, status, due_date),
        )
        connection.commit()
        return True
    except Exception as e:
        print(f"[database/tasks.py] create_task error: {e}")
        return False
    finally:
        close_connection(connection, cursor)


def get_all_tasks():
    """Returns every task, joined with project and assignee names."""
    connection = get_connection()
    if connection is None:
        return []

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT t.id, t.title, t.description, t.priority, t.status, t.due_date,
                   t.created_at, t.updated_at,
                   p.project_name, p.id AS project_id,
                   u.username AS assigned_to_name, u.id AS assigned_to
            FROM tasks t
            LEFT JOIN projects p ON t.project_id = p.id
            LEFT JOIN users u ON t.assigned_to = u.id
            ORDER BY t.created_at DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"[database/tasks.py] get_all_tasks error: {e}")
        return []
    finally:
        close_connection(connection, cursor)


def get_user_tasks(user_id):
    """Returns tasks assigned to a specific user."""
    connection = get_connection()
    if connection is None:
        return []

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT t.id, t.title, t.description, t.priority, t.status, t.due_date,
                   t.created_at, t.updated_at,
                   p.project_name, p.id AS project_id
            FROM tasks t
            LEFT JOIN projects p ON t.project_id = p.id
            WHERE t.assigned_to = %s
            ORDER BY t.due_date IS NULL, t.due_date ASC
        """
        cursor.execute(query, (user_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"[database/tasks.py] get_user_tasks error: {e}")
        return []
    finally:
        close_connection(connection, cursor)


def get_task_by_id(task_id):
    """Returns a single task by id."""
    connection = get_connection()
    if connection is None:
        return None

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"[database/tasks.py] get_task_by_id error: {e}")
        return None
    finally:
        close_connection(connection, cursor)


def update_task(task_id, title, description, project_id, assigned_to, priority, status, due_date):
    """Updates all editable fields of a task."""
    connection = get_connection()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        query = """
            UPDATE tasks
            SET title = %s, description = %s, project_id = %s, assigned_to = %s,
                priority = %s, status = %s, due_date = %s
            WHERE id = %s
        """
        cursor.execute(
            query,
            (title, description, project_id, assigned_to, priority, status, due_date, task_id),
        )
        connection.commit()
        return True
    except Exception as e:
        print(f"[database/tasks.py] update_task error: {e}")
        return False
    finally:
        close_connection(connection, cursor)


def delete_task(task_id):
    """Deletes a task by id."""
    connection = get_connection()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        connection.commit()
        return True
    except Exception as e:
        print(f"[database/tasks.py] delete_task error: {e}")
        return False
    finally:
        close_connection(connection, cursor)


def update_task_status(task_id, new_status):
    """Updates only the status field of a task (used by quick-action buttons)."""
    connection = get_connection()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE tasks SET status = %s WHERE id = %s", (new_status, task_id)
        )
        connection.commit()
        return True
    except Exception as e:
        print(f"[database/tasks.py] update_task_status error: {e}")
        return False
    finally:
        close_connection(connection, cursor)


# ---------------------------------------------------------------------
# SAFE, PREDEFINED QUERY FUNCTIONS FOR HelpFlow
# These are the ONLY database functions the AI assistant is allowed to
# call. Each one uses a fixed, parameterized query - the AI never
# builds or executes raw SQL itself.
# ---------------------------------------------------------------------

def get_pending_tasks(user_id=None):
    """Returns all tasks with status = 'Pending', optionally filtered by user."""
    return _get_tasks_by_status("Pending", user_id)


def get_completed_tasks(user_id=None):
    """Returns all tasks with status = 'Completed', optionally filtered by user."""
    return _get_tasks_by_status("Completed", user_id)


def get_overdue_tasks(user_id=None):
    """
    Returns tasks whose due_date has passed and are not yet Completed
    or Cancelled, optionally filtered by user.
    """
    connection = get_connection()
    if connection is None:
        return []

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        if user_id is not None:
            query = """
                SELECT t.id, t.title, t.status, t.priority, t.due_date,
                       p.project_name
                FROM tasks t
                LEFT JOIN projects p ON t.project_id = p.id
                WHERE t.due_date < %s
                  AND t.status NOT IN ('Completed', 'Cancelled')
                  AND t.assigned_to = %s
                ORDER BY t.due_date ASC
            """
            cursor.execute(query, (date.today(), user_id))
        else:
            query = """
                SELECT t.id, t.title, t.status, t.priority, t.due_date,
                       p.project_name
                FROM tasks t
                LEFT JOIN projects p ON t.project_id = p.id
                WHERE t.due_date < %s
                  AND t.status NOT IN ('Completed', 'Cancelled')
                ORDER BY t.due_date ASC
            """
            cursor.execute(query, (date.today(),))
        return cursor.fetchall()
    except Exception as e:
        print(f"[database/tasks.py] get_overdue_tasks error: {e}")
        return []
    finally:
        close_connection(connection, cursor)


def get_high_priority_tasks(user_id=None):
    """Returns tasks with priority = 'High' or 'Critical', optionally filtered by user."""
    connection = get_connection()
    if connection is None:
        return []

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        if user_id is not None:
            query = """
                SELECT t.id, t.title, t.status, t.priority, t.due_date,
                       p.project_name
                FROM tasks t
                LEFT JOIN projects p ON t.project_id = p.id
                WHERE t.priority IN ('High', 'Critical') AND t.assigned_to = %s
                ORDER BY t.priority DESC, t.due_date ASC
            """
            cursor.execute(query, (user_id,))
        else:
            query = """
                SELECT t.id, t.title, t.status, t.priority, t.due_date,
                       p.project_name
                FROM tasks t
                LEFT JOIN projects p ON t.project_id = p.id
                WHERE t.priority IN ('High', 'Critical')
                ORDER BY t.priority DESC, t.due_date ASC
            """
            cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"[database/tasks.py] get_high_priority_tasks error: {e}")
        return []
    finally:
        close_connection(connection, cursor)


def _get_tasks_by_status(status_value, user_id=None):
    """Internal helper shared by get_pending_tasks / get_completed_tasks."""
    connection = get_connection()
    if connection is None:
        return []

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        if user_id is not None:
            query = """
                SELECT t.id, t.title, t.status, t.priority, t.due_date,
                       p.project_name
                FROM tasks t
                LEFT JOIN projects p ON t.project_id = p.id
                WHERE t.status = %s AND t.assigned_to = %s
                ORDER BY t.due_date IS NULL, t.due_date ASC
            """
            cursor.execute(query, (status_value, user_id))
        else:
            query = """
                SELECT t.id, t.title, t.status, t.priority, t.due_date,
                       p.project_name
                FROM tasks t
                LEFT JOIN projects p ON t.project_id = p.id
                WHERE t.status = %s
                ORDER BY t.due_date IS NULL, t.due_date ASC
            """
            cursor.execute(query, (status_value,))
        return cursor.fetchall()
    except Exception as e:
        print(f"[database/tasks.py] _get_tasks_by_status error: {e}")
        return []
    finally:
        close_connection(connection, cursor)


def get_task_count(user_id=None):
    """Returns the total number of tasks, optionally filtered by user."""
    connection = get_connection()
    if connection is None:
        return 0

    cursor = None
    try:
        cursor = connection.cursor()
        if user_id is not None:
            cursor.execute(
                "SELECT COUNT(*) FROM tasks WHERE assigned_to = %s", (user_id,)
            )
        else:
            cursor.execute("SELECT COUNT(*) FROM tasks")
        result = cursor.fetchone()
        return result[0] if result else 0
    except Exception as e:
        print(f"[database/tasks.py] get_task_count error: {e}")
        return 0
    finally:
        close_connection(connection, cursor)


def get_task_statistics(user_id=None):
    """
    Returns a dictionary with counts used by the Dashboard page and by
    HelpFlow: total, pending, in_progress, completed, cancelled, overdue.
    """
    connection = get_connection()
    if connection is None:
        return {
            "total": 0, "pending": 0, "in_progress": 0,
            "completed": 0, "cancelled": 0, "overdue": 0,
        }

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        base_where = "WHERE assigned_to = %s" if user_id is not None else ""
        params = (user_id,) if user_id is not None else ()

        cursor.execute(f"SELECT COUNT(*) AS c FROM tasks {base_where}", params)
        total = cursor.fetchone()["c"]

        stats = {"total": total}
        for status_key, status_value in [
            ("pending", "Pending"),
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ]:
            if user_id is not None:
                q = "SELECT COUNT(*) AS c FROM tasks WHERE status = %s AND assigned_to = %s"
                cursor.execute(q, (status_value, user_id))
            else:
                q = "SELECT COUNT(*) AS c FROM tasks WHERE status = %s"
                cursor.execute(q, (status_value,))
            stats[status_key] = cursor.fetchone()["c"]

        if user_id is not None:
            q = """
                SELECT COUNT(*) AS c FROM tasks
                WHERE due_date < %s AND status NOT IN ('Completed', 'Cancelled')
                AND assigned_to = %s
            """
            cursor.execute(q, (date.today(), user_id))
        else:
            q = """
                SELECT COUNT(*) AS c FROM tasks
                WHERE due_date < %s AND status NOT IN ('Completed', 'Cancelled')
            """
            cursor.execute(q, (date.today(),))
        stats["overdue"] = cursor.fetchone()["c"]

        return stats
    except Exception as e:
        print(f"[database/tasks.py] get_task_statistics error: {e}")
        return {
            "total": 0, "pending": 0, "in_progress": 0,
            "completed": 0, "cancelled": 0, "overdue": 0,
        }
    finally:
        close_connection(connection, cursor)
