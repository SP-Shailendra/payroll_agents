class PayrollExplanationAgent:
    """
    Generates human-readable explanations for payroll issues.
    """

    def explain_validation(self, issue):
        return (
            f"Employee {issue['employee_id']} has payroll validation issues. "
            f"Issues detected: {', '.join(issue['issues'])}. "
            f"Please verify payroll inputs."
        )

    def explain_anomaly(self, anomaly):
        details = anomaly["details"]
        return (
            f"Employee {anomaly['employee_id']} has a salary change of "
            f"{details['change_percentage']}% compared to the previous period. "
            f"Previous Gross: {details['previous_gross']}, "
            f"Current Gross: {details['current_gross']}. "
            f"Please verify bonus or compensation changes."
        )
