
import streamlit as st
from database.users import authenticate_user


def init_session_state():
    """Makes sure all session_state keys exist with safe defaults."""
    defaults = {
        "logged_in": False,
        "user_id": None,
        "username": None,
        "role": None,
        "email": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def login_user(email: str, password: str) -> bool:
    """
    Attempts to log a user in. On success, populates session_state and
    returns True. On failure, returns False (caller shows the error).
    """
    user = authenticate_user(email, password)
    if user is None:
        return False

    st.session_state["logged_in"] = True
    st.session_state["user_id"] = user["id"]
    st.session_state["username"] = user["username"]
    st.session_state["role"] = user["role"]
    st.session_state["email"] = user["email"]
    return True


def logout_user():
    """Clears the session so the user is returned to the login page."""
    st.session_state["logged_in"] = False
    st.session_state["user_id"] = None
    st.session_state["username"] = None
    st.session_state["role"] = None
    st.session_state["email"] = None


def is_logged_in() -> bool:
    """Convenience helper used at the top of every protected page."""
    return st.session_state.get("logged_in", False)
