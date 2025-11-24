
from datetime import datetime, timedelta
from datahandler import DatabaseConnector

data_handler = DatabaseConnector()
data_handler.connect()
def get_current_week_dates():
    current_date = datetime.now().date()
    start_week = current_date - timedelta(days=current_date.weekday())
    end_week = start_week + timedelta(days=6)
    
    return start_week, end_week


def generate_weekly_summary():
    week_start, week_end = get_current_week_dates()

    # Connect once
    database = DatabaseConnector()
    if not database.connect():
        print("Unable to connect to the database.")
        return

    print("\n""==================================================")
    print(f"WEEKLY SUMMARY: {week_start} to {week_end}")
    print("\n""==================================================")

    #The hours
    sql_hours = """
        SELECT SUM(duration_minutes) AS total_minutes 
        FROM sessions 
        WHERE session_type='work' 
        AND DATE(start_time) BETWEEN %s AND %s
    """
    database.cursor.execute(sql_hours, (week_start, week_end))
    result = database.cursor.fetchone()
    total_minutes = result['total_minutes'] if result['total_minutes'] else 0
    total_hours = round(float(total_minutes) / 60.0, 1)

    #  getting the task complede 
    sql_completed = """
        SELECT COUNT(*) AS completed 
        FROM tasks 
        WHERE status='Completed'
        AND DATE(updated_at) BETWEEN %s AND %s
    """
    database.cursor.execute(sql_completed, (week_start, week_end))
    completed_tasks = database.cursor.fetchone()['completed']

    # getting the  tasks due 
    sql_due = """
        SELECT COUNT(*) AS due_count 
        FROM tasks 
        WHERE deadline BETWEEN %s AND %s
    """
    database.cursor.execute(sql_due, (week_start, week_end))
    tasks_due = database.cursor.fetchone()['due_count']

    # getting the missed deadlines
    sql_missed = """
        SELECT COUNT(*) AS missed 
        FROM tasks 
        WHERE status='Overdue'
        AND deadline BETWEEN %s AND %s
    """
    database.cursor.execute(sql_missed, (week_start, week_end))
    missed_deadlines = database.cursor.fetchone()['missed']

    # Getting the most productive days bellow
    sql_productive = """
        SELECT DATE(start_time) AS study_day, 
               SUM(duration_minutes) AS minutes
        FROM sessions
        WHERE session_type='work'
        AND DATE(start_time) BETWEEN %s AND %s
        GROUP BY DATE(start_time)
        ORDER BY minutes DESC
        LIMIT 1
    """
    database.cursor.execute(sql_productive, (week_start, week_end))
    row = database.cursor.fetchone()

    if row:
        productive_day = row['study_day']
        productive_hours = round(float(row['minutes']) / 60.0, 1)
    else:
        productive_day = "None"
        productive_hours = 0
    print("\n""--------------------------------------------------")
    print("---------------WEEK STATISTICS:------------------------")
    print("--------------------------------------------------")
    print("COMPLETED TASKS:")
    print(f"    You completed {completed_tasks} out of {tasks_due} assignments this week")
    print("TOTAL HOURS STUDIED:")
    print(f"    You studied for {total_hours} hours total")
    print("MOST PRODUCTIVE DAY:")
    print(f"    Your most productive day was {productive_day} ({productive_hours} hours)\n")
    print("\n""--------------------------------------------------")

    # Tasks completed
    target_Sql = """
        SELECT title, DATE(updated_at) AS completion_date
        FROM tasks
        WHERE status='Completed'
        AND DATE(updated_at) BETWEEN %s AND %s
        ORDER BY updated_at DESC
    """
    database.cursor.execute(target_Sql, (week_start, week_end))
    completed_list = database.cursor.fetchall()

    print("COMPLETED TASK THIS WEEK:")
    if completed_list:
        for t in completed_list:
            print(f"{t['title']} (completed {t['completion_date']})")
    else:
        print("No tasks completed this week. Please try to improve next time")
    print()

    #Areas of improvement
    print("\n""--------------------------------------------------")
    print("IMPROVEMENT AREAS:")
    if missed_deadlines > 0:
        print(f"You missed {missed_deadlines} deadlines this week")
    else:
        print("Great job! No missed deadlines this week!, keep it up!")

    # Weekend study time Check
    sql_weekend = """
        SELECT SUM(duration_minutes) AS weekend_minutes
        FROM sessions
        WHERE session_type='work'
        AND DAYOFWEEK(start_time) IN (1,7)
        AND DATE(start_time) BETWEEN %s AND %s
    """
    database.cursor.execute(sql_weekend, (week_start, week_end))
    weekend_minutes = database.cursor.fetchone()['weekend_minutes'] or 0

    if weekend_minutes < 60:
        print("Tip: You studied less on weekends. Try adding one session on Saturday.")

    if total_hours < 10:
        print("Tip: Try to increase your study time. Aim for at least 10 hours per week.")

    database.close()
    print("\n""--------------------------------------------------")

