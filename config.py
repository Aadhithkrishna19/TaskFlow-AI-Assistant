
import os
from dotenv import load_dotenv

# Load variables from a local .env file (if one exists) into the
# environment. In production you would instead set real environment
# variables on the server.
load_dotenv()

# ---------------------------------------------------------------------
# Database configuration
# ---------------------------------------------------------------------
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "taskflow_db")

# ---------------------------------------------------------------------
# AI / HelpFlow configuration
# ---------------------------------------------------------------------
# AI_PROVIDER selects which AI backend HelpFlow uses to phrase answers:
# "gemini" (Google, has a free tier) or "openai". If neither key is
# set, HelpFlow automatically falls back to simple template answers.
AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
AI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# ---------------------------------------------------------------------
# App branding
# ---------------------------------------------------------------------
APP_NAME = "TaskFlow"
APP_TAGLINE = "Smart Task Management"
ASSISTANT_NAME = "HelpFlow"
ASSISTANT_TAGLINE = "Your AI TaskFlow Assistant"

# ---------------------------------------------------------------------
# Business constants (kept here so every file agrees on the same lists)
# ---------------------------------------------------------------------
TASK_STATUSES = ["Pending", "In Progress", "Completed", "Cancelled"]
TASK_PRIORITIES = ["Low", "Medium", "High", "Critical"]
PROJECT_STATUSES = ["Planning", "Active", "Completed", "On Hold"]
USER_ROLES = ["Admin", "Manager", "Employee"]

# ---------------------------------------------------------------------
# Theme colors (used by utils/ui.py to style the app)
# ---------------------------------------------------------------------
COLOR_PRIMARY = "#0B1F3A"      # Dark Navy Blue
COLOR_SECONDARY = "#1E5FBF"    # Blue
COLOR_BACKGROUND = "#F5F6F8"   # Light Gray
COLOR_CARD = "#FFFFFF"         # White
COLOR_TEXT = "#2B2B2B"         # Dark Gray