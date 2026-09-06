"""
ai/assistant.py
----------------
WHAT THIS FILE DOES:
This is the "brain" of HelpFlow. It receives a user's chat message,
figures out what they want (using ai/intent.py), fetches the right
information (from ai/knowledge_base.py or database/tasks.py /
database/projects.py), and returns a friendly natural-language answer.

WHY IT EXISTS:
Keeping all of this orchestration in one function -
get_helpflow_response() - means pages/helpflow.py only has to call one
simple function and doesn't need to know anything about intents,
knowledge bases, or SQL.

FUNCTIONS INSIDE THIS FILE:
- get_helpflow_response(user_id, message) -> the main entry point.
- _call_ai_model(system_prompt, user_prompt) -> talks to the OpenAI API
  (if a key is configured) to turn raw data into a natural sentence.
  If no API key is set, or the call fails, this file falls back to a
  simple template-based response so HelpFlow still works.

HOW IT CONNECTS TO OTHER FILES:
- pages/helpflow.py calls get_helpflow_response(user_id, message) for
  every message the user sends.
- Uses ai/intent.py to classify the question.
- Uses ai/knowledge_base.py for APPLICATION_HELP answers.
- Uses database/tasks.py and database/projects.py for DATABASE_QUERY
  answers (only through their already-safe, parameterized functions -
  this file NEVER writes or executes raw SQL).
- Uses database/chat.py to save every exchange to chat_history.
"""

from config import OPENAI_API_KEY, AI_MODEL
from ai.intent import detect_intent, match_knowledge_base_topic, detect_database_topic
from ai.knowledge_base import KNOWLEDGE_BASE
from database import tasks as tasks_db
from database import projects as projects_db
from database.chat import save_chat

# System prompt that constrains the AI model to ONLY rephrase the data
# we already fetched - it is never allowed to invent facts or run SQL.
SYSTEM_PROMPT = (
    "You are HelpFlow, a friendly and concise AI assistant built into "
    "the TaskFlow application. You help users understand how to use "
    "TaskFlow and answer questions about their tasks and projects. "
    "You will be given factual information that has already been "
    "retrieved from the database or knowledge base - rephrase it into "
    "a short, clear, natural-sounding answer. Never invent task or "
    "project details that were not given to you. Never mention SQL, "
    "databases, or internal system details to the user. Keep answers "
    "under 4 sentences unless listing multiple tasks."
)


def _call_ai_model(user_prompt: str) -> str:
    """
    Sends the retrieved facts to the OpenAI API to turn them into a
    natural-language answer. If no API key is configured, or the
    request fails for any reason, returns None so the caller can fall
    back to a simple template-based response instead.
    """
    if not OPENAI_API_KEY:
        return None

    try:
        from openai import OpenAI

        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=300,
            temperature=0.4,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ai/assistant.py] AI model call failed, using fallback: {e}")
        return None


def _format_task_list(task_rows, empty_message):
    """Formats a list of task dict rows into a readable bullet list."""
    if not task_rows:
        return empty_message

    lines = []
    for t in task_rows:
        due = t.get("due_date")
        due_str = f" (due {due})" if due else ""
        project = t.get("project_name") or "No project"
        lines.append(f"- **{t['title']}** — {t['priority']} priority, {project}{due_str}")
    return "\n".join(lines)


def _handle_application_help(message: str):
    """Builds the raw facts + fallback text for an APPLICATION_HELP question."""
    topic = match_knowledge_base_topic(message)

    if topic and topic in KNOWLEDGE_BASE:
        answer_text = KNOWLEDGE_BASE[topic]["answer"]
    else:
        answer_text = (
            "I can help with creating, editing, deleting and updating "
            "tasks, creating projects, viewing your tasks, and reading "
            "your dashboard. Could you tell me a bit more about what "
            "you're trying to do?"
        )

    raw_facts = f"User asked: \"{message}\"\nKnowledge base answer: {answer_text}"
    return raw_facts, answer_text


