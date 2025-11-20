import mysql.connector
from datetime import datetime, timedelta

MYSQL_CONFIG = {
            'host': 'apex-2025-ekco-2048.e.aivencloud.com',
            'user': 'avnadmin',
            'password': os.getenv('DB_PASS'),
            'port': 21911,
            'database': 'KRONOS',
            'ssl_disabled' : True
}

# ---------------------------
# Helper: connect to MySQL
# ---------------------------
def get_connection():
    return mysql.connector.connect(**MYSQL_CONFIG)

# ---------------------------
# Fetch completed tasks for the current week
# ---------------------------
def get_tasks_completed_this_week():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())  # Monday
    week_end = week_start + timedelta(days=6)             # Sunday

    query = """
        SELECT * FROM tasks
        WHERE status='Completed'
        AND deadline BETWEEN %s AND %s
    """
    cursor.execute(query, (week_start.date(), week_end.date()))
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return tasks, week_start.date(), week_end.date()

# ---------------------------
# Calculate total study hours for the week
# ---------------------------
def get_total_study_hours_this_week():
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())  # Monday
    week_end = week_start + timedelta(days=6)             # Sunday

    query = """
        SELECT SUM(duration_minutes) FROM sessions
        WHERE start_time BETWEEN %s AND %s
    """
    cursor.execute(query, (week_start, week_end))
    result = cursor.fetchone()
    total_hours = (result[0] or 0) / 60  # Convert minutes to hours
    cursor.close()
    conn.close()
    return total_hours

# ---------------------------
# Save user reflection
# ---------------------------
def save_reflection(week_start, week_end, reflection_text):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO reflections (week_start_date, week_end_date, reflection_text)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (week_start, week_end, reflection_text))
    conn.commit()
    cursor.close()
    conn.close()

# ---------------------------
# Display weekly summary
# ---------------------------
def display_weekly_summary():
    tasks, week_start, week_end = get_tasks_completed_this_week()
    total_hours = get_total_study_hours_this_week()

    print(f"\ Weekly Summary: {week_start} to {week_end}\n")
    
    if tasks:
        print(" Completed Tasks:")
        for task in tasks:
            print(f"- {task['title']} ({task['module']}) | Deadline: {task['deadline']} | Status: {task['status']}")
    else:
        print(" No tasks completed this week.")

    print(f"\n Total study hours this week: {total_hours:.2f} hrs")

    # Motivational feedback
    if total_hours >= 15:
        print("🎉 Amazing! You studied a lot this week!")
    elif total_hours >= 7:
        print("👍 Good progress! Keep it up!")
    else:
        print("💪 Keep going! Try adding one more study session tomorrow.")

    # ---------------------------
    # User reflection input
    # ---------------------------
    print("\n📝 Weekly Reflection:")
    reflection = input("What did you learn this week?\n")
    reflection += "\n" + input("What challenged you this week?\n")
    reflection += "\n" + input("What will you do differently next week?\n")

    save_reflection(week_start, week_end, reflection)
    print("✅ Reflection saved!\n")

# ---------------------------
# Main program
# ---------------------------
if __name__ == "__main__":
    display_weekly_summary()

