#importing database handler
from collections import namedtuple

# Importing peoples files
from weeklysummary import *
from PomodoroTimer import *
from progress_analyzer import *
from TaskManager import *
from time_allocator import *

# Initializing class handlers
task_handler = TaskManager()
time_allocater = TimeAllocator()
data_handler = DatabaseConnector()

data_handler.connect()

Menu = namedtuple('Menu', ['desc', 'func'])

home_menu = {
     "1" : Menu('Manage Assignments', task_handler.main),
     "2" : Menu('View Study Plan', time_allocater.main),
     "3" : Menu('Start Timer', pomodoro_main),
     "4" : Menu('View Progress', display_progress_summary),
     "5" : Menu('Weekly Summary', weekly_summary_menu),
     "0" : Menu('Exit', None)
}

def display_menu():
     print("\n==========================================")
     print("                 <KRONOS>                 ")
     print("==========================================")

     print("\n========== KRONOS STUDY TRACKER ==========")
     for key, item in home_menu.items():
          print(f"{key}. {item.desc}")
     print("==========================================")

while True:  
     display_menu()
     choice = input("Enter Selection (1-6): ")
     menu_item = home_menu.get(choice)

     if menu_item:
          if menu_item.func:
               menu_item.func()
          else:
               break 
     else:
          print('Invalid Option!')


    
