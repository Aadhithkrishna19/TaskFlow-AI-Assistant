
from database.connection import get_connection, close_connection


def create_project(project_name, description, start_date, end_date, status, manager_id):
    """Inserts a new project row. Returns True/False for success."""
    connection = get_connection()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO projects
                (project_name, description, start_date, end_date, status, manager_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            query, (project_name, description, start_date, end_date, status, manager_id)
        )
        connection.commit()
        return True
    except Exception as e:
        print(f"[database/projects.py] create_project error: {e}")
        return False
    finally:
        close_connection(connection, cursor)


def get_all_projects():
    """Returns every project, joined with the manager's username."""
    connection = get_connection()
    if connection is None:
        return []

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT p.id, p.project_name, p.description, p.start_date, p.end_date,
                   p.status, p.manager_id, u.username AS manager_name, p.created_at
            FROM projects p
            LEFT JOIN users u ON p.manager_id = u.id
            ORDER BY p.created_at DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"[database/projects.py] get_all_projects error: {e}")
        return []
    finally:
        close_connection(connection, cursor)


def get_project_by_id(project_id):
    """Returns a single project by id."""
    connection = get_connection()
    if connection is None:
        return None

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM projects WHERE id = %s", (project_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"[database/projects.py] get_project_by_id error: {e}")
        return None
    finally:
        close_connection(connection, cursor)


def update_project(project_id, project_name, description, start_date, end_date, status, manager_id):
    """Updates all editable fields of a project."""
    connection = get_connection()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        query = """
            UPDATE projects
            SET project_name = %s, description = %s, start_date = %s,
                end_date = %s, status = %s, manager_id = %s
            WHERE id = %s
        """
        cursor.execute(
            query,
            (project_name, description, start_date, end_date, status, manager_id, project_id),
        )
        connection.commit()
        return True
    except Exception as e:
        print(f"[database/projects.py] update_project error: {e}")
        return False
    finally:
        close_connection(connection, cursor)


def delete_project(project_id):
    """Deletes a project by id."""
    connection = get_connection()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM projects WHERE id = %s", (project_id,))
        connection.commit()
        return True
    except Exception as e:
        print(f"[database/projects.py] delete_project error: {e}")
        return False
    finally:
        close_connection(connection, cursor)
