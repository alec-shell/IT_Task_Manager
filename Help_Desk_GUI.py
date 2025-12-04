"""
Help_Desk_GUI.py: Main GUI program for Help Desk Tracking System.
Alec Shellberg
11/29/2025
"""

import tkinter as tk
from tkinter import ttk, StringVar
from tkinter.scrolledtext import ScrolledText

from IT_Task_Manager.Assignment import Assignment
from IT_Task_Manager.Database_Tier import create_connection, init_tables, reset_tables, \
    query_employees, retrieve_employee_names, query_tasks, query_assignments, add_task, add_assignment, \
    update_assignment_status
from IT_Task_Manager.Task import Task


class HelpDeskGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.conn = create_connection()
        reset_tables(self.conn)
        init_tables(self.conn)
        self.__notebook = ttk.Notebook(self)
        self.task_column_names = ["TASK_ID", "CUSTOMER", "DESCRIPTION", "PRICE", "EST._HOURS"]
        self.employee_column_names = ["EMPLOYEE_ID", "FIRST_NAME", "LAST_NAME", "PHONE #", "EMAIL"]
        self.assignment_column_names = ["ASSIGNMENT_ID", "EMPLOYEE_ID", "TASK_ID", "COMPLETED"]
        self.__notebook.add(self.build_tasks_tab(), text="Tasks")
        self.__notebook.add(self.build_employees_tab(), text="Employees")
        self.__notebook.add(self.build_assignments_tab(), text="Assignments")
        self.__notebook.pack(expand=True, fill="both")
        self.title("Help Desk Tracking System")
        self.geometry("1000x500")
        self.mainloop()


    def build_tasks_tab(self):
        """
        :return: ttk.Frame
        """
        tasks_tab = ttk.Frame(self.__notebook)
        display_container = ttk.Frame(tasks_tab)
        self.build_task_sort_controls(display_container)
        self.build_task_submission_form(tasks_tab)
        self.task_table = ScrolledText(display_container, font=("Courier New", 10), border=5, relief="solid", height=20)
        self.build_table(self.task_table, self.task_column_names, query_tasks(self.conn))
        display_container.pack()
        self.task_table.pack(expand=True)
        return tasks_tab


    def build_task_sort_controls(self, parent):
        """
        Build controls ttk.Frame for Tasks tab
        :param parent: ttk.Frame
        :return: None
        """
        # radio btn for task completeness
        controls_container = ttk.Frame(parent, border=5, relief="sunken")
        radio_container = ttk.Frame(controls_container)
        radio_lbl = tk.Label(radio_container, text="Completion status:")
        radio_lbl.pack()
        completed_var = tk.StringVar()
        complete = ttk.Radiobutton(radio_container, text="Complete", variable=completed_var, value="yes")
        complete.pack(side=tk.LEFT)
        incomplete = ttk.Radiobutton(radio_container, text="Incomplete", variable=completed_var, value="no")
        incomplete.pack(side=tk.LEFT)
        no_selection = ttk.Radiobutton(radio_container, text="All", variable=completed_var, value="", takefocus=True)
        no_selection.pack(side=tk.LEFT)
        radio_container.pack(pady=10)
        # create employee selection
        employees = retrieve_employee_names(self.conn)
        selected_employee = tk.StringVar()
        selected_employee.set(employees[0])
        employee_selector = ttk.Combobox(controls_container, textvariable=selected_employee, values=employees)
        employees_lbl = tk.Label(controls_container, text="Employee: ")
        employees_lbl.pack(side=tk.LEFT)
        employee_selector.pack(side=tk.LEFT, padx=10)
        # submit
        submit_btn = tk.Button(controls_container,
                               text="Submit",
                               command=lambda:self.build_table(self.task_table, self.task_column_names, query_tasks(
                                   self.conn, completed_var.get(), employees.index(selected_employee.get()))))
        submit_btn.pack()
        controls_container.pack(pady=10)


    def build_task_submission_form(self, parent):
        """
        :param parent: ttk.Frame
        :return: None
        """
        container = ttk.Frame(parent, border=5, relief="sunken")
        form_label = tk.Label(container, text="Create new task:")
        form_label.pack(side=tk.TOP)
        customer_name = self.build_text_input_field(container, "Customer name: ")
        job_desc = self.build_text_input_field(container, "Job description: ")
        price = self.build_text_input_field(container, "Job price: ")
        hours = self.build_text_input_field(container, "Est. hours: ")
        submit = tk.Button(container, text="Submit", command=lambda:self.validate_task_entry(customer_name.get(),
                                                                                                  job_desc.get(),
                                                                                                  price.get(),
                                                                                                  hours.get()))
        submit.pack()
        container.pack(side=tk.LEFT, padx=50)


    def validate_task_entry(self, name, desc, price, hours):
        """
        Validate and execute task entry
        :param name: String
        :param desc: String
        :param price: String
        :param hours: String
        :return: None
        """
        if len(name) > 0 and len(desc) > 0 and len(price) > 0 and len(hours) > 0:
            try:
                if float(price) >= 0 and float(hours) >= 0:
                    new_task = Task(None, name, desc, float(price), float(hours))
                    resp = add_task(self.conn, new_task)
                    self.build_table(self.task_table, self.task_column_names, query_tasks(self.conn))
                    self.reusable_popup(resp)
                else:
                    self.reusable_popup("Price and hours must be >= 0")
            except Exception as e:
                self.reusable_popup(e)
        else:
            self.reusable_popup("One or more fields incomplete.")


    def build_employees_tab(self):
        """
        :return: ttk.Frame
        """
        emp_tab = ttk.Frame(self.__notebook)
        self.employees_table = ScrolledText(emp_tab, font=("Courier New", 10), border=5, relief="solid", height=20)
        self.build_table(self.employees_table, self.employee_column_names, query_employees(self.conn))
        self.employees_table.pack(expand=True)
        return emp_tab


    def build_assignments_tab(self):
        """
        :return: ttk.Frame
        """
        assignments_tab = ttk.Frame(self.__notebook)
        forms_container = ttk.Frame(assignments_tab)
        table_container = ttk.Frame(assignments_tab)
        self.build_assignment_status_update_form(forms_container)
        self.build_assignment_submission_form(forms_container)
        self.assignments_table = ScrolledText(table_container, font=("Courier New", 10), border=5, relief="solid", height=20)
        self.build_assignments_sort_controls(table_container)
        self.build_table(self.assignments_table, self.assignment_column_names, query_assignments(self.conn, ""))
        forms_container.pack(side=tk.LEFT)
        self.assignments_table.pack(expand=True)
        table_container.pack()
        return assignments_tab


    def build_assignments_sort_controls(self, parent):
        """
        :param parent: ttk.Frame
        :return: None
        """
        container = ttk.Frame(parent, border=5, relief="sunken")
        completion_status = StringVar()
        label = tk.Label(container, text="Completion status: ")
        complete = ttk.Radiobutton(container, variable=completion_status, value="yes", text="Complete")
        incomplete = ttk.Radiobutton(container, variable=completion_status, value="no", text="Incomplete")
        show_all = ttk.Radiobutton(container, variable=completion_status, value="", text="All", takefocus=True)
        submit = tk.Button(container, text="Submit", command=lambda:self.build_table(self.assignments_table,
                                                                                self.assignment_column_names,
                                                                                query_assignments(self.conn,
                                                                                                  completion_status.get())))
        label.pack(side=tk.TOP)
        complete.pack(side=tk.LEFT)
        incomplete.pack(side=tk.LEFT)
        show_all.pack(side=tk.LEFT)
        submit.pack()
        container.pack(pady=10)


    def build_assignment_status_update_form(self, parent):
        """
        :param parent: ttk.Frame
        :return: None
        """
        container = ttk.Frame(parent, border=5, relief="sunken")
        label = tk.Label(container, text="Update completion status:")
        label.pack()
        assignment_id = self.build_text_input_field(container, "Assignment ID: ")
        completed_values = ["no", "yes"]
        completed_selector_label = tk.Label(container, text="Completed: ")
        completed_value = StringVar()
        completed_value.set(completed_values[0])
        completed_status_selector = ttk.Combobox(container, textvariable=completed_value, values=completed_values)
        completed_selector_label.pack()
        completed_status_selector.pack(pady=10)
        submit = tk.Button(container, text="Submit", command=lambda:self.validate_completion_status_update(assignment_id.get(),
                                                                                                           completed_value.get()))
        submit.pack()
        container.pack(pady=10)


    def validate_completion_status_update(self, assignment_id, new_status):
        if len(assignment_id) > 0:
            try:
                resp = update_assignment_status(self.conn, new_status, int(assignment_id))
                self.build_table(self.assignments_table, self.assignment_column_names, query_assignments(self.conn, ""))
                self.reusable_popup(resp)
            except Exception as e:
                self.reusable_popup(e)
        else:
            self.reusable_popup("One or more invalid entries.")


    def build_assignment_submission_form(self, parent):
        """
        :param parent: ttk.Frame
        :return: None
        """
        container = ttk.Frame(parent, border=5, relief="sunken")
        label = tk.Label(container, text="Create new assignment:")
        label.pack()
        employee_id = self.build_text_input_field(container, "Employee ID: ")
        task_id = self.build_text_input_field(container, "Task ID: ")
        completed_values = ["no", "yes"]
        completed_selector_label = tk.Label(container, text="Completed: ")
        completed_value = StringVar()
        completed_value.set(completed_values[0])
        completed_status_selector = ttk.Combobox(container, textvariable=completed_value, values=completed_values)
        completed_selector_label.pack()
        completed_status_selector.pack(pady=10)
        submit = tk.Button(container, text="Submit", command=lambda:self.validate_assignment_submission(employee_id.get(),
                                                                                                        task_id.get(),
                                                                                                        completed_value.get()))
        submit.pack(pady=10)
        container.pack(side=tk.LEFT, padx=50)


    def validate_assignment_submission(self, emp_id, task_id, completed_val):
        """
        Validate and execute assignment submission
        :param emp_id: String
        :param task_id: String
        :param completed_val: String
        :return: None
        """
        if len(emp_id) > 0 and len(task_id) > 0 and len(completed_val) > 0:
            try:
                new_assignment = Assignment(None, int(emp_id), int(task_id), completed_val)
                resp = add_assignment(self.conn, new_assignment)
                self.build_table(self.assignments_table, self.assignment_column_names, query_assignments(self.conn, ""))
                self.reusable_popup(resp)
            except Exception as e:
                self.reusable_popup(e)
        else:
            self.reusable_popup("One or more invalid entries.")


    def build_table(self, table, columns, data):
        """
        Build display tables for all tabs.
        :param table: tk.Text
        :param columns: list[str]
        :param data: list[Object]
        :return: tk.Text
        """
        table.config(state=tk.NORMAL)
        table.delete("1.0", tk.END)
        table_text = ""
        for column in columns:
            table_text += column.center(15, " ")
        table_text += "\n"
        for row in data:
            table_text += str(row) +"\n"
        table.insert(tk.END, table_text)
        table.config(state=tk.DISABLED)


    def build_text_input_field(self, parent, label_text):
        """
        Reusable text field building function.
        :param parent: ttk.Frame
        :param label_text: String
        :return: tk.Entry
        """
        container = ttk.Frame(parent)
        label = tk.Label(container, text=label_text, width=15)
        label.pack(side=tk.LEFT)
        field = tk.Entry(container, width=20)
        field.pack()
        container.pack(pady=10)
        return field


    def reusable_popup(self, message):
        """
        Reusable popup box function.
        :param message: String
        :return: None
        """
        popup = tk.Toplevel()
        popup.wm_title("Message: ")
        message = tk.Label(popup, text=message)
        button = tk.Button(popup, text="Close", command=popup.destroy)
        message.pack(padx=10, pady=10)
        button.pack(padx=10, pady=50)


HelpDeskGUI()
