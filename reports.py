from department import load_departments
from employee import load_employees
from project import load_projects


def total_employees():

    # Load employees from CSV
    employees = load_employees()
    count_employees = len(employees)
    return count_employees

def highest_paid_employee():

    # Load employees from CSV
    employees = load_employees()

    # Get max salary
    salaries = [e.salary for e in employees]
    max_salary = max(salaries)

    # Get employee with max salary
    max_salary_employees = [e for e in employees if e.salary == max_salary]
    return max_salary_employees

def dept_salary_expense():

    # Load departments
    departments = load_departments()

    # for d in departments:
       # print(f"{d.dept_id} - {d.total_salary_expense()}")
    return [(d.dept_id, d.dept_name, d.total_salary_expense()) for d in departments]

def get_active_projects():

    # Load projects
    projects = load_projects()
    active_projects = []

    for project_id, project in projects.items():
        # Check assigned_employees list is not empty
        if project["assigned_employees"]:
            active_projects.append((project_id, project["project_name"]))  # add tuple with project_id and project_name
    return active_projects

def monthly_payroll_summary():

    # load employees
    employees = load_employees()
    total_salary = sum(e.salary for e in employees)
    return total_salary








