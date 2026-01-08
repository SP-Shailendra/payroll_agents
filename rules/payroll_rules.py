# rules/payroll_rules.py

"""
Centralized payroll rules and validations.
Used by validation_agent, compliance_agent, and payroll workflow.
"""

# ===============================
# Statutory Configuration
# ===============================

PF_RATE = 0.12                # 12% Provident Fund
PF_WAGE_LIMIT = 15000         # PF applicable up to this basic salary

ESI_RATE = 0.0075             # 0.75% Employee ESI
ESI_WAGE_LIMIT = 21000        # ESI applicable below this gross salary

PT_AMOUNT = 200               # Professional Tax (flat)
TDS_RATE = 0.10               # Simplified flat TDS for MVP

# ===============================
# Validation Rules
# ===============================

def validate_payroll_record(record):
    """
    Validates a computed payroll record.
    This is executed AFTER payroll calculation.
    """

    issues = []

    gross = record.get("gross_salary", 0)
    net = record.get("net_salary", 0)
    deductions = record.get("deductions", {})

    # --- Salary sanity checks ---
    if gross <= 0:
        issues.append("Gross salary must be greater than zero")

    if net < 0:
        issues.append("Net salary cannot be negative")

    if net > gross:
        issues.append("Net salary cannot exceed gross salary")

    # --- Mandatory statutory checks ---
    mandatory_deductions = ["PF", "ESI", "PT"]

    for deduction in mandatory_deductions:
        if deduction not in deductions:
            issues.append(f"Mandatory deduction missing: {deduction}")

    # --- Logical checks ---
    if "PF" in deductions and deductions["PF"] > gross * PF_RATE:
        issues.append("PF deduction exceeds allowed limit")

    if "ESI" in deductions and gross > ESI_WAGE_LIMIT and deductions["ESI"] > 0:
        issues.append("ESI applied even though gross exceeds eligibility limit")

    return issues


# ===============================
# Helper Calculation Functions
# ===============================

def calculate_pf(basic_salary):
    """
    PF is calculated on basic salary, capped by wage limit.
    """
    applicable_wage = min(basic_salary, PF_WAGE_LIMIT)
    return round(applicable_wage * PF_RATE, 2)


def calculate_esi(gross_salary):
    """
    ESI applies only if gross salary is within limit.
    """
    if gross_salary <= ESI_WAGE_LIMIT:
        return round(gross_salary * ESI_RATE, 2)
    return 0.0


def calculate_pt():
    """
    Professional tax is flat for MVP.
    """
    return PT_AMOUNT


def calculate_tds(taxable_income):
    """
    Simplified TDS calculation for MVP.
    """
    return round(taxable_income * TDS_RATE, 2)
