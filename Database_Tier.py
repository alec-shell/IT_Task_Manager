"""
Database_Tier.py: Basic CRUD functionality for help desk database.
Alec Shellberg
11/29/2025
"""

import sqlite3
from contextlib import closing

from IT_Task_Manager.Assignment import Assignment
from IT_Task_Manager.Employee import Employee
from IT_Task_Manager.Task import Task
from IT_Task_Manager.config import default_employee_list, default_task_list, default_assignments_list


def create_connection():
    """
    Create connection to database.
    :return: Connection or None
    """
    try:
        conn = sqlite3.connect("Help_Desk.db")
        return conn
    except Exception as e:
        print("create_connection(): ",e)
        return None


def init_tables(conn):
    """
    Initialize employee, task, and assignment tables in Help_Desk.db.
    :param conn: Connection
    :return: String
    """
    emp_table_cmd = ("CREATE TABLE IF NOT EXISTS "
                     "Employee(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "first_name VARCHAR(30) NOT NULL,"
                     "last_name VARCHAR(40) NOT NULL,"
                     "phone_number VARCHAR(20) NOT NULL,"
                     "email_address VARCHAR(100) NOT NULL)")
    task_table_cmd = ("CREATE TABLE IF NOT EXISTS "
                      "Task(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                      "customer_name VARCHAR(60) NOT NULL,"
                      "job_description VARCHAR(100) NOT NULL,"
                      "price REAL NOT NULL,"
                      "estimated_hours REAL NOT NULL)")
    assignment_table_cmd = ("CREATE TABLE IF NOT EXISTS "
                            "Assignment(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                            "employee_id INTEGER NOT NULL,"
                            "task_id INTEGER NOT NULL,"
                            "completed VARCHAR(5) NOT NULL,"
                            "FOREIGN KEY(employee_id) REFERENCES Employee(id),"
                            "FOREIGN KEY(task_id) REFERENCES Task(id))")
    try:
        with closing(conn.cursor()) as cursor:
            cursor.execute(emp_table_cmd)
            cursor.execute(task_table_cmd)
            cursor.execute(assignment_table_cmd)
            populate_default_entries(conn)
        return "Tables successfully created."
    except Exception as e:
        print("init_tables(): ", e)
        return e


def add_employee(conn, employee):
    """
    :param conn: Connection
    :param employee: Employee
    :return: String
    """
    cmd = "INSERT INTO Employee(first_name, last_name, phone_number, email_address) VALUES (?, ?, ?, ?)"
    try:
        with closing(conn.cursor()) as cursor:
            cursor.execute(cmd, (employee.get_first_name(),
                           employee.get_last_name(),
                           employee.get_phone(),
                           employee.get_email()))
            conn.commit()
        return "Successfully added employee."
    except Exception as e:
        print("add_employee(): ", e)
        return e


def add_task(conn, task):
    """
    :param conn: Connection
    :param task: Task
    :return: String
    """
    cmd = "INSERT INTO Task(customer_name, job_description, price, estimated_hours) VALUES (?, ?, ?, ?)"
    try:
        with closing(conn.cursor()) as cursor:
            cursor.execute(cmd, (task.get_customer_name(),
                           task.get_description(),
                           task.get_price(),
                           task.get_hours()))
            conn.commit()
        return "Successfully added task."
    except Exception as e:
        print("add_task(): ", e)
        return e


def add_assignment(conn, assignment):
    """
    :param conn: Connection
    :param assignment: Assignment
    :return: String
    """
    cmd = "INSERT INTO Assignment(employee_id, task_id, completed) VALUES (?, ?, ?)"
    try:
        with closing(conn.cursor()) as cursor:
            cursor.execute(cmd, (assignment.get_employee_id(),
                           assignment.get_task_id(),
                           assignment.get_completed()))
            conn.commit()
        return "Successfully added assignment."
    except Exception as e:
        print("add_assignment(): ", e)
        return e