def write_reflection():
    data_handler.connect()
    week_start, week_end = get_current_week_dates()
    
    print("\n""--------------------------------------------------")
    print("========= WEEKLY REFLECTION ====================")
    print("\n""--------------------------------------------------")
    print("Take a moment to reflect on yourself for the week.\n")
    
    # Ask reflection questions
    print("What did you learn this week?")
    learning = input("Your answer: ").strip()
    print("\n""--------------------------------------------------")
    print("\nWhat went well?")
    went_well = input("Your answer: ").strip()
    print("\n""--------------------------------------------------")
    print("\nWhat was challenging?")
    challenge = input("Your answer: ").strip()
    print("\n""--------------------------------------------------")
    print("\nWhat will you do differently next week?")
    next_actions = input("Your answer: ").strip()

    # Now creating a message using a variable
    reflection_text = f"""
    --------------------------------------------------

    What I learned: {learning}
    What went well: {went_well}
    What was challenging: {challenge}
    Future changes: {next_actions}

    --------------------------------------------------
    """


    # Saving the message to database
    database = DatabaseConnector()
    database.add_reflection(week_start, week_end, reflection_text)

    print("\nReflection saved successfully!")
    print("\n""--------------------------------------------------")


def view_past_reflections():

    database = DatabaseConnector()

    if not database.connect():
        print("Unable to connect to the database.")
        return

    reflections = database.fetch_reflections()
    
    print("\n--------------------------------------------------")
    print("========= PAST REFLECTIONS ================")
    print("\n--------------------------------------------------")
    
    if not reflections:
        print("No reflections saved yet.")
        print("Make sure to start writing reflections to track your progress over time!\n")
        return
    
    for reflection in reflections:
        week_start = reflection['week_start']
        week_end = reflection['week_end']
        reflection_text = reflection['reflection_text']
        
        print(f"Week: {week_start} to {week_end}")
        print(reflection_text)
        print()
    
    print("\n--------------------------------------------------")

def deleting_reflections():
    database = DatabaseConnector()   
    if not database.connect():
        print("Unable to connect to the database.")
        return
    database.cursor.execute("""
        SELECT id, week_start, week_end
        FROM reflections
        ORDER BY week_start DESC
    """)
    reflections = database.cursor.fetchall()

    print("\nAvailable reflections:\n")
    for r in reflections:
        print(f"ID: {r['id']} | From:{r['week_start']} To: {r['week_end']}")

    choice = input("\nEnter the ID of the reflection you want to delete: ")

    if not database.remove_reflection(choice):
        print("invalid input please try again")
    else:
        database.remove_reflection(choice)
   
def past_reflections_menu():
    print("===== PAST REFLECTIONS MENU =======")
    print(" 1.View past reflections")
    print(" 2.Edit past reflection")
    print(" 3.Delete reflection")
    
    choice = input("\nChoose an option (1-2): ").strip()
    if choice == "1":
        view_past_reflections()
    elif choice =="2":
        updating_reflections()
    elif choice == "3":
        deleting_reflections()
    else:
        print("Invalid option. Please choose 1, 2, or 3")
def updating_reflections():
    database = DatabaseConnector()

  
    if not database.connect():
        print("Unable to connect to the database.")
        return

    reflections = database.fetch_reflections()
    if not reflections:
        print("No reflections found.")
        return

    for r in reflections:
        print(f"ID: {r['id']} | From: {r['week_start']} To: {r['week_end']}")

    option = input("\nEnter reflection ID to edit: ").strip()

    # Asking for new text
    print("\nEnter your updated reflection (type END on a new line to finish):")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)

    new_text = "\n".join(lines)

    # Update in database
    success = database.edit_reflection(option, new_text)

    if success:
        print("\nReflection updated successfully!")
    else:
        print("\nFailed to update reflection. Please try again.")

    database.close()

def weekly_summary_menu():
    while True:
        print("\n""--------------------------------------------------")
        print("=========== WEEKLY SUMMARY MENU ===========")
        print("--------------------------------------------------")
        print("1. Generate this week's summary")
        print("2. Write weekly reflection")
        print("3. Past reflections")
        print("4. Back to main menu")
        print("\n""--------------------------------------------------")
        
        choice = input("\nChoose an option (1-4): ").strip()
        
        if choice == "1":
            generate_weekly_summary()
        elif choice == "2":
            write_reflection()
        elif choice == "3":
            past_reflections_menu()       
        elif choice == "4":
            print("\nReturning to main menu...\n")
            break
        else:
            print("\nInvalid option. Please choose 1, 2, 3, or 4.\n")


# This allows you to run this file directly for testing
if __name__ == "__main__":
    weekly_summary_menu()
