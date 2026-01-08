# workflows/payroll_workflow.py

import pandas as pd
from datetime import datetime
import uuid

from agents.validation_agent import PayrollValidationAgent
from agents.anomaly_agent import PayrollAnomalyAgent
from agents.explanation_agent import PayrollExplanationAgent
from agents.salary_structure_agent import SalaryStructureAgent
from agents.variable_pay_agent import VariablePayAgent
from agents.compliance_agent import ComplianceAgent
from agents.payroll_calculation_agent import PayrollCalculationAgent
from agents.audit_agent import AuditAgent
from agents.payroll_approval_agent import PayrollApprovalAgent


# =================================================
# Payroll Run Context (one per execution)
# =================================================
payroll_run_id = f"PR-{datetime.now().strftime('%Y%m')}-{uuid.uuid4().hex[:6]}"
payroll_period = datetime.now().strftime("%B %Y")


class PayrollWorkflow:
    """
    Orchestrates end-to-end payroll execution for a single employee:
    Earnings → Deductions → Calculation → Validation → Anomaly → Explanation → Audit
    """

    def __init__(self):
        self.validation_agent = PayrollValidationAgent()
        self.anomaly_agent = PayrollAnomalyAgent()
        self.explainer = PayrollExplanationAgent()
        self.structure_agent = SalaryStructureAgent()
        self.variable_agent = VariablePayAgent()
        self.compliance_agent = ComplianceAgent()
        self.calculation_agent = PayrollCalculationAgent()
        self.audit_agent = AuditAgent()
        self.approval_agent = PayrollApprovalAgent()

    def run(self, employee_id, payroll_df, historical_df):
        """
        Executes payroll for a single employee.
        Approval state is initialized here and managed at UI / orchestration level.
        """

        # =================================================
        # 0️⃣ Initialize Approval State (DRAFT)
        # =================================================
        approval_state = self.approval_agent.init_state(payroll_run_id)

        # =================================================
        # 1️⃣ Earnings (Salary Structure + Variable Pay)
        # =================================================
        earnings = self.structure_agent.run(employee_id, payroll_df)
        earnings.update(self.variable_agent.run(employee_id, payroll_df))

        # =================================================
        # 2️⃣ Statutory Deductions
        # =================================================
        deductions = self.compliance_agent.run(earnings)

        # =================================================
        # 3️⃣ Payroll Calculation (Gross → Net)
        # =================================================
        payroll = self.calculation_agent.run(earnings, deductions)

        payroll_record = {
            "employee_id": employee_id,
            "gross_salary": payroll["gross_salary"],
            "net_salary": payroll["net_salary"],
            "deductions": deductions
        }

        # =================================================
        # 4️⃣ Validation (Post-calculation)
        # =================================================
        validation_issues = self.validation_agent.run(
            pd.DataFrame([payroll_record])
        )

        # =================================================
        # 5️⃣ Anomaly Detection (vs historical)
        # =================================================
        anomalies = self.anomaly_agent.run(
            current_df=pd.DataFrame([payroll_record]),
            historical_df=historical_df
        )

        # =================================================
        # 6️⃣ Explanation (Human readable)
        # =================================================
        explanations = []

        for issue in validation_issues:
            explanations.append(self.explainer.explain_validation(issue))

        for anomaly in anomalies:
            explanations.append(self.explainer.explain_anomaly(anomaly))

        final_explanation = (
            "\n".join(explanations)
            if explanations
            else "No validation issues or anomalies detected."
        )

        # =================================================
        # 7️⃣ Audit (JSON-safe + Approval-aware)
        # =================================================
        self.audit_agent.run({
            "payroll_run_id": payroll_run_id,
            "payroll_period": payroll_period,
            "execution_status": "SUCCESS",
            "approval_status": approval_state["status"],  # DRAFT at this stage
            "employee_id": employee_id,
            "earnings": earnings,
            "deductions": deductions,
            "gross_salary": payroll["gross_salary"],
            "net_salary": payroll["net_salary"],
            "validation_issues": validation_issues,
            "anomalies": anomalies
        })

        # =================================================
        # 8️⃣ Return Result to UI
        # =================================================
        return {
            "employee_id": employee_id,
            "payroll_run_id": payroll_run_id,
            "payroll_period": payroll_period,
            "approval_status": approval_state["status"],
            "gross_salary": payroll["gross_salary"],
            "total_deductions": payroll["total_deductions"],
            "net_salary": payroll["net_salary"],
            "earnings": earnings,
            "deductions": deductions,
            "validation_issues": validation_issues,
            "anomalies": anomalies,
            "explanation": final_explanation
        }
