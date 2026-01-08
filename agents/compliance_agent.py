# agents/compliance_agent.py

from rules.payroll_rules import (
    calculate_pf,
    calculate_esi,
    calculate_pt,
    calculate_tds
)

class ComplianceAgent:
    """
    Applies statutory deductions using centralized payroll rules
    """

    def run(self, earnings: dict):
        """
        earnings: dict with numeric values only
        """

        # ✅ Force scalar values
        clean_earnings = {
            k: float(v) for k, v in earnings.items()
        }

        basic = clean_earnings.get("Basic", 0.0)
        gross = sum(clean_earnings.values())

        deductions = {}

        deductions["PF"] = calculate_pf(basic)
        deductions["ESI"] = calculate_esi(gross)
        deductions["PT"] = calculate_pt()

        taxable_income = gross - deductions["PF"]
        deductions["TDS"] = calculate_tds(taxable_income)

        return deductions
