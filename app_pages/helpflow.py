"""
pages/helpflow.py
-------------------
WHAT THIS FILE DOES:
Renders the HelpFlow AI Assistant chat page using Streamlit's built-in
chat components (st.chat_message, st.chat_input), including suggested
starter questions.

WHY IT EXISTS:
Gives users a friendly chatbot-style interface to interact with
HelpFlow, TaskFlow's built-in AI assistant.

HOW IT CONNECTS TO OTHER FILES:
- Called from app.py when the user selects "HelpFlow" in the sidebar.
- Uses ai/assistant.py -> get_helpflow_response() to generate answers.
- Uses database/chat.py -> get_chat_history() to reload past messages.
"""

import streamlit as st

from config import ASSISTANT_NAME, ASSISTANT_TAGLINE
from ai.assistant import get_helpflow_response
from database.chat import get_chat_history

SUGGESTED_QUESTIONS = [
    "How do I create a task?",
    "Show my pending tasks",
    "How many completed tasks do I have?",
    "What are my overdue tasks?",
    "How do I create a project?",
    "How can I change task status?",
    "Show my high priority tasks",
    "How many tasks are assigned to me?",
]


def render():
    st.title(f"🤖 {ASSISTANT_NAME}")
    st.caption(ASSISTANT_TAGLINE)

    user_id = st.session_state.get("user_id")

    # Load history from the database only once per session so we don't
    # keep re-querying MySQL on every chat message.
    if "helpflow_messages" not in st.session_state:
        history = get_chat_history(user_id, limit=30) if user_id else []
        messages = []
        for exchange in history:
            messages.append({"role": "user", "content": exchange["user_message"]})
            messages.append({"role": "assistant", "content": exchange["assistant_response"]})
        st.session_state["helpflow_messages"] = messages

    st.markdown("**Try asking:**")
    cols = st.columns(4)
    for i, question in enumerate(SUGGESTED_QUESTIONS):
        with cols[i % 4]:
            if st.button(question, key=f"suggested_{i}", use_container_width=True):
                st.session_state["pending_question"] = question

    st.markdown("---")

    for msg in st.session_state["helpflow_messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    typed_question = st.chat_input("Ask HelpFlow anything about TaskFlow...")
    question = st.session_state.pop("pending_question", None) or typed_question

    if question:
        st.session_state["helpflow_messages"].append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("HelpFlow is thinking..."):
                answer = get_helpflow_response(user_id, question)
            st.markdown(answer)

        st.session_state["helpflow_messages"].append({"role": "assistant", "content": answer})
