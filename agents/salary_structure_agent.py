# agents/salary_structure_agent.py

class SalaryStructureAgent:
    """
    Fetches and normalizes salary structure for an employee.
    Always returns numeric (float) values.
    """

    def run(self, employee_id, payroll_df):
        emp_row = payroll_df[payroll_df["employee_id"] == employee_id].iloc[0]

        # Case 1: Component-based salary exists
        if all(col in payroll_df.columns for col in ["basic", "hra", "allowances"]):
            structure = {
                "Basic": float(emp_row["basic"]),
                "HRA": float(emp_row["hra"]),
                "Allowances": float(emp_row["allowances"])
            }

        # Case 2: Fallback to gross salary
        elif "gross_salary" in payroll_df.columns:
            gross = float(emp_row["gross_salary"])
            structure = {
                "Basic": round(gross * 0.50, 2),
                "HRA": round(gross * 0.30, 2),
                "Allowances": round(gross * 0.20, 2)
            }

        else:
            raise ValueError(
                "Payroll data must contain either salary components "
                "or gross_salary column"
            )

        return structure
