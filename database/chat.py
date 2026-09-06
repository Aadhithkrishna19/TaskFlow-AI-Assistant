
from database.connection import get_connection, close_connection


def save_chat(user_id, user_message, assistant_response):
    """Inserts one chat exchange (question + answer) into chat_history."""
    connection = get_connection()
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO chat_history (user_id, user_message, assistant_response)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (user_id, user_message, assistant_response))
        connection.commit()
        return True
    except Exception as e:
        print(f"[database/chat.py] save_chat error: {e}")
        return False
    finally:
        close_connection(connection, cursor)


def get_chat_history(user_id, limit=50):
    """Returns the most recent chat exchanges for a user, oldest first."""
    connection = get_connection()
    if connection is None:
        return []

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT id, user_message, assistant_response, created_at
            FROM chat_history
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT %s
        """
        cursor.execute(query, (user_id, limit))
        rows = cursor.fetchall()
        return list(reversed(rows))  # oldest first, for natural chat order
    except Exception as e:
        print(f"[database/chat.py] get_chat_history error: {e}")
        return []
    finally:
        close_connection(connection, cursor)
