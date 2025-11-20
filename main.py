# import PomodoroTimer
import sqlite3
import os
import mysql.connector
from datetime import datetime, timedelta
from datahandler import DatabaseConnector
from weeklysummary import *
from PomodoroTimer import *
from progress_analyzer import *
def display_menu():
    print("========== KRONOS STUDY TRACKER ==========")
    print("1. Manage Assignments")
    print("2. View Study Plan")
    print("3. Start Timer")
    print("4. View Progress")
    print("5. Weekly Summary")
    print("6. Exit")
    print("==========================================")
while True:
    display_menu()
    choice = input("Choose an option (1-6)")
    if choice.strip() == " ":
          print("Invalid option. Please enter a number between 1 and 6.")
          continue
    if choice =="1": # Eric's code
         print("Erics")
    if choice =="2":# Raphael's code
         print("Rafeals")
    if choice == "3":# Albert's code
         pomodoro_main()
    if choice =="4":# Alvin's code
         display_progress_summary()
    if choice =="5":# My code
         weekly_summary_menu()
    if choice =="6": # My code
         print("Thank you for using this platform.")  
         exit
    else:
         print("Invalid input. Please enter(1-6)")
         continue

    
