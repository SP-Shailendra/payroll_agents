# agents/payroll_approval_agent.py

from datetime import datetime
import uuid


class PayrollApprovalAgent:
    """
    Handles multi-stage payroll approval:
    HR → Finance → Final
    """

    def init_state(self, payroll_run_id=None):
        """
        Initializes approval workflow.
        payroll_run_id is optional to avoid Streamlit reload issues.
        """

        if payroll_run_id is None:
            payroll_run_id = f"PR-UNKNOWN-{uuid.uuid4().hex[:6]}"

        return {
            "payroll_run_id": payroll_run_id,
            "status": "HR_PENDING",
            "approved_by": None,
            "timestamp": None
        }

    def approve(self, payroll_run_id, role, current_status):
        """
        Moves payroll to next approval stage
        """

        if role == "HR" and current_status == "HR_PENDING":
            return {
                "payroll_run_id": payroll_run_id,
                "status": "FINANCE_PENDING",
                "approved_by": "HR",
                "timestamp": datetime.utcnow().isoformat()
            }

        if role == "Finance" and current_status == "FINANCE_PENDING":
            return {
                "payroll_run_id": payroll_run_id,
                "status": "FINAL_APPROVED",
                "approved_by": "Finance",
                "timestamp": datetime.utcnow().isoformat()
            }

        return {
            "payroll_run_id": payroll_run_id,
            "status": current_status,
            "approved_by": None,
            "timestamp": None
        }