def reset_tables(conn):
    """
    Drop Employee, Task, and Assignments tables.
    :param conn: Connection
    :return: String
    """
    del_emp = "DROP TABLE IF EXISTS Employee"
    del_task = "DROP TABLE IF EXISTS Task"
    del_assignment = "DROP TABLE IF EXISTS Assignment"
    try:
        with closing(conn.cursor()) as cursor:
            cursor.execute(del_emp)
            cursor.execute(del_task)
            cursor.execute(del_assignment)
        return "Tables successfully dropped."
    except Exception as e:
        print("reset_tables(): ", e)
        return e


def populate_default_entries(conn):
    """
    Fill database tables with default employees, tasks and assignments from config.py
    :param conn: Connection
    :return: None
    """
    for employee in default_employee_list:
        add_employee(conn, employee)
    for task in default_task_list:
        add_task(conn, task)
    for assignment in default_assignments_list:
        add_assignment(conn, assignment)


def query_employees(conn):
    cmd = "SELECT * FROM Employee WHERE 1=1"
    employees = []
    try:
        with closing(conn.cursor()) as cursor:
            cursor.execute(cmd)
            rows = cursor.fetchall()
            for row in rows:
                employees.append(Employee(row[0], row[1], row[2], row[3], row[4]))
    except Exception as e:
        print(e)
    return employees


def retrieve_employee_names(conn):
    employee_names = ["Any"]
    cmd = "SELECT first_name, last_name FROM Employee"
    try:
        with closing(conn.cursor()) as cursor:
            cursor.execute(cmd)
            names = cursor.fetchall()
            for row in names:
                employee_names.append(row[0] + " " + row[1])
    except Exception as e:
        print("retrieve_employee_names(): ", e)
    return employee_names


def query_tasks(conn, is_complete="", employee_id=0):
    """
    Retrieve tasks:
    - all
    - complete/incomplete
    - specified employee_id
    :param conn: Connection
    :param is_complete: String
    :param employee_id: int
    :return: List[Task]
    """
    tasks = []
    cmd, params = prepare_task_cmd(is_complete, employee_id)
    try:
        with closing(conn.cursor()) as cursor:
            if params:
                cursor.execute(cmd, params)
            else:
                cursor.execute(cmd)
            rows = cursor.fetchall()
            for row in rows:
                tasks.append(Task(row[0], row[1], row[2], row[3], row[4]))
    except Exception as e:
        print("query_tasks(): ", e)
    return tasks


def prepare_task_cmd(is_complete, employee_id):
    """
    Structure Task table sql query based on user input.
    :param is_complete: String
    :param employee_id: int
    :return: List[Task]
    """
    if employee_id != 0 or is_complete:
        cmd = """
        SELECT Task.id, Task.customer_name, Task.job_description, Task.price, Task.estimated_hours
        From Task
        JOIN Assignment ON Assignment.task_id = Task.id
        WHERE 1=1
        """
    else:
        cmd = "SELECT * FROM Task"
    params = []
    if employee_id != 0:
        cmd += " AND Assignment.employee_id = ?"
        params.append(employee_id)
    if is_complete:
        cmd += " AND Assignment.completed LIKE ?"
        params.append(is_complete)
    return cmd, tuple(params)


def query_assignments(conn, is_completed):
    assignments = []
    cmd = "SELECT * FROM Assignment WHERE 1=1"
    if is_completed:
        cmd += " AND completed = ?"
    try:
        with closing(conn.cursor()) as cursor:
            if is_completed:
                cursor.execute(cmd, (is_completed,))
            else:
                cursor.execute(cmd)
            rows = cursor.fetchall()
            for row in rows:
                assignments.append(Assignment(row[0], row[1], row[2], row[3]))
    except Exception as e:
        print("query_assignments(): ", e)
    return assignments


def update_assignment_status(conn, new_status, assignment_id):
    cmd = """
    UPDATE Assignment
    SET completed = ?
    WHERE id = ?
    """
    try:
        with closing(conn.cursor()) as cursor:
            cursor.execute(cmd, (new_status, assignment_id))
            conn.commit()
        return "Completed status update successfully."
    except Exception as e:
        print("update_assignment_status(): ", e)
        return "Error: ", e
