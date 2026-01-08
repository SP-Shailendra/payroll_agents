# agents/payroll_calculation_agent.py

class PayrollCalculationAgent:
    """
    Computes gross and net salary
    """

    def run(self, earnings, deductions):
        gross = sum(earnings.values())
        total_deductions = sum(deductions.values())
        net = gross - total_deductions

        return {
            "gross_salary": gross,
            "total_deductions": total_deductions,
            "net_salary": net
        }
