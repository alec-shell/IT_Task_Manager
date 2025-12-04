"""
config.py: Default Employee, Task, and Assignment objects.
Alec Shellberg
11/29/2025
"""
from IT_Task_Manager.Assignment import Assignment
from IT_Task_Manager.Employee import Employee
from IT_Task_Manager.Task import Task

# default employees
John = Employee(1, "John", "Johnson", "555-555-2345", "john_j@helpdesk.com")
Jenny = Employee(2, "Jenny", "Jenson", "555-444-1234", "jenny_j@helpdesk.com")
Bob = Employee(3, "Bob", "Benson", "555-222-2323", "bob_b@helpdesk.com")
Alice = Employee(4, "Alice", "Allen", "555-111-4567", "alice_a@helpdesk.com")
Carl = Employee(5, "Carl", "Clark", "555-222-5678", "carl_c@helpdesk.com")
default_employee_list = [John, Jenny, Bob, Alice, Carl]

# default tasks
task1 = Task(1, "Charlie Cook", "Fix WiFi", 99.99, 1.5)
task2 = Task(2, "Harriet Holmes", "Setup computer", 59.99, 1)
task3 = Task(3, "Jackie Jumper", "Recover login", 74.99, 1.2)
task4 = Task(4, "Logan Locke", "Repair mouse", 49.99, .5)
task5 = Task(5, "Allen Apple", "Replace hardrive", 59.99, 0.8)
task6 = Task(6, "Megan Marsh", "Install printer", 39.99, 0.7)
task7 = Task(7, "Dylan Drake", "Clean malware", 89.99, 1.3)
task8 = Task(8, "Sophie Sparks", "Upgrade RAM", 69.99, 0.9)
task9 = Task(9, "Reese Rivers", "Optimize system", 54.99, 1.0)
task10 = Task(10, "Carter Cole", "Configure email", 44.99, 0.6)
default_task_list = [task1, task2, task3, task4, task5, task6, task7, task8, task9, task10]

# default assignments
assignment1 = Assignment(10, 3, 5, "yes")
assignment2 = Assignment(1, 5, 10, "no")
assignment3 = Assignment(2, 1, 1, "yes")
assignment4 = Assignment(3, 2, 2, "yes")
assignment5 = Assignment(4, 4, 3, "no")
assignment6 = Assignment(5, 5, 4, "no")
assignment7 = Assignment(6, 1, 6, "no")
assignment8 = Assignment(7, 3, 7, "yes")
assignment9 = Assignment(8, 2, 8, "no")
assignment10 = Assignment(9, 4, 9, "yes")
default_assignments_list = [assignment1, assignment2, assignment3, assignment4, assignment5,
                            assignment6, assignment7, assignment8, assignment9, assignment10]
