import datahandler
from datetime import date
from collections import namedtuple

class TaskManager():
    def __init__(self):
        self.database_handler = datahandler.DatabaseConnector()
        Menu = namedtuple('Menu', ['desc', 'func'])

        self.menu_options = {
            "1" : Menu("Add Task", self.add_task),
            "2" : Menu("Edit Task", 'self.edit_task'),
            "3" : Menu("Complete Task", 'self.complete_task'),
            "4" : Menu("View_Tasks", 'self.view_tasks'),
            "5" : Menu("Return to main Menu", None)
        }

    def add_task(self): 
        task_name = input("Enter Task Name: ")

        # Saving deadline
        try:
            print("When is your due date: ")
            due_day = int(input("Enter Day (DD): "))
            due_month = int(input("Enter Month (MM): "))
            due_year = int(input("Enter Year (YYYY): ")) 

            deadline = date(due_year, due_month, due_day).strftime('%Y-%m-%d')
        except ValueError:
            print("Error!! Invalid date entered")
            return #

        # Saving estimated hours
        try:
            estimated_hours = float(input("What is the estimated time to completion (Hours, e.g. 2.5): "))
            if estimated_hours <= 0 or estimated_hours > 100:
                print("Estimated hours must be a positive number less than 100.")
                return
        except ValueError:
            print("Error!! You must enter a number for hours (e.g. 3 or 2.5)")
            return

        self.database_handler.add_task(task_name, deadline, estimated_hours)
        print("\nTask Successfully added!\n")

    def menu_display(self):
        for key, item in self.menu_options.items():
            print(f"{key}: {item.desc}")

    def main(self):
        while True:
            print("Kronos: ")
            self.menu_display()

            user_choice = input("Enter Selection: ")

            menu_item = self.menu_options.get(user_choice)

            if menu_item:
                if menu_item.func:
                    menu_item.func()
                else:
                    print("Toodles... ")
                    break
            else:
                print("Invalid Selection")

test = TaskManager()
test.main()
