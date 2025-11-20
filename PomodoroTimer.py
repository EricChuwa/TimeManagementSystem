import time
from datetime import datetime, timedelta
from datahandler import *
def timestamp(min):
    total_minutes = min
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=total_minutes)
    return start_time, end_time , total_minutes
def adding_to_database(min):
    details=timestamp(min)
    database = DatabaseConnector()   
    if not database.connect():
        print("Unable to connect to the database.")
        return
    success=database.add_session(1,details[0],details[1],details[2],"work")
    if success:
        print("\nSesion added successfully!")
    else:
        print("\nFailed to add a session. Please try again.")

    database.close()
def countdown(minutes, label):
    total_seconds = minutes * 60
    while total_seconds:
        mins, secs = divmod(total_seconds, 60)
        print(f"\r {label}: {mins:02d}:{secs:02d}", end="")
        time.sleep(1)
        total_seconds -= 1
    print(f"\n {label} complete!")

def pomodoro_session(total_minutes):
    cycles = total_minutes // 30
    remainder = total_minutes % 30
    print(f"\nTotal time: {total_minutes} minutes → {cycles} Pomodoro cycles + {remainder} extra minutes")

    for i in range(cycles):
        print(f"\n Cycle {i+1} - Study for 25 minutes")
        countdown(25, "Study time")
        print("Great job! Time for a 5-minute break.")
        countdown(5, "Break time")

    if remainder >= 5:
        print(f"\n Final study block: {remainder - 5} minutes")
        countdown(remainder - 5, "Study time")
        print("Final 5-minute break")
        countdown(5, "Break time")
    elif remainder > 0:
        print(f"\nFinal short study block: {remainder} minutes")
        countdown(remainder, "Study time")

    print("\nAll done! You’ve completed your study session.")
def set_session_minutes():
    while True:
        try:
            total_minutes = int(input("Enter total study time in minutes: "))
            if total_minutes <= 0:
                print("Please enter a positive integer for minutes.")
                continue
            return total_minutes
        except ValueError:
            print("Invalid input. Please enter a valid number.")
def pomodoro_main():
    print("========== KRONOS STUDY TRACKER ==========")
    print("Starting Pomodoro Timer Session")
    minutes=set_session_minutes()
    adding_to_database(minutes)
    pomodoro_session(minutes)
if __name__ == "__main__":
    pomodoro_main()