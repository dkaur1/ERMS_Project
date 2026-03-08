import json
import os
from json import JSONDecodeError

from employee import load_employees
PROJECT_FILE = "data/projects.json"

class Project:

    def __init__(self, project_id: str, project_name: str, assigned_employees: list[str] | None = None):     #assigned_employees is optional here(| None), default is None value
        self.project_id = project_id
        self.project_name = project_name
        self.assigned_employees = assigned_employees or []

    def assign_employee(self, emp_id):

        employees = load_employees()   #get list of Employee Objects

        if not any(emp.employee_id == emp_id for emp in employees):
            raise ValueError("Employee does not exist")

        if emp_id in self.assigned_employees:
            raise ValueError("Employee already assigned")

        self.assigned_employees.append(emp_id)

    def remove_employee(self, emp_id):

        if emp_id not in self.assigned_employees:
            raise ValueError("Employee not assigned to this project")

        self.assigned_employees.remove(emp_id)

    def list_project_members(self):

        if not self.assigned_employees:
            print("No employees assigned to this project")
            return

        print("\nProject Members:")

        for emp in self.assigned_employees:
            print(emp)

#-----------------------------------------------
# LOAD CSV AND SAVE TO CSV
#-----------------------------------------------

# load_projects() returns a dictionary of projects with project_id as key
def load_projects():

    try:
        with open(PROJECT_FILE, "r") as file:
            return json.load(file)              #return type of json.load() depends on the structure of the file, here it is returning dict
    except FileNotFoundError:
        print("Projects data file not found")
    except JSONDecodeError:
        print("Error: Corrupt JSON File for projects")
        return {}                                # good practice to always return a safe default value, not None, for functions that load data, to prevent code from crashing


def save_projects(projects):

    with open(PROJECT_FILE, "w") as f:          # No try block: write failures should be raised instead of being silently handled
        json.dump(projects, f, indent=4)        #indent=4, to indent each nesting level by 4 spaces, for cleaner file structure

def get_project(project_id):

    projects = load_projects()
    project_data = projects.get(project_id)  # default is None

    if project_data is None:
        raise ValueError("Project not found")
    # Create Project Obj from project_data dict
    project = Project(project_id, project_data["project_name"], project_data["assigned_employees"])
    return project

#-----------------------------------------------
# SYSTEM FUNCTIONS
#-----------------------------------------------
def create_project(projectId, projectName):
    #load existing projects, here projects will be a dictionary
    projects = load_projects()

    # Check Duplicate
    if projectId in projects:
        raise ValueError("This Project ID already exists")

    #add new project
    projects[projectId] = {
        "project_name" : projectName,
        "assigned_employees": []        #start with empty list
    }
    save_projects(projects)
    print("Project created successfully.")


def assign_employee_to_project(project_id, emp_id):

    # Load all projects
    projects = load_projects()              #projects is a dict here, with project_id as the key

    if project_id not in projects:
        print("Project not found")
        return

    project_data = projects[project_id]

    # Create Project object -> assign_employee() -> add to projects dict -> save back to file
    project = Project(project_id, project_data['project_name'], project_data['assigned_employees'])

    project.assign_employee(emp_id)

    #update assigned_employees list of given project_id in projects
    projects[project_id]['assigned_employees'] =  project.assigned_employees

    #save to file
    save_projects(projects)

    print("Employee assigned successfully")

def remove_employee_from_project(project_id, emp_id):

    # Load all projects
    projects = load_projects()  # projects is a dict here, with project_id as the key

    if project_id not in projects:
        print("Project not found")
        return

    project_data = projects[project_id]
    # Create Project object
    project = Project(project_id, project_data['project_name'], project_data['assigned_employees'])

    project.remove_employee(emp_id)

    # update assigned_employees list of given project_id in projects
    projects[project_id]['assigned_employees'] = project.assigned_employees

    # save to file
    save_projects(projects)

    print(f"Employee removed successfully from Project ({project_id})")