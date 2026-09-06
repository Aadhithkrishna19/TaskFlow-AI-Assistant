
import streamlit as st
from config import (
    APP_NAME, APP_TAGLINE, COLOR_PRIMARY, COLOR_SECONDARY,
    COLOR_BACKGROUND, COLOR_CARD, COLOR_TEXT,
)


def apply_custom_theme():
    """Injects a professional SaaS-style CSS theme into the page."""
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {COLOR_BACKGROUND};
            color: {COLOR_TEXT};
        }}
        section[data-testid="stSidebar"] {{
            background-color: {COLOR_PRIMARY};
        }}
        section[data-testid="stSidebar"] * {{
            color: #FFFFFF !important;
        }}
        div.stButton > button {{
            background-color: {COLOR_SECONDARY};
            color: #FFFFFF;
            border: none;
            border-radius: 6px;
            padding: 0.5em 1.2em;
            font-weight: 600;
        }}
        div.stButton > button:hover {{
            background-color: {COLOR_PRIMARY};
            color: #FFFFFF;
        }}
        .stat-card {{
            background-color: {COLOR_CARD};
            border-radius: 10px;
            padding: 1.2rem;
            box-shadow: 0 1px 4px rgba(0,0,0,0.08);
            text-align: center;
        }}
        .stat-card h2 {{
            margin: 0;
            font-size: 2rem;
        }}
        .stat-card p {{
            margin: 0;
            color: #666666;
            font-weight: 500;
        }}
        .badge {{
            display: inline-block;
            padding: 0.2em 0.7em;
            border-radius: 999px;
            color: white;
            font-size: 0.8rem;
            font-weight: 600;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    """
    Draws the branded sidebar with navigation links.

    Returns:
        The name of the page the user selected (a string).
    """
    with st.sidebar:
        st.markdown(f"## 🗂️ {APP_NAME.upper()}")
        st.caption(APP_TAGLINE)
        st.markdown("---")

        page = st.radio(
            "Navigate",
            [
                "Dashboard",
                "Tasks",
                "Projects",
                "My Tasks",
                "HelpFlow",
            ],
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.caption(f"Logged in as **{st.session_state.get('username', '')}**")
        st.caption(f"Role: {st.session_state.get('role', '')}")

        if st.button("Logout", use_container_width=True):
            from utils.authentication import logout_user
            logout_user()
            st.rerun()

    return page


def render_stat_card(label: str, value, color: str = None):
    """Renders a single KPI stat card (used on the Dashboard)."""
    color_style = f"color: {color};" if color else ""
    st.markdown(
        f"""
        <div class="stat-card">
            <h2 style="{color_style}">{value}</h2>
            <p>{label}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status_badge(text: str, color: str):
    """Renders a small colored badge (used for status/priority in tables)."""
    st.markdown(
        f'<span class="badge" style="background-color:{color};">{text}</span>',
        unsafe_allow_html=True,
    )
