

import mysql.connector
from mysql.connector import Error
import streamlit as st

from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


def get_connection():
    """
    Opens a new connection to the MySQL database.

    Returns:
        mysql.connector.connection.MySQLConnection | None
        A live connection object on success, or None if the connection
        could not be made (a friendly error is shown to the user).
    """
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
        return connection
    except Error as e:
        # Never show the raw stack trace to the user - show something
        # friendly instead, and log the real error to the console for
        # the developer to see.
        print(f"[database/connection.py] MySQL connection error: {e}")
        st.error(
            "⚠️ Could not connect to the TaskFlow database. "
            "Please make sure MySQL is running and your .env file is "
            "configured correctly."
        )
        return None


def close_connection(connection, cursor=None):
    """
    Safely closes a cursor (if given) and a database connection.
    Wrapping this in a helper avoids repeating try/except everywhere.
    """
    try:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
    except Error as e:
        print(f"[database/connection.py] Error closing connection: {e}")
