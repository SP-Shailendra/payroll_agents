from rules.payroll_rules import validate_payroll_record

class PayrollValidationAgent:
    """
    Performs rule-based payroll validation.
    """

    def run(self, payroll_df):
        validation_results = []

        for _, row in payroll_df.iterrows():
            issues = validate_payroll_record(row)

            if issues:
                validation_results.append({
                    "employee_id": row["employee_id"],
                    "issue_type": "Validation Error",
                    "issues": issues,
                    "severity": "High"
                })

        return validation_results
