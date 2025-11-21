import datahandler
from datetime import date
from collections import namedtuple


# Note ETC stands for Estimated Time for Completion
class TaskManager():
    def __init__(self):
        self.database_handler = datahandler.DatabaseConnector()
        Menu = namedtuple('Menu', ['desc', 'func'])

        self.main_menu_options = {
            "1" : Menu("Add Task", self.add_task),
            "2" : Menu("Edit Task", self.edit_task),
            "3" : Menu("Complete Task", self.complete_task),
            "4" : Menu("View_Tasks", self.view_tasks),
            "5" : Menu("Return to main Menu", None)
        }

        self.task_details_menu = {
            "1" : Menu("Name",lambda id,name: self.database_handler.edit_task(id, title=name)), 
            "2" : Menu("Deadline", lambda id, date: self.database_handler.edit_task(id, deadline=date)),
            "3" : Menu("Estimated Time for Completion", lambda id, etc: self.database_handler.edit_task(id, estimated_hours=etc)),
            "4" : Menu("Return", None)
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

    def edit_task(self): 
        tries = 0

        while tries < 3:
            tasks = self.database_handler.fetch_tasks() # fetches all tasks and saves them in this list of dictionaries
            valid_ids = {task['id'] for task in tasks} # Stors the existing ids

            print("Recorded Tasks: ")
            for task in tasks:
                print(f"{task['id']}. {task['title']}")
            print("0. Return to Previous Menu")

            user_selected_id = int(input("Enter Task Number: ")) # Assigns user id

            
            if user_selected_id  == 0:
                break
            elif user_selected_id in valid_ids:
                selected_task_details = self.database_handler.fetch_task_by_id(user_selected_id)

                while True:
                    # printing list of details
                    print(f"Task Name: {selected_task_details['title']}\nDeadline: {selected_task_details['deadline']}\nEstimated Time for Completion (ETC): {selected_task_details['estimated_hours']}\n")

                    self.menu_display(self.task_details_menu) # Printing detail menu

                    chosen_detail = input("Enter Selection: ")
                    menu_item = self.task_details_menu.get(chosen_detail)

                    if menu_item:
                        # Deals with deadline change
                        if menu_item.desc == 'Deadline':
                            try:
                                print("\nEnter Details")
                                day = int(input("Enter New Day (DD): "))
                                month = int(input("Enter New Month (MM): "))
                                year = int(input("Enter New Year (YYYY): "))
                                new_deadline = date(year,month,day).strftime('%Y-%m-%d') # Puts the date in correct format for database
                            except Exception as e:
                                print(f"!Error: {e}")

                            menu_item.func(user_selected_id, new_deadline)
                            print("\nUpdate Complete\n")
                            break
                        
                        # Deals with ETC change
                        elif menu_item.desc == 'Estimated Time for Completion':   
                            new_etc = int(input("\nEnter New Estimated Hours: "))

                            menu_item.func(user_selected_id, new_etc)
                            print("\nUpdate Complete\n")
                            break
                        
                        # Deals with title change
                        elif menu_item.desc == 'Name':
                            new_name = input("\nEnter New Assignment Name: ")

                            menu_item.func(user_selected_id, new_name)
                            print("\nUpdate Complete\n")
                            break

                        else:
                            break
                    else: 
                        print("\nInvalid Selection\n")
            else:
                print("\nInvalid Selection\n")
                
                if tries == 1: 
                    print("\nWARNING: This is your LAST attempt\n")
                
                tries+=1
                    
    def complete_task(self): 
        pending_tasks = self.database_handler.fetch_tasks_by_status('Pending')
        tasks_in_progress = self.database_handler.fetch_tasks_by_status('In Progress')

        for pending_task in pending_tasks: 
            print(f"{pending_task['id']}. {pending_task['title']} (Status: {pending_task['status']})")
        for task_in_progress in tasks_in_progress:
            print(f"{task_in_progress['id']}. {task_in_progress['title']} (Status: {task_in_progress['status']})")

        user_selection = int(input("Select the Number of the Task you wish to complete: "))

        self.database_handler.edit_task(user_selection, status = "Completed")
    
    def view_tasks(self):
        tasks = self.database_handler.fetch_tasks() # Saving all existing tasks into list

        print("Tasks: ")
        # Iterating through tasks
        for task in tasks:
            print(f"{task['id']}. {task['title']} (Status: {task['status']}) | Due: {task['deadline']}") 
        
    def menu_display(self, menu):
        for key, item in menu.items():
            print(f"{key}: {item.desc}")

    def main(self):
        while True:
            print("\nKronos: ")
            self.menu_display(self.main_menu_options)

            user_choice = input("Enter Selection: ")

            menu_item = self.main_menu_options.get(user_choice)

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
