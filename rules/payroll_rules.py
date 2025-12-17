def validate_payroll_record(record):
    issues = []

    if record["gross_salary"] <= 0:
        issues.append("Gross salary must be greater than zero")

    if record["net_salary"] > record["gross_salary"]:
        issues.append("Net salary exceeds gross salary")

    mandatory_deductions = ["tax", "insurance"]
    for deduction in mandatory_deductions:
        if record[deduction] <= 0:
            issues.append(f"Mandatory deduction missing or zero: {deduction}")

    return issues
