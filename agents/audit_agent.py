# agents/audit_agent.py

import json
import os
from datetime import datetime

AUDIT_LOG_JSON = "data/payroll_audit_detail.jsonl"
AUDIT_LOG_CSV = "data/payroll_audit_summary.csv"


class AuditAgent:
    """
    Persists payroll audit data in JSON-safe and reporting-friendly formats.
    """

    def _safe(self, obj):
        if isinstance(obj, dict):
            return {k: self._safe(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._safe(v) for v in obj]
        try:
            return float(obj)
        except Exception:
            return obj

    def run(self, payload: dict):
        timestamp = datetime.utcnow().isoformat()

        payload["execution_timestamp"] = timestamp
        safe_payload = self._safe(payload)

        # -----------------------------
        # 1️⃣ JSONL – full audit record
        # -----------------------------
        os.makedirs("data", exist_ok=True)
        with open(AUDIT_LOG_JSON, "a", encoding="utf-8") as f:
            f.write(json.dumps(safe_payload) + "\n")

        # -----------------------------
        # 2️⃣ CSV – summary for reports
        # -----------------------------
        summary_row = (
            f"{payload['payroll_run_id']},"
            f"{payload['payroll_period']},"
            f"{payload['employee_id']},"
            f"{safe_payload.get('gross_salary', 0)},"
            f"{safe_payload.get('net_salary', 0)},"
            f"{len(payload.get('validation_issues', []))},"
            f"{len(payload.get('anomalies', []))},"
            f"{timestamp}\n"
        )

        if not os.path.exists(AUDIT_LOG_CSV):
            with open(AUDIT_LOG_CSV, "w", encoding="utf-8") as f:
                f.write(
                    "payroll_run_id,payroll_period,employee_id,"
                    "gross_salary,net_salary,"
                    "validation_issue_count,anomaly_count,execution_timestamp\n"
                )

        with open(AUDIT_LOG_CSV, "a", encoding="utf-8") as f:
            f.write(summary_row)