def _handle_database_query(user_id, message: str):
    """
    Builds the raw facts + fallback text for a DATABASE_QUERY question
    by calling one of the SAFE, predefined functions in database/tasks.py
    or database/projects.py. No raw SQL is ever built from user input.
    """
    topic = detect_database_topic(message)

    if topic == "pending":
        rows = tasks_db.get_pending_tasks(user_id=user_id)
        fallback = f"You have {len(rows)} pending task(s).\n\n" + _format_task_list(
            rows, "You have no pending tasks right now."
        )
        raw_facts = f"Pending tasks for this user ({len(rows)} total): {rows}"

    elif topic == "completed":
        rows = tasks_db.get_completed_tasks(user_id=user_id)
        fallback = f"You have completed {len(rows)} task(s).\n\n" + _format_task_list(
            rows, "You haven't completed any tasks yet."
        )
        raw_facts = f"Completed tasks for this user ({len(rows)} total): {rows}"

    elif topic == "overdue":
        rows = tasks_db.get_overdue_tasks(user_id=user_id)
        fallback = f"You have {len(rows)} overdue task(s).\n\n" + _format_task_list(
            rows, "Great news — you have no overdue tasks."
        )
        raw_facts = f"Overdue tasks for this user ({len(rows)} total): {rows}"

    elif topic == "high_priority":
        rows = tasks_db.get_high_priority_tasks(user_id=user_id)
        fallback = f"You have {len(rows)} high priority task(s).\n\n" + _format_task_list(
            rows, "You have no high priority tasks right now."
        )
        raw_facts = f"High priority tasks for this user ({len(rows)} total): {rows}"

    elif topic == "projects":
        rows = projects_db.get_all_projects()
        if rows:
            lines = [f"- **{p['project_name']}** ({p['status']})" for p in rows]
            fallback = "Here are the available projects:\n\n" + "\n".join(lines)
        else:
            fallback = "There are no projects in the system yet."
        raw_facts = f"All projects ({len(rows)} total): {rows}"

    elif topic == "count":
        stats = tasks_db.get_task_statistics(user_id=user_id)
        fallback = (
            f"You have {stats['total']} total task(s): "
            f"{stats['pending']} pending, {stats['in_progress']} in progress, "
            f"{stats['completed']} completed, {stats['overdue']} overdue."
        )
        raw_facts = f"Task statistics for this user: {stats}"

    else:  # "all"
        rows = tasks_db.get_user_tasks(user_id)
        fallback = f"You have {len(rows)} task(s) in total.\n\n" + _format_task_list(
            rows, "You have no tasks assigned to you yet."
        )
        raw_facts = f"All tasks for this user ({len(rows)} total): {rows}"

    raw_facts = f"User asked: \"{message}\"\n{raw_facts}"
    return raw_facts, fallback


def get_helpflow_response(user_id: int, message: str) -> str:
    """
    Main entry point for HelpFlow. Given a user's id and their chat
    message, returns HelpFlow's natural-language reply.

    Flow (matches the architecture described in the project spec):
    1. Detect intent (APPLICATION_HELP or DATABASE_QUERY).
    2. If application help -> pull the answer from the knowledge base.
       If database query -> call a safe, predefined database function.
    3. Send the retrieved facts to the AI model to phrase a natural
       answer (or fall back to a template if no AI key is configured).
    4. Save the conversation to chat_history.
    5. Return the final response text.
    """
    if not message or not message.strip():
        return "I didn't catch that — could you type your question again?"

    intent = detect_intent(message)

    if intent == "APPLICATION_HELP":
        raw_facts, fallback_answer = _handle_application_help(message)
    else:
        raw_facts, fallback_answer = _handle_database_query(user_id, message)

    ai_answer = _call_ai_model(raw_facts)
    final_answer = ai_answer if ai_answer else fallback_answer

    save_chat(user_id, message, final_answer)

    return final_answer
