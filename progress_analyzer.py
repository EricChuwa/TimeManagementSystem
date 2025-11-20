import mysql.connector
from datetime import datetime, timedelta

#  CHANGE THESE TO YOUR MYSQL CREDENTIALS
MYSQL_CONFIG = {
             'host': 'apex-2025-ekco-2048.e.aivencloud.com',
            'user': 'avnadmin',
            'password': os.getenv('DB_PASS'),
            'port': 21911,
            'database': 'KRONOS',
            'ssl_disabled' : True
}
def get_connection():
    """Establish and return a MySQL database connection."""
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f" Error connecting to MySQL: {err}")
        return None

def get_all_tasks():
    """Fetch all tasks from the tasks table."""
    conn = get_connection()
    if not conn:
        return []

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        return tasks
    except mysql.connector.Error as err:
        print(f" Error fetching tasks: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_total_study_hours():
    """Calculate total study hours from sessions table."""
    conn = get_connection()
    if not conn:
        return 0

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT SUM(duration_minutes) FROM sessions")
        total_minutes = cursor.fetchone()[0]
        if total_minutes:
            return round(total_minutes / 60, 2)  # convert to hours
        return 0
    except mysql.connector.Error as err:
        print(f" Error calculating study hours: {err}")
        return 0
    finally:
        cursor.close()
        conn.close()

def get_completed_tasks_count():
    """Count number of completed tasks."""
    conn = get_connection()
    if not conn:
        return 0

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='Completed'")
        count = cursor.fetchone()[0]
        return count
    except mysql.connector.Error as err:
        print(f" Error counting completed tasks: {err}")
        return 0
    finally:
        cursor.close()
        conn.close()

def get_task_completion_rate():
    """Calculate task completion percentage."""
    tasks = get_all_tasks()
    total_tasks = len(tasks)
    if total_tasks == 0:
        return 0
    completed_tasks = len([t for t in tasks if t['status'] == 'Completed'])
    return round((completed_tasks / total_tasks) * 100, 2)

def get_study_hours_by_day(days=7):
    """Return dictionary of hours studied per day for the last 'days' days."""
    conn = get_connection()
    if not conn:
        return {}

    cursor = conn.cursor(dictionary=True)
    try:
        start_date = datetime.now() - timedelta(days=days)
        cursor.execute("""
            SELECT DATE(start_time) AS day, SUM(duration_minutes) AS total_minutes
            FROM sessions
            WHERE start_time >= %s
            GROUP BY DATE(start_time)
            ORDER BY DATE(start_time)
        """, (start_date,))
        data = cursor.fetchall()
        day_hours = {row['day'].strftime('%Y-%m-%d'): round(row['total_minutes']/60, 2) for row in data}
        return day_hours
    except mysql.connector.Error as err:
        print(f" Error fetching daily study hours: {err}")
        return {}
    finally:
        cursor.close()
        conn.close()

def display_progress_summary():
    """Print a summary of user progress."""
    print("\n========== KRONOS STUDY PROGRESS SUMMARY ==========")
    tasks = get_all_tasks()
    total_tasks = len(tasks)
    completed_tasks = get_completed_tasks_count()
    completion_rate = get_task_completion_rate()
    total_hours = get_total_study_hours()
    daily_hours = get_study_hours_by_day()

    print(f" Total Tasks: {total_tasks}")
    print(f" Completed Tasks: {completed_tasks}")
    print(f" Task Completion Rate: {completion_rate}%")
    print(f" Total Study Hours: {total_hours} hrs")

    print("\n Study Hours in the Last 7 Days:")
    for day, hours in daily_hours.items():
        bar = '█' * int(hours)
        print(f"{day}: {bar} ({hours} hrs)")

    # Motivational feedback
    if completion_rate == 100:
        print("\n🎉 Excellent! All tasks completed! Keep up the great work!")
    elif completion_rate >= 70:
        print("\n👍 Good job! Most tasks are completed. Stay consistent!")
    else:
        print("\n💪 Keep going! Try to complete more tasks this week!")

if __name__ == "__main__":
    display_progress_summary()

