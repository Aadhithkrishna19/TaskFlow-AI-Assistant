# 🗂️ TaskFlow — Smart Task Management

TaskFlow is a beginner-friendly, full-stack task and project management
web app built **entirely in Python** using **Streamlit**, with a MySQL
database and a built-in AI assistant called **HelpFlow**.

You do **not** need to know HTML, CSS, or JavaScript to run or extend
this project — everything is Python.

---

## 1. Project Overview

TaskFlow lets a company's team:

- Log in securely
- View a dashboard of task statistics and charts
- Create, edit, delete, and update tasks
- Assign tasks to teammates
- Create and manage projects
- View "My Tasks" (tasks assigned to you), with filters
- Ask **HelpFlow**, the built-in AI assistant, questions like:
  - "How do I create a task?"
  - "Show my pending tasks"
  - "What are my overdue tasks?"

---

## 2. Features

- 🔐 Secure login with bcrypt-hashed passwords
- 📊 Dashboard with KPI cards and a Plotly status chart
- ✅ Full task CRUD (create / read / update / delete / status change)
- 📁 Project management
- 🙋 Personal "My Tasks" view with filters
- 🤖 HelpFlow AI assistant with two capabilities:
  - **Application Help** — answers "how do I…" questions from a
    built-in knowledge base
  - **Database Assistance** — answers questions about your real task
    data by calling safe, predefined MySQL queries (never raw
    AI-generated SQL)
- 💬 Chat history saved to MySQL

---

## 3. Technologies

| Purpose            | Technology                  |
|---------------------|------------------------------|
| Language            | Python 3.10+                |
| Frontend / UI        | Streamlit                   |
| Database             | MySQL                       |
| DB driver            | mysql-connector-python      |
| Data handling        | Pandas                      |
| Charts               | Plotly                      |
| AI                    | OpenAI API (optional)       |
| Password hashing      | bcrypt                       |
| Config                | python-dotenv                |

---

## 4. Project Structure

```
TaskFlow/
│
├── app.py                  # Main entry point (run this file)
├── config.py                # All configuration & constants
│
├── database/                 # Everything that talks to MySQL
│   ├── connection.py
│   ├── users.py
│   ├── tasks.py
│   ├── projects.py
│   └── chat.py
│
├── pages/                     # One file per screen
│   ├── dashboard.py
│   ├── tasks.py
│   ├── projects.py
│   ├── my_tasks.py
│   └── helpflow.py
│
├── ai/                          # HelpFlow's brain
│   ├── assistant.py
│   ├── intent.py
│   └── knowledge_base.py
│
├── utils/                        # Shared helpers
│   ├── authentication.py
│   ├── task_utils.py
│   └── ui.py
│
├── sql/
│   └── taskflow_db.sql            # Creates the database + sample data
│
├── .env.example
├── requirements.txt
└── README.md
```

### What each folder does

- **database/** — All MySQL queries live here. Every other file asks
  these functions for data instead of writing SQL itself.
- **pages/** — Each file has one `render()` function that draws one
  screen. `app.py` calls the right one based on sidebar navigation.
- **ai/** — `knowledge_base.py` holds the "how do I..." answers,
  `intent.py` decides what kind of question was asked, and
  `assistant.py` ties it all together into HelpFlow's replies.
- **utils/** — Login/session handling, small validation helpers, and
  the shared visual theme.

---

## 5. MySQL Installation

If you don't already have MySQL installed:

- **Windows / Mac**: download MySQL Community Server from
  https://dev.mysql.com/downloads/mysql/ and install it (or install
  MySQL Workbench, which bundles the server).
- **Mac (Homebrew)**: `brew install mysql && brew services start mysql`
- **Linux (Ubuntu/Debian)**: `sudo apt install mysql-server`

Make sure the MySQL server is running before continuing.

---

## 6. Create the Database

Open `sql/taskflow_db.sql` in **MySQL Workbench** and execute the
whole script, **or** run it from a terminal:

```bash
mysql -u root -p < sql/taskflow_db.sql
```

This creates the `taskflow_db` database, all 4 tables, and inserts
5 sample users, 4 sample projects, and 20 sample tasks.

---

## 7. Python Environment Setup

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

---

## 8. Installing Requirements

```bash
pip install -r requirements.txt
```

---

## 9. .env Configuration

Copy the example file and fill in your real values:

```bash
cp .env.example .env
```

Then edit `.env`:

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=taskflow_db

OPENAI_API_KEY=your_openai_api_key
AI_MODEL=gpt-4o-mini
```

> **Note:** `OPENAI_API_KEY` is optional. If you leave it blank,
> HelpFlow still works — it will use clear, template-based answers
> instead of AI-generated phrasing.

---

## 10. Running the Application

```bash
streamlit run app.py
```

Streamlit will open the app in your browser (usually at
`http://localhost:8501`).

---

## 11. Sample Login Credentials

All sample users share the same password: **`password123`**

| Email                   | Role     |
|--------------------------|----------|
| alice@taskflow.com       | Admin    |
| bob@taskflow.com         | Manager  |
| carla@taskflow.com       | Manager  |
| daniel@taskflow.com      | Employee |
| emily@taskflow.com       | Employee |

---

## 12. HelpFlow Architecture

```
User types a message
        ↓
ai/intent.py detects intent:
  APPLICATION_HELP  or  DATABASE_QUERY
        ↓
   ┌────────────┴─────────────┐
   ↓                           ↓
ai/knowledge_base.py     database/tasks.py or
(instructions)             database/projects.py
                           (safe predefined functions
                            like get_pending_tasks())
   └────────────┬─────────────┘
                ↓
   ai/assistant.py sends the retrieved
   facts to the OpenAI API to phrase a
   natural-language answer (or falls back
   to a template if no API key is set)
                ↓
   database/chat.py saves the exchange
                ↓
       Response shown to the user
```

HelpFlow **never** lets the AI write or run its own SQL — it only ever
calls already-safe, parameterized functions like `get_pending_tasks()`,
`get_completed_tasks()`, `get_overdue_tasks()`, `get_task_count()`, and
`get_project_list()`.

---

## 13. Future Improvements

- Add task comments and file attachments
- Add email notifications for due/overdue tasks
- Add role-based permissions (e.g. only Managers can create projects)
- Add a Kanban board view for tasks
- Let HelpFlow create/update tasks directly from chat (with confirmation)
- Add unit tests for the `database/` and `ai/` modules
