# Smart Time Allocator Module for Project Kronos
"""
This module analyzes tasks and creates optimized study schedules
Author: Raphael

"""
import datahandler
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

# datetime,timedelta - used to work with dates and calculate the remaining days
#typing - used to make our code clear about what data types to expect

class TimeAllocator():
    def __init__(self):
        self.database_handler = datahandler.DatabaseConnector() # Used for referencing the methods in the datahandler's DatabaseConnector class
        self.tasks = self.database_handler.fetch_tasks_by_status('Pending') + self.database_handler.fetch_tasks_by_status('In Progress') # Storing "Pending" and "In Progress Assignments"

    """
    Calculate the priority score for an assignment
    The higher the score, the more urgent the task
    """

    def calculate_priority(self, estimated_hours: float, deadline) -> float:
    # The function is made to ensure that the return value is a number by adding the parameters and also the "-> float" meaning this function returns as a float
        
        #Getting today's date
        today = datetime.now().date()
        #Converting the deadline string to a date object
        deadline_date = deadline
        #Calculate days remaining
        days_remaining = (deadline_date - today).days

        if days_remaining <= 0:
            #Assignment is overdue or due today
            return float('10')
        
        #Calculating the priority score
        priority_score = estimated_hours / days_remaining

        return priority_score
    
    """
    Assign the priority to each of the tasks and sort them in accordance with their priority
    Returns a list of tasks.
    """
    def indexing_tasks_with_priorities(self): 
        prioritized_tasks = [] # list for the tasks

        # iterating through tasks
        for task in self.tasks:
            priority = self.calculate_priority(task['estimated_hours'], task['deadline'])

            # Storiing the task id and priority of tasks in one list
            prioritized_tasks.append({
                "task_id" : task["id"],
                "priority" : priority
            })
        
        # Sorting prioritized 
        sorted_tasks = sorted(prioritized_tasks, key=lambda d: d['priority'], reverse=True)
        prioritized_with_index = []

        # Store all the sorted tasks in a list in accordance to their priority.
        for index, item in enumerate(sorted_tasks, start=1):
            prioritized_with_index.append({
                "index": index,
                "task_id" : item['task_id'],
                "priority" : item['priority']
            })

        return prioritized_with_index

    """
    Main Function
    """
    def main(self):
        prioritized_tasks = self.indexing_tasks_with_priorities()

        # Output: [prioritized_task["index"]]. task[prioritized_task]
        for prioritized_task in prioritized_tasks:
                item = self.database_handler.fetch_task_by_id(prioritized_task['task_id'])
                print(f'{prioritized_task['index']}. {item['title']} (Due: {item['deadline']}) | Priority: {prioritized_task['priority']}')
                
# TEST CODE - We'll remove this later
test = TimeAllocator()
test.main()
# if __name__ == "__main__":
#     print("=" * 50)
#     print("TESTING PRIORITY CALCULATOR")
#     print("=" * 50)
   
#     # Test 1: Assignment due in 2 days, needs 10 hours
#     print("\n📝 Test 1: 10 hours, due in 2 days")
#     priority1 = test.calculate_priority(10, '2025-11-15')
#     print(f"   Priority Score: {priority1}")
#     print(f"   Expected: 5.0")
   
#     # Test 2: Assignment due in 10 days, needs 3 hours
#     print("\n📝 Test 2: 3 hours, due in 10 days")
#     priority2 = test.calculate_priority(3, '2025-11-23')
#     print(f"   Priority Score: {priority2}")
#     print(f"   Expected: 0.3")
   
#     # Test 3: Assignment due today
#     print("\n📝 Test 3: 5 hours, due TODAY")
#     priority3 = test.calculate_priority(5, '2025-11-13')
#     print(f"   Priority Score: {priority3}")
#     print(f"   Expected: inf (infinity)")
   
#     # Test 4: Your custom test!
#     print("\n📝 Test 4: 8 hours, due in 4 days")
#     priority4 = test.calculate_priority(8, '2025-11-17')
#     print(f"   Priority Score: {priority4}")
#     print(f"   Expected: 2.0")
   
#     print("\n" + "=" * 50)
#     print("✅ All tests completed!")
#     print("=" * 50)