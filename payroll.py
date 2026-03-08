from ERMS_Project.employee import load_employees


class Payroll:

# Tax Slabs on Monthly Salary Basis
    TAX_SLABS = [
        (5000, 0.25),  # upto 5000, 25% tax
        (10000, 0.40),  # upto 10000, 40% tax
        (15000, 0.50),  # upto 15000, 50% tax
        (float("inf"), 0.55)  # for more than 15000, 55% tax, inf refers to infinity, here it means 15001 - infinity, apply 55% tax
    ]

    def __init__(self, employee):
        self.employee = employee

    def calculate_tax(self):

        salary = self.employee.salary
        total_tax = 0
        prev_limit = 0

        for limit, rate in self.TAX_SLABS:

            if salary > limit:
                total_tax += (limit - prev_limit) * rate
                prev_limit = limit
            else:
                total_tax += (salary - prev_limit) * rate
                break
        return total_tax

# Calculate total deduction amount based on leave days
    def deduct_leave(self, leave_days):
        if leave_days < 0:
            raise ValueError("Leave days cannot be negative")

        sal_per_day = self.employee.salary / 30

        total_deduction = sal_per_day * leave_days

        return total_deduction

    def generate_salary_slip(self, leave_days):

        gross_salary = self.employee.salary
        tax_deduction = self.calculate_tax()
        leave_deduction = self.deduct_leave(leave_days)

        net_salary = gross_salary - (tax_deduction + leave_deduction)

        slip = {
            "Employee ID"       :   self.employee.employee_id,
            "Employee Name"     :   self.employee.name,
            "Department"        :   self.employee.department,
            "Gross Salary"      :   gross_salary,
            "Leave Deduction"   :   f"${round(leave_deduction, 2)}",
            "Tax Deduction"     :   f"${round(tax_deduction, 2)}",
            "Net Salary"        :   f"${round(net_salary, 2)}"

        }

        print(f"\n{'='*40}")            #it prints '=' 40 times
        print(f"{'SALARY SLIP':^40}")   # ^ is center alignment symbol, it center aligns 'SALARY SLIP' within 40 char space
        print(f"{'=' * 40}")

        for key, value in slip.items():
            print(f"{key:<20}: {value}")       # < is a left alignment symbol, here it left aligns key in 20 char width


def process_payroll():

    employees = load_employees()

    if not employees:
        print("No employees found.")
        return

    emp_id = input("Enter employee ID: ")

    emp = next((e for e in employees if e.employee_id == emp_id), None)  #return employee object of given emp_id

    if not emp:
        print("Employee not found.")
        return

    leave_days = int(input("Enter leave days: "))

    payroll = Payroll(emp)
    payroll.generate_salary_slip(leave_days)






