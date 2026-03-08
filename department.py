import csv
import os

DEPARTMENT_FILE = "data/departments.csv"
FIELDNAMES = ["dept_id", "dept_name", "employee_list"]

#-----------------------
#  Custom Exceptions
#-----------------------
class DuplicateDepartmentError(Exception): pass
class DepartmentNotFoundError(Exception): pass
class EmployeeDoesNotExistError(Exception): pass

#-----------------------
#  Department Class
#-----------------------
# Storing employee_list as pipe separated instead of comma in csv file.

class Department:

    def __init__(self, dept_id: str, dept_name: str, employee_list=None):
        if not  str(dept_id).strip():
            raise ValueError("Department ID cannot be empty")

        if not  str(dept_name).strip():
            raise ValueError("Department Name cannot be empty")

        self.dept_id = str(dept_id).strip()
        self.dept_name = dept_name.strip()

        if employee_list is None:
            self.employee_list = []
        elif isinstance(employee_list, list):
            self.employee_list = employee_list
        else:
            raise TypeError("employee_list must be a list of employee IDs")


    def add_employee(self, emp_id: str):
        #1. load employees from employees module
        from employee import load_employees               # Import inside function to avoid circular dependency. if we write this import at the top, it gives error because of circular dependency between employee and department modules
        employees = load_employees()

        #2. Validate employee exists
        if not any(emp.employee_id == emp_id for emp in employees):
            raise EmployeeDoesNotExistError(f"Employee ID {emp_id} does not exist")

        #3. Prevent duplicate emp_id in department
        if emp_id in self.employee_list:
            raise ValueError(f"Employee Id {emp_id} already exists in the department")

        self.employee_list.append(emp_id)

    def remove_employee(self, emp_id: str):
        if emp_id not in self.employee_list:
            raise ValueError(f"Employee with id {emp_id} not found in this department")

        self.employee_list.remove(emp_id)

    def total_salary_expense(self):
        total_salary = 0
        #1. load employees from employees module
        from employee import load_employees
        employees = load_employees()

        for emp in employees:
            if emp.employee_id in self.employee_list:
                total_salary += emp.salary

        return total_salary

    def to_dict(self):
        return {
            "dept_id": self.dept_id,
            "dept_name": self.dept_name,
            # Join only if list is non-empty
            "employee_list": "|".join(self.employee_list) if self.employee_list else ""
        }

    def display_details(self):
        print(
            f"Dept ID: {self.dept_id} | Name: {self.dept_name} | Employees: {len(self.employee_list)} | Total Salary: ${self.total_salary_expense():,.2f}"
        )
#---------------------------------------------------------------------
# Helper Functions
# (File Handling - load and Save department data using csv file)
# For employee_list, we wil save emp_id separated by '|' instead of comma
#---------------------------------------------------------------------
def load_departments():
    #create a list to store Department objects
    departments = []

    # if file doesn't exist, return empty list to prevent system from crashing
    if not os.path.exists(DEPARTMENT_FILE):
        return departments
    try:
        with open(DEPARTMENT_FILE, "r", newline="") as deptFile:    # here,newline="" disables Python's newline handling, because csv module handles newlines itself
            reader = csv.DictReader(deptFile)
            for row in reader:
                # Split only if non-empty
                employee_list = row["employee_list"].split("|") if row["employee_list"].strip() else []
                #append Department object
                departments.append(Department(row["dept_id"], row["dept_name"], employee_list))
    except Exception as e:
        print("Error: Error while reading departments file", {e})
    return departments

def save_departments(departments: list):
    #create data folder (if it doesn't exist), to save the csv file
    os.makedirs("data", exist_ok=True)      # exist_ok=True, it prevents raising Error if dir already exists

    #create/open csv file in write mode
    with open(DEPARTMENT_FILE, "w", newline="") as deptFile:
        #1. create a DictWriter Object (it is used when we need header in the file, otherwise csv.writer())
        writer = csv.DictWriter(deptFile, fieldnames=FIELDNAMES)

        #2. write header row
        writer.writeheader()

        #3. Write the data rows
        for dept in departments:
            writer.writerow(dept.to_dict())

#-------------------------------------------------------------
# CRUD Functions
#-------------------------------------------------------------

def add_department(department: Department):     #Department object

    #1. load departments.csv file to departments list
    departments = load_departments()

    #2. check if the given employeeId already exists
    if any(d.dept_id == department.dept_id for d in departments):
        raise DuplicateDepartmentError(f"Department ID {department.dept_id} already exists.")

    #3. append department record to the existing list
    departments.append(department)

    #4. Save the departments list back to the csv file
    save_departments(departments)

def get_department(dept_id):
    departments = load_departments()

    for dept in departments:
        if dept.dept_id == dept_id:
            return dept

    raise DepartmentNotFoundError("Department not found")

def update_department(updated_department: Department):
    #load departments.csv file to departments list
    departments = load_departments()

    for i, dept in enumerate(departments):
        if dept.dept_id == updated_department.dept_id:
            departments[i] = updated_department
            save_departments(departments)
            return

    raise DepartmentNotFoundError("Department not found")

# to remove emp_id from all departments' employee_list
def remove_employee_from_departments(emp_id: str):
    # load departments.csv file to departments list
    departments = load_departments()

    for dept in departments:
        if emp_id in dept.employee_list:
            dept.remove_employee(emp_id)

    save_departments(departments)
    print(f"Employee ID {emp_id} removed successfully from the departments")

def create_department():
    dept_id = input("Enter Department ID: ")
    dept_name = input("Enter Department Name: ")

    # Load all departments
    departments = load_departments()        # departments -> []

    # Check for duplicate ID
    if any(d.dept_id == dept_id for d in departments):
        print(f"Department {dept_id} already exists")
        return

    # Create new department Object
    new_dept = Department(dept_id, dept_name)

    departments.append(new_dept)

    # Save back to CSV
    save_departments(departments)

    print(f"Department {dept_name} ({dept_id}) created successfully.")

def add_employee_to_department():
    dept_id = input("Enter Department ID: ")
    emp_id = input("Enter Employee ID: ")

    # Load departments
    departments = load_departments()

    # Find the department
    dept = None
    for d in departments:
        if d.dept_id == dept_id:
            dept = d
            break

    if not dept:
        print(f"Department {dept_id} not found.")
        return

    # Prevent duplicate employee
    if emp_id in dept.employee_list:
        print(f"Employee {emp_id} is already in department {dept_id}.")
        return

    # Add employee
    dept.add_employee(emp_id)

    # Save back to CSV
    save_departments(departments)

    print(f"Employee {emp_id} added to department {dept_id} successfully.")

def view_department():
    dept_id = input("Enter Department ID: ")
    dept = get_department(dept_id)
    print("Department:", dept.dept_name)
    print("Employees:", dept.employee_list)

def list_departments():

    departments = load_departments()

    if not departments:
        print("No departments found.")
        return

    print("\n--- Departments ---")
    for dept in departments:
        print(f"{dept.dept_id} - {dept.dept_name}")
