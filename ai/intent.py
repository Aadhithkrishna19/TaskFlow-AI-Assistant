"""
ai/intent.py
------------
WHAT THIS FILE DOES:
Looks at the user's message and decides whether it is:
  - APPLICATION_HELP  -> a "how do I..." question about using TaskFlow
  - DATABASE_QUERY    -> a question about the user's actual task/project
                          data ("how many tasks do I have?")

WHY IT EXISTS:
Separating "understand what the user wants" from "go get the answer"
keeps ai/assistant.py simple and makes the logic easy to test and
extend (for example, adding a new intent later).

FUNCTIONS INSIDE THIS FILE:
- detect_intent(message) -> returns "APPLICATION_HELP" or
  "DATABASE_QUERY"
- match_knowledge_base_topic(message) -> returns the best-matching
  knowledge base topic key (or None)
- detect_database_topic(message) -> returns a short label describing
  which safe SQL function should be called (e.g. "pending", "overdue")

HOW IT CONNECTS TO OTHER FILES:
- ai/assistant.py calls detect_intent() first, then calls
  match_knowledge_base_topic() or detect_database_topic() depending on
  the result.
- Reads keyword lists from ai/knowledge_base.py.
"""

from ai.knowledge_base import KNOWLEDGE_BASE

# Keywords that strongly suggest the user wants data ABOUT their tasks,
# rather than instructions on HOW to use the app.
DATABASE_KEYWORDS = [
    "how many", "show me", "show my", "list my", "what are my",
    "which tasks", "pending tasks", "completed tasks", "overdue",
    "high priority", "assigned to me", "my pending", "my completed",
    "task count", "how much", "count of",
]

# Keywords that strongly suggest the user wants instructions.
APPLICATION_KEYWORDS = [
    "how do i", "how to", "how can i", "where can i", "where do i",
    "explain", "guide", "instructions", "steps to",
]


def detect_intent(message: str) -> str:
    """
    Classifies a user's message as APPLICATION_HELP or DATABASE_QUERY.

    The logic is intentionally simple and keyword-based so it is fast,
    free, and does not depend on an external AI call just to route the
    question.
    """
    text = message.lower().strip()

    # If the question clearly asks "how do I do X", it's app help -
    # even if it also mentions tasks/projects.
    for phrase in APPLICATION_KEYWORDS:
        if phrase in text:
            # But "how many" style counting questions should still be
            # treated as database queries even though they start with
            # "how" - check that first.
            if not any(dbk in text for dbk in ["how many", "how much"]):
                return "APPLICATION_HELP"

    for phrase in DATABASE_KEYWORDS:
        if phrase in text:
            return "DATABASE_QUERY"

    # Fall back: try to match a knowledge base topic. If we find a
    # strong match, treat it as application help; otherwise default to
    # a database query since most remaining questions tend to be about
    # the user's own data ("pending tasks", "my tasks", etc).
    topic = match_knowledge_base_topic(text)
    if topic:
        return "APPLICATION_HELP"

    return "DATABASE_QUERY"


def match_knowledge_base_topic(message: str):
    """
    Finds the knowledge base topic whose keywords best match the
    message. Returns the topic key (e.g. "create_task") or None.
    """
    text = message.lower().strip()
    best_topic = None
    best_score = 0

    for topic_key, topic_data in KNOWLEDGE_BASE.items():
        score = 0
        for keyword in topic_data["keywords"]:
            if keyword in text:
                score += len(keyword.split())  # longer matches score higher
        if score > best_score:
            best_score = score
            best_topic = topic_key

    return best_topic


def detect_database_topic(message: str) -> str:
    """
    Determines which safe database function HelpFlow should call for a
    DATABASE_QUERY intent. Returns one of:
    "pending", "completed", "overdue", "high_priority", "projects",
    "count", "all"
    """
    text = message.lower().strip()

    if "overdue" in text:
        return "overdue"
    if "pending" in text:
        return "pending"
    if "completed" in text or "complete" in text or "done" in text:
        return "completed"
    if "high priority" in text or "critical" in text or "urgent" in text:
        return "high_priority"
    if "project" in text:
        return "projects"
    if "how many" in text or "count" in text or "total" in text:
        return "count"

    return "all"
