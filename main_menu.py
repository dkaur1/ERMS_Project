import ERMS_Project.department as department
from ERMS_Project.employee import load_employees
import ERMS_Project.payroll as payroll
import ERMS_Project.project as project
import ERMS_Project.reports as reports
import auth_user as auth_user

def main():
    user = auth_user.login()

    if not user:
        return

    if user.role not in {"admin","manager"}:  # using set{} instead of tuple() because it is slightly faster for look up
        print("ERMS - Access Denied")
        return

    print(f"Welcome {user.username}! Logged in as {user.role}")

    main_menu(user)

# Helper Function to check if emp_id exists in employees
def employee_exists(emp_id, employees):
    return any(e.employee_id == emp_id for e in employees)


######################################################################
#                   MAIN MENU
######################################################################

def main_menu(user):
    while True:
        print("\n--- Enterprise Resource Management System ---")
        print("1. Employee Management")
        print("2. Department Management")
        print("3. Project Assignment")
        print("4. Payroll Processing")
        print("5. Generate Reports")
        print("6. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                    employee_menu()
            elif choice == "2":
                department_menu()
            elif choice == "3":
                project_menu()
            elif choice == "4":
                payroll.process_payroll()
            elif choice == "5":
                reports_menu()
            elif choice == "6":
                print("Exiting system. Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")
        except Exception as e:
            print(f"Error: {e}")

######################################################################
#           EMPLOYEE MANAGEMENT MENU
######################################################################
def employee_menu():
    while True:
        print("\n--- Employee Management ---")
        print("1. Add Employee")
        print("2. Update Salary")
        print("3. Delete Employee")
        print("4. List Employees")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        try:
            # Add Employee
            if choice == "1":
                emp_id = input("Employee ID: ")

                # check if emp_id already exists (although this check has been added inside add_employee() function, it's a good practice to check as soon user enter the employee ID, because otherwise it takes all the inputs and then raise the Error)
                from employee import load_employees, DuplicateEmployeeIdError
                employees = load_employees()
                if employee_exists(emp_id, employees):
                    raise DuplicateEmployeeIdError("Employee ID already exists")

                name = input("Name: ")
                dept = input("Department: ")
                salary = float(input("Salary: "))
                joining_date = input("Joining Date (YYYY-MM-DD): ")
                from employee import Employee, add_employee
                add_employee(Employee(emp_id, name, dept, salary, joining_date))
                print("Employee added successfully!")

            # Update Salary
            elif choice == "2":
                emp_id = input("Employee ID: ")
                new_salary = float(input("New Salary: "))
                from employee import update_salary
                update_salary(emp_id, new_salary)
                print("Salary updated successfully!")

            # Delete Employee
            elif choice == "3":
                emp_id = input("Employee ID: ")
                from employee import delete_employee
                delete_employee(emp_id)
                print("Employee deleted successfully!")

            # List Employees
            elif choice == "4":
                from employee import list_employees
                list_employees()

            elif choice == "5":
                break
            else:
                print("Invalid choice. Try again.")
        except Exception as e:
            print(f"Error: {e}")

######################################################################
#           DEPARTMENT MANAGEMENT MENU
######################################################################

def department_menu():
    while True:
        print("\n------Department Management--------")
        print("1. Create Department")
        print("2. Add Employee to Department")
        print("3. View Department Details")
        print("4. List All Departments")
        print("5. Remove Employee from Department")
        print("6. Department Total Salary Expense")
        print("7. Back to Main Menu")

        choice  = input("Enter your choice:")

        try:
            # Create Department
            if choice == "1":
                department.create_department()

            # Add Employee to Dept
            elif choice == "2":
                department.add_employee_to_department()

            # View Department Details
            elif choice == "3":
                department.view_department()

            # List All Departments
            elif choice == "4":
                department.list_departments()

            # Remove Employee from Department
            elif choice == "5":
                emp_id = input("Enter Employee ID: ")
                #Validate emp_id
                employees = load_employees()
                if not employee_exists(emp_id, employees):
                    print(f"Employee ID {emp_id} does not exist")
                    return
                department.remove_employee_from_departments(emp_id)

            # Department Total Salary Expense
            elif choice == "6":
                dept_id = input("Enter Department ID: ")
                # Load departments
                departments = department.load_departments()
                for d in departments:
                    if d.dept_id == dept_id:
                        print(f"Total Salary Expense for {dept_id}:",d.total_salary_expense())
                        return
                print(f"Department ID {dept_id} not found")

            elif choice == "7":
                break
            else:
                print("Invalid choice. Try again.")

        except Exception as e:
            print(f"Error: {e}")
######################################################################
#           PROJECT ASSIGNMENT MENU
######################################################################

def project_menu():

    while True:
        print("\n--- Project Assignment ---")
        print("1. Create Project")
        print("2. Assign Employee to a Project")
        print("3. Remove Employee from a Project")
        print("4. List Employees (in a Project)")
        print("5. Back to Main Menu")

        choice = input("Enter your choice:")

        try:
            # Create Project
            if choice == "1":
                project_id = input("Project ID: ")
                project_name = input("Project Name: ")
                project.create_project(project_id, project_name)

            # Assign Employee to a Project
            elif choice == "2":
                project_id = input("Project ID: ")
                emp_id = input("Employee ID: ")
                project.assign_employee_to_project(project_id, emp_id)

            # Remove Employee from a Project
            elif choice == "3":
                project_id = input("Project ID: ")
                emp_id = input("Employee ID: ")
                project.remove_employee_from_project(project_id, emp_id)

            #List Employees
            elif choice == "4":
                project_id = input("Project ID: ")
                # Create Project object
                proj = project.get_project(project_id)
                proj.list_project_members()

            elif choice == "5":
                break
            else:
                print("Invalid choice. Try again.")

        except Exception as e:
            print(f"Error: {e}")


################################################################
#           REPORTS SUB MENU
################################################################

def reports_menu():
    while True:
        print("\n-------- Reporting System --------")
        print("1. Total Employees")
        print("2. Highest Paid Employee")
        print("3. Department-wise salary expense")
        print("4. Active projects")
        print("5. Monthly payroll summary")
        print("6. Back to Main Menu")

        choice = input("Enter your choice:")

        try:
            # Total Employees
            if choice == "1":
                print("Total Employees: ", reports.total_employees())

            # Highest Paid Employee
            elif choice == "2":
                print("Highest Paid Employee(s):")
                emps = reports.highest_paid_employee()
                for emp in emps:
                    print(f"{emp.name}({emp.employee_id}) with salary {emp.salary}")

            # Department-wise Salary expense
            elif choice == "3":
                for dept_id, dept_name, total_salary in reports.dept_salary_expense():
                    print(f"{dept_name}({dept_id}) - {total_salary}")

            # Active Projects
            elif choice == "4":
                active_projects = reports.get_active_projects()

                if not active_projects:
                    raise ValueError("There are no active projects")

                print("----Active Projects----")
                for project_id, project_name in active_projects:
                    print(f"{project_name} ({project_id})")

            # Monthly payroll summary
            elif choice == "5":
                print(f"Total Employees: {reports.total_employees()}")
                print(f"Total Payroll Expense: {reports.monthly_payroll_summary()}")

            elif choice == "6":
                break
            else:
                print("Invalid choice. Try again.")

        except Exception as e:
            print(f"Error: {e}")

################################################################

# run main() method only if current file is run directly. Every Python file has a built-in special variable __name__, its value depends on how the file is being run
# if file is run directly, __name__ = __main__, if another file imports main_menu file, then inside main_menu.py, __name__="main_menu" and if "main_menu" == "__main__": and condition becomes false
# always keep it at the botton of file
if __name__ == "__main__":
    main()
