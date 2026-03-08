import csv
import os
from datetime import datetime

from department import get_department, update_department, remove_employee_from_departments

EMPLOYEES_FILE = "data/employees.csv"
FIELDNAMES = ["employee_id", "name", "department", "salary", "joining_date"]


#-----------------------
#  Custom Exceptions
#-----------------------
class InvalidSalaryError(Exception): pass
class DuplicateEmployeeIdError(Exception): pass
class EmployeeNotFoundError(Exception): pass

#----------------------------------
#  Employee Class
# department = department.dept_id
#----------------------------------

class Employee:

    def __init__(self, employee_id: str, name: str, department: str, salary: float, joining_date: str):
        self.employee_id = str(employee_id).strip()
        self.name = name.strip()
        self.department = department.strip()
        self.salary = float(salary)         #float() conversion handles invalid salary value, it raises ValueError if a non-numeric value is passed

        # Validate date format
        try:
            datetime.strptime(joining_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Joining date must be in YYYY-MM-DD format")
        self.joining_date = joining_date

    def display_details(self):
        # ,.2f - comma separator and shows 2 digits after decimal. 60000 -> 60,000.00
        print(f"ID: {self.employee_id} | Name: {self.name} | Dept: {self.department} | Salary: ${self.salary:,.2f} | Annual Sal: ${self.salary*12:,.2f}| Joining: {self.joining_date}")

    def to_dict(self):
        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "department": self.department,
            "salary": self.salary,
            "joining_date": self.joining_date
        }

#---------------------------------------------------------------------
# CSV Helper Functions
# (File Handling - load employees data and Save employees data to csv)
#---------------------------------------------------------------------

def load_employees():
    #create list to store Employee objects
    employees = []

    # if file doesn't exist, return empty list to prevent system from crashing
    if not os.path.exists(EMPLOYEES_FILE):
        return employees
    try:
        with open(EMPLOYEES_FILE, "r", newline="") as empFile:    # here,newline="" disables Python's newline handling, because csv module handles newlines itself
            reader = csv.DictReader(empFile)
            for row in reader:
                #append Employee object
                employees.append(Employee(row["employee_id"], row["name"], row["department"], float(row["salary"]), row["joining_date"] ))
    except Exception as e:
        print("Error: Error while reading employees file", {e})
    return employees

def save_employees(employees: list):
    #create data folder (if it doesn't exist), to save the csv file
    os.makedirs("data", exist_ok=True)      # exist_ok=True, it prevents raising Error if dir already exists

    #create/open csv file in write mode
    with open(EMPLOYEES_FILE, "w", newline="") as empFile:
        #1. create a DictWriter Object (it is used when we need header in the file, otherwise csv.writer())
        writer = csv.DictWriter(empFile, fieldnames=FIELDNAMES)

        #2. write header row
        writer.writeheader()

        #3. Write the data rows
        for emp in employees:
            # writer.writerow([emp["employee_id"],emp["name"]])
            writer.writerow(emp.to_dict())

#-------------------------------------------------------------
# CRUD Functions
#-------------------------------------------------------------
# add employee to employees.csv and then to departments.csv
def add_employee(employee: Employee):

    # load employees.csv file to employees list
    employees = load_employees()

    # check if the given employeeId already exists
    if any(emp.employee_id == employee.employee_id for emp in employees):
        raise DuplicateEmployeeIdError(f"Employee ID {employee.employee_id} already exists.")

    # Validate department exists
    dept = get_department(employee.department)      #it throws DepartmentNotFoundError if dept does not exist

    # add employee record to the existing list and Save the employees list back to the csv file
    employees.append(employee)
    save_employees(employees)

    # Add employee ID to department employee list
    dept.add_employee(employee.employee_id)

    # Save updated department
    update_department(dept)

def update_salary(emp_id: str, new_salary: float):
    # load employees.csv file to employees list
    employees = load_employees()
    for emp in employees:
        if emp.employee_id == emp_id:
            if new_salary < 0:
                raise InvalidSalaryError("Salary cannot be negative")
            emp.salary = new_salary
            save_employees(employees)
            return
    raise EmployeeNotFoundError(f"Employee not found with ID {emp_id}")

def calculate_annual_salary(emp_id: str):
    # load employees.csv file to employees list
    employees = load_employees()
    for emp in employees:
        if emp.employee_id == emp_id:
           return emp.salary * 12
    raise EmployeeNotFoundError(f"Employee not found with ID {emp_id}")

# 1. Remove employee from employees.csv
# 2. Remove employee ID from department.employee_list (update department)
def delete_employee(emp_id: str):
    # load employees.csv file to employees list
    employees = load_employees()

    # add all the non-matching employees to a new updated list
    updatedEmpList = [emp for emp in employees if emp.employee_id != emp_id]

    if len(updatedEmpList) == len(employees):
        raise EmployeeNotFoundError(f"Employee not found with ID {emp_id}")

    # save updated list to the csv file
    save_employees(updatedEmpList)

    #update all departments - remove emp_id from employee_list of all the departments
    remove_employee_from_departments(emp_id)


def list_employees():
    # load employees.csv file to employees list
    employees = load_employees()
    if not employees:
        print("No employees found")
        return
    for emp in employees:
        emp.display_details()
