# agents/variable_pay_agent.py

class VariablePayAgent:
    """
    Handles incentives and bonuses.
    Always returns numeric (float) values.
    """

    def run(self, employee_id, payroll_df):
        emp_row = payroll_df[payroll_df["employee_id"] == employee_id].iloc[0]

        bonus = float(emp_row["bonus"]) if "bonus" in payroll_df.columns else 0.0
        incentive = (
            float(emp_row["incentive"])
            if "incentive" in payroll_df.columns
            else 0.0
        )

        return {
            "Bonus": bonus,
            "Incentive": incentive
        }
