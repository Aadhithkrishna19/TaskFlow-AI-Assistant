
import streamlit as st

from config import APP_NAME, APP_TAGLINE
from utils.authentication import init_session_state, login_user, is_logged_in
from utils.ui import apply_custom_theme, render_sidebar

from app_pages import dashboard, tasks, projects, my_tasks, helpflow


st.set_page_config(
    page_title=f"{APP_NAME} — {APP_TAGLINE}",
    page_icon="🗂️",
    layout="wide",
)

apply_custom_theme()
init_session_state()


def render_login_page():
    """Shows the login form. On success, reruns the app to load the dashboard."""
    st.markdown(
        f"""
        <div style="text-align:center; margin-top: 3rem;">
            <h1>🗂️ {APP_NAME.upper()}</h1>
            <p style="color:#666;">{APP_TAGLINE}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, center, _ = st.columns([1, 1.2, 1])
    with center:
        with st.container(border=True):
            st.subheader("Login")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if st.button("Login", use_container_width=True):
                if not email or not password:
                    st.error("Please enter both email and password.")
                else:
                    success = login_user(email, password)
                    if success:
                        st.rerun()
                    else:
                        st.error("Invalid email or password. Please try again.")

            st.caption(
                "Sample login: alice@taskflow.com / password123 "
                "(see README for all sample accounts)"
            )


def render_app():
    """Draws the sidebar and routes to the selected page."""
    selected_page = render_sidebar()

    if selected_page == "Dashboard":
        dashboard.render()
    elif selected_page == "Tasks":
        tasks.render()
    elif selected_page == "Projects":
        projects.render()
    elif selected_page == "My Tasks":
        my_tasks.render()
    elif selected_page == "HelpFlow":
        helpflow.render()


def main():
    if not is_logged_in():
        render_login_page()
    else:
        render_app()


if __name__ == "__main__":
    main()
