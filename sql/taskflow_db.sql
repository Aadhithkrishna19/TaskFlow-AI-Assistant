-- =====================================================================
-- taskflow_db.sql
-- ---------------
-- WHAT THIS FILE DOES:
-- Creates the "taskflow_db" MySQL database, all four tables (users,
-- projects, tasks, chat_history), their foreign keys, and inserts
-- realistic sample data (5 users, 4 projects, 20 tasks).
--
-- HOW TO USE:
-- Open this file in MySQL Workbench (or run it via the mysql CLI:
--   mysql -u root -p < sql/taskflow_db.sql
-- ) and execute it. It will create everything TaskFlow needs.
--
-- SAMPLE LOGIN (all sample users share this password):
--   Password for every sample user: password123
-- =====================================================================

CREATE DATABASE IF NOT EXISTS taskflow_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE taskflow_db;

-- ---------------------------------------------------------------------
-- Table: users
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS chat_history;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,   -- bcrypt hash, never plain text
    role ENUM('Admin', 'Manager', 'Employee') NOT NULL DEFAULT 'Employee',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------------
-- Table: projects
-- ---------------------------------------------------------------------
CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(150) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    status ENUM('Planning', 'Active', 'Completed', 'On Hold') NOT NULL DEFAULT 'Planning',
    manager_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (manager_id) REFERENCES users(id) ON DELETE SET NULL
);

-- ---------------------------------------------------------------------
-- Table: tasks
-- ---------------------------------------------------------------------
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    project_id INT,
    assigned_to INT,
    priority ENUM('Low', 'Medium', 'High', 'Critical') NOT NULL DEFAULT 'Medium',
    status ENUM('Pending', 'In Progress', 'Completed', 'Cancelled') NOT NULL DEFAULT 'Pending',
    due_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL,
    FOREIGN KEY (assigned_to) REFERENCES users(id) ON DELETE SET NULL
);

-- ---------------------------------------------------------------------
-- Table: chat_history
-- ---------------------------------------------------------------------
CREATE TABLE chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    user_message TEXT NOT NULL,
    assistant_response TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- =====================================================================
-- SAMPLE DATA
-- =====================================================================

-- ---------------------------------------------------------------------
-- 5 sample users (password for all of them is: password123)
-- ---------------------------------------------------------------------
INSERT INTO users (username, email, password, role) VALUES
('alice',   'alice@taskflow.com',   '$2b$12$KwedJ2FD91CRNUKNGaemZeKB.di2B5bszjZ4aZdBgusepvNnhaiHW', 'Admin'),
('bob',     'bob@taskflow.com',     '$2b$12$KwedJ2FD91CRNUKNGaemZeKB.di2B5bszjZ4aZdBgusepvNnhaiHW', 'Manager'),
('carla',   'carla@taskflow.com',   '$2b$12$KwedJ2FD91CRNUKNGaemZeKB.di2B5bszjZ4aZdBgusepvNnhaiHW', 'Manager'),
('daniel',  'daniel@taskflow.com',  '$2b$12$KwedJ2FD91CRNUKNGaemZeKB.di2B5bszjZ4aZdBgusepvNnhaiHW', 'Employee'),
('emily',   'emily@taskflow.com',   '$2b$12$KwedJ2FD91CRNUKNGaemZeKB.di2B5bszjZ4aZdBgusepvNnhaiHW', 'Employee');

-- ---------------------------------------------------------------------
-- 4 sample projects
-- ---------------------------------------------------------------------
INSERT INTO projects (project_name, description, start_date, end_date, status, manager_id) VALUES
('Website Development', 'Redesign and rebuild the company marketing website.', '2026-06-01', '2026-10-31', 'Active', 2),
('Mobile Application', 'Build the companion iOS/Android app for customers.', '2026-05-15', '2026-12-15', 'Active', 3),
('Customer Support System', 'Internal ticketing and support portal for the support team.', '2026-03-01', '2026-08-01', 'On Hold', 2),
('Internal Automation', 'Automate recurring internal reporting and workflows.', '2026-07-01', '2026-11-30', 'Planning', 3);

-- ---------------------------------------------------------------------
-- 20 sample tasks
-- ---------------------------------------------------------------------
INSERT INTO tasks (title, description, project_id, assigned_to, priority, status, due_date) VALUES
('Design dashboard',              'Create the high-fidelity design for the new dashboard UI.',        1, 4, 'High',     'In Progress', '2026-09-10'),
('Create login system',           'Build secure login and session handling.',                          1, 4, 'Critical', 'Pending',     '2026-09-05'),
('Fix notification issue',        'Notifications are not firing for overdue tasks.',                   1, 5, 'High',     'Pending',     '2026-09-03'),
('Develop task API',              'Build REST endpoints for task CRUD operations.',                     1, 5, 'Medium',   'In Progress', '2026-09-20'),
('Prepare project report',        'Compile the monthly status report for stakeholders.',               1, 2, 'Low',      'Completed',   '2026-08-25'),
('Set up CI/CD pipeline',         'Automate build and deployment for the website.',                    1, 5, 'Medium',   'Pending',     '2026-09-15'),
('Design app wireframes',         'Sketch wireframes for the main app screens.',                        2, 4, 'High',     'Completed',   '2026-08-20'),
('Implement push notifications',  'Add push notification support for task reminders.',                 2, 5, 'Medium',   'In Progress', '2026-09-18'),
('Build offline mode',            'Allow the app to function without an internet connection.',         2, 4, 'Critical', 'Pending',     '2026-09-25'),
('App store submission',          'Prepare and submit the app for App Store / Play Store review.',     2, 3, 'High',     'Pending',     '2026-10-01'),
('QA testing pass',               'Full regression test of the mobile app.',                            2, 5, 'Medium',   'Pending',     '2026-09-12'),
('Design ticket workflow',        'Map out the support ticket lifecycle and statuses.',                3, 2, 'Medium',   'Completed',   '2026-07-15'),
('Build support portal UI',       'Create the customer-facing support portal interface.',              3, 4, 'Low',      'Cancelled',   '2026-08-01'),
('Integrate email support',       'Connect the ticketing system to the support email inbox.',           3, 5, 'Medium',   'Pending',     '2026-08-28'),
('Automate weekly reports',       'Script to auto-generate and email weekly status reports.',           4, 3, 'Medium',   'Pending',     '2026-09-08'),
('Build Slack integration',       'Send task updates to a Slack channel automatically.',               4, 4, 'Low',      'Pending',     '2026-09-22'),
('Audit internal workflows',      'Review current manual processes for automation opportunities.',     4, 2, 'High',     'In Progress', '2026-09-06'),
('Fix database backup script',    'Nightly backup script is failing intermittently.',                   4, 5, 'Critical', 'Pending',     '2026-08-30'),
('Update employee onboarding doc', 'Refresh the onboarding checklist for new hires.',                   3, 3, 'Low',      'Completed',   '2026-08-10'),
('Plan Q4 roadmap',               'Draft the product roadmap for the next quarter.',                    1, 2, 'High',     'Pending',     '2026-09-28');
