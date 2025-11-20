import mysql.connector
from datetime import datetime, timedelta
from datahandler import DatabaseConnector


def get_connection():
    """Return a new DatabaseConnector instance that is connected."""
    database = DatabaseConnector()
    if not database.connect():
        print("Unable to connect to the database.")
        return None
    return database


def get_all_tasks():
    """Fetch all tasks from the tasks table."""
    database = get_connection()
    if not database:
        return []

    cursor = database.cursor
    try:
        cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as err:
        print(f"Error fetching tasks: {err}")
        return []
    finally:
        cursor.close()
        database.close()


def get_total_study_hours():
    """Calculate total study hours from sessions table."""
    database = get_connection()
    if not database:
        return 0

    cursor = database.cursor
    try:
        cursor.execute("SELECT SUM(duration_minutes) AS total_minutes FROM sessions")
        row = cursor.fetchone()

        total_minutes = row['total_minutes'] if row and row['total_minutes'] else 0
        return round(total_minutes / 60, 2)
        
    except mysql.connector.Error as err:
        print(f"Error calculating study hours: {err}")
        return 0
    finally:
        cursor.close()
        database.close()

def get_completed_tasks_count():
    """Return number of completed tasks."""
    database = get_connection()
    if not database:
        return 0

    cursor = database.cursor
    try:
        cursor.execute("SELECT COUNT(*) AS total FROM tasks WHERE status='Completed'")
        row = cursor.fetchone()
        return row['total'] if row else 0      # Use dict key
    except mysql.connector.Error as err:
        print(f"Error counting tasks: {err}")
        return 0
    finally:
        cursor.close()
        database.close()


def get_task_completion_rate():
    """Return completion percentage."""
    tasks = get_all_tasks()
    if not tasks:
        return 0

    total = len(tasks)
    completed = sum(1 for t in tasks if t["status"] == "Completed")
    return round((completed / total) * 100, 2)


def get_study_hours_by_day(days=7):
    """Return dict of daily study hours for the last N days."""
    database = get_connection()
    if not database:
        return {}

    cursor = database.cursor
    try:
        start = datetime.now() - timedelta(days=days)
        cursor.execute("""
            SELECT DATE(start_time) AS day, SUM(duration_minutes) AS total_minutes
            FROM sessions
            WHERE start_time >= %s
            GROUP BY DATE(start_time)
            ORDER BY DATE(start_time)
        """, (start,))

        rows = cursor.fetchall()
        return {
            row["day"].strftime("%Y-%m-%d"): round(row["total_minutes"] / 60, 2)
            for row in rows
        }

    except mysql.connector.Error as err:
        print(f"Error fetching study hours: {err}")
        return {}
    finally:
        cursor.close()
        database.close()


def display_progress_summary():
    """Print a summary of user progress."""
    print("--------------------------------------------------")
    print("\n========== KRONOS STUDY PROGRESS SUMMARY ==========")
    print("--------------------------------------------------")
    tasks = get_all_tasks()
    total_tasks = len(tasks)
    completed = get_completed_tasks_count()
    rate = get_task_completion_rate()
    hours = get_total_study_hours()
    daily_hours = get_study_hours_by_day()

    print(f" Total Tasks: {total_tasks}")
    print(f" Completed Tasks: {completed}")
    print(f" Completion Rate: {rate}%")
    print(f" Total Study Hours: {hours} hrs\n")

    print(" Study Hours (Last 7 Days):")
    for day, hrs in daily_hours.items():
        print(f"{day}: {'█' * int(hrs)} ({hrs} hrs)")

    # feedback
    if rate == 100:
        print("\n Excellent work!")
    elif rate >= 70:
        print("\n Good progress!")
    else:
        print("\n Keep pushing!")


if _name_ == "_main_":
    display_progress_summary()
