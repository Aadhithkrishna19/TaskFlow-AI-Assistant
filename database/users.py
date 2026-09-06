
import bcrypt
from database.connection import get_connection, close_connection


def _hash_password(plain_password: str) -> str:
    """Hashes a plain-text password using bcrypt before storing it."""
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compares a plain-text password against a stored bcrypt hash."""
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
    except ValueError:
        # Happens if the stored hash is malformed - treat as no match.
        return False


def create_user(username: str, email: str, password: str, role: str = "Employee"):
    """
    Creates a new user in the database with a hashed password.

    Returns:
        True if the user was created successfully, False otherwise.
    """
    connection = get_connection()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        hashed_pw = _hash_password(password)
        query = (
            "INSERT INTO users (username, email, password, role) "
            "VALUES (%s, %s, %s, %s)"
        )
        cursor.execute(query, (username, email, hashed_pw, role))
        connection.commit()
        return True
    except Exception as e:
        print(f"[database/users.py] create_user error: {e}")
        return False
    finally:
        close_connection(connection, cursor)


def authenticate_user(email: str, password: str):
    """
    Checks the given email/password against the users table.

    Returns:
        A dict with the user's info if credentials are valid,
        otherwise None.
    """
    connection = get_connection()
    if connection is None:
        return None

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user is None:
            return None

        if _verify_password(password, user["password"]):
            # Never return the password hash to the rest of the app.
            user.pop("password", None)
            return user

        return None
    except Exception as e:
        print(f"[database/users.py] authenticate_user error: {e}")
        return None
    finally:
        close_connection(connection, cursor)


def get_user_by_id(user_id: int):
    """Fetches a single user record (without the password) by id."""
    connection = get_connection()
    if connection is None:
        return None

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, username, email, role, created_at FROM users WHERE id = %s",
            (user_id,),
        )
        return cursor.fetchone()
    except Exception as e:
        print(f"[database/users.py] get_user_by_id error: {e}")
        return None
    finally:
        close_connection(connection, cursor)


def get_all_users():
    """Returns every user (without passwords) - used for dropdowns."""
    connection = get_connection()
    if connection is None:
        return []

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, username, email, role, created_at FROM users ORDER BY username"
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"[database/users.py] get_all_users error: {e}")
        return []
    finally:
        close_connection(connection, cursor)
