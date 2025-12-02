"""
Employee.py: Class structure for Employee objects.
Alec Shellberg
11/29/2025
"""

class Employee:
    def __init__(self, employee_id, first_name, last_name, phone, email):
        self.__employee_id = employee_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__phone = phone
        self.__email = email


    def __str__(self):
        return (str(self.__employee_id).center(15, " ")
                + str(self.__first_name).center(15, " ")
                + str(self.__last_name).center(15, " ")
                + str(self.__phone).center(15, " ")
                + str(self.__email).center(15, " "))

    # getters
    def get_id(self):
        return self.__employee_id


    def get_first_name(self):
        return self.__first_name


    def get_last_name(self):
        return self.__last_name


    def get_phone(self):
        return self.__phone


    def get_email(self):
        return self.__email

    # setters
    def set_id(self, new_id):
        if type(new_id) == int:
            self.__employee_id = new_id


    def set_first_name(self, new_name):
        self.__first_name = new_name


    def set_last_name(self, new_name):
        self.__last_name = new_name


    def set_phone(self, new_phone):
        self.__phone = new_phone


    def set_email(self, new_email):
        self.__email = new_email
