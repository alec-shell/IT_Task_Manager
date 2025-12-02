"""
Assignment.py: Class structure for Assignment objects.
Alec Shellberg
11/29/2025
"""

class Assignment:
    def __init__(self, assignment_id, employee_id, task_id, completed):
        self.__assignment_id = assignment_id
        self.__employee_id = employee_id
        self.__task_id = task_id
        self.__completed = completed


    def __str__(self):
        return (str(self.__assignment_id).center(15, " ")
                + str(self.__employee_id).center(15, " ")
                + str(self.__task_id).center(15, " ")
                + str(self.__completed).center(15, " ")
                )

    # getters
    def get_id(self):
        return self.__assignment_id


    def get_employee_id(self):
        return self.__employee_id


    def get_task_id(self):
        return self.__task_id


    def get_completed(self):
        return self.__completed

    # setters
    def set_id(self, new_id):
        if type(new_id) == int:
            self.__assignment_id = new_id


    def set_employee_id(self, new_id):
        if type(new_id) == int:
            self.__employee_id = new_id


    def set_task_id(self, new_id):
        if type(new_id) == int:
            self.__task_id = new_id


    def set_completed(self, new_value):
        self.__completed = new_value
