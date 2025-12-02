"""
Task.py: Class structure for Task objects.
Alec Shellberg
11/29/2025
"""

class Task:
    def __init__(self, task_id, customer_name, job_desc, price, hours):
        self.__task_id = task_id
        self.__customer_name = customer_name
        self.__job_desc = job_desc
        self.__price = price
        self.__hours = hours


    def __str__(self):
        return (str(self.__task_id).center(15, " ")
                + str(self.__customer_name).center(15, " ")
                + str(self.__job_desc).center(15, " ")
                + str(self.__price).center(15, " ")
                + str(self.__hours).center(15, " ")
                )

    # getters
    def get_id(self):
        return self.__task_id


    def get_customer_name(self):
        return self.__customer_name


    def get_description(self):
        return self.__job_desc


    def get_price(self):
        return self.__price


    def get_hours(self):
        return self.__hours

    # setters
    def set_id(self, new_id):
        if type(new_id) == int:
            self.__task_id = new_id


    def set_customer_name(self, new_name):
        self.__customer_name = new_name


    def set_job_description(self, new_descr):
        self.__job_desc = new_descr


    def set_price(self, new_price):
        if type(new_price) == float:
            self.__price = new_price


    def set_hours(self, new_hours):
        if type(new_hours) == float:
            self.__hours = new_hours
