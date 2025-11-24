# Time Management System
By: Apex Technologies LTD

# Project Kronos 🎓⏱️

> A Python-based CLI productivity tool designed to help students manage assignments, track study time, and improve academic performance.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Database](https://img.shields.io/badge/database-MySQL-orange.svg)](https://www.mysql.com/)

---

## 📋 Overview

Project Kronos is a comprehensive time management system that helps students organize their academic workload, optimize study schedules, and track productivity. Named after the Greek god of time, Kronos provides:

- **Assignment Management** - Create, edit, and track tasks with deadlines
- **Smart Scheduling** - Priority-based task organization using urgency algorithms
- **Pomodoro Timer** - 25-minute focus sessions with automatic logging
- **Progress Analytics** - Visual reports of study hours and completion rates
- **Weekly Summaries** - Comprehensive reports with reflection prompts

---

## 🏗️ Project Structure

```
kronos/
├── main.py                    # Main application menu
├── datahandler.py            # MySQL database operations
├── TaskManager.py            # Assignment CRUD operations (Eric)
├── time_allocator.py         # Task prioritization (Raphael)
├── PomodoroTimer.py          # Study timer with session logging (Albert)
├── progress_analyzer.py      # Statistics and analytics (Alvin)
├── weeklysummary.py          # Weekly reports and reflections (Michael)
├── .env                      # Database credentials (not committed)
└── README.md
```

### Database Schema

The application uses MySQL with four main tables:

- **tasks** - Stores assignments with title, deadline, estimated hours, and status
- **sessions** - Logs study sessions with duration and task associations
- **reflections** - Saves weekly reflection entries
- **preferences** - Stores user settings (optional)

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8+
- MySQL database access (hosted on Aiven cloud)
- Required Python packages: `mysql-connector-python`, `python-dotenv`

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/EricChuwa/TimeManagementSystem.git
   cd TimeManagementSystem
   ```

2. **Install dependencies**
   ```bash
   pip install mysql-connector-python python-dotenv
   ```

3. **Configure database credentials**
   
   Create a `.env` file in the project root:
   ```
   DB_PASS=your_database_password
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

---

## 💻 Usage Guide

### Main Menu

```
========== KRONOS STUDY TRACKER ==========
1. Manage Assignments
2. View Study Plan
3. Start Timer
4. View Progress
5. Weekly Summary
6. Exit
```

### Quick Workflows

#### Adding an Assignment
1. Select option `1` → Manage Assignments
2. Choose "Add Task"
3. Enter details: title, deadline (DD/MM/YYYY), estimated hours
4. Task is saved with "Pending" status

#### Starting a Study Session
1. Select option `3` → Start Timer
2. Enter study duration in minutes
3. Timer runs in 25-minute Pomodoro cycles with 5-minute breaks
4. Session automatically logs to database

#### Viewing Your Progress
1. Select option `4` → View Progress
2. See total study hours, completion rate, and daily breakdown
3. View ASCII bar charts of weekly activity

#### Generating Weekly Summary
1. Select option `5` → Weekly Summary
2. Review completed tasks and statistics
3. Answer reflection prompts (what went well, challenges, etc.)
4. Reflection is saved for future reference

---

## 🔧 Key Features

### 1. Assignment Tracker (`TaskManager.py`)
- Add, edit, complete, and view tasks
- Automatic status management (Pending, In Progress, Completed)
- Task filtering and organized display

### 2. Smart Time Allocator (`time_allocator.py`)
- Priority calculation: `priority = estimated_hours / days_remaining`
- Sorts tasks by urgency (higher score = more urgent)
- Displays prioritized task list with due dates

### 3. Focus Timer (`PomodoroTimer.py`)
- Customizable Pomodoro sessions (default: 25 min work, 5 min break)
- Real-time countdown display
- Automatic session logging to database
- Cycles through multiple Pomodoros for longer study periods

### 4. Progress Analytics (`progress_analyzer.py`)
- Total study hours calculation
- Task completion rate percentage
- 7-day study history with ASCII bar charts
- Motivational feedback based on performance

### 5. Weekly Summary (`weeklysummary.py`)
- Week statistics: hours studied, tasks completed, most productive day
- List of completed assignments
- Improvement suggestions (missed deadlines, weekend study tips)
- Reflection prompts for self-assessment
- View, edit, and delete past reflections

---

## 👥 Development Team

| Developer | Module | Focus |
|-----------|--------|-------|
| **Eric** | TaskManager.py | Task CRUD operations |
| **Raphael** | time_allocator.py | Priority algorithms |
| **Albert** | PomodoroTimer.py | Timer & session logging |
| **Alvin** | progress_analyzer.py | Analytics & statistics |
| **Michael** | weeklysummary.py | Reports & integration |

---

## 🔒 Database Configuration

The application connects to a MySQL database hosted on Aiven cloud:

```python
config = {
    'host': 'apex-2025-ekco-2048.e.aivencloud.com',
    'user': 'avnadmin',
    'password': os.getenv('DB_PASS'),
    'port': 21911,
    'database': 'KRONOS',
    'ssl_disabled': True
}
```

**Note:** Database credentials are stored in `.env` file and excluded from version control for security.

---

## 📝 License

This project is licensed under the MIT License. See LICENSE file for details.

---

## 🙏 Acknowledgments

Built to help students take control of their time and achieve academic excellence. Special thanks to the Pomodoro Technique by Francesco Cirillo for inspiration.

---

**Made with ❤️ by students, for students.**
kronos_readme.md
Displaying kronos_readme.md.
