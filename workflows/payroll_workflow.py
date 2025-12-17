from agents.validation_agent import PayrollValidationAgent
from agents.anomaly_agent import PayrollAnomalyAgent
from agents.explanation_agent import PayrollExplanationAgent

class PayrollWorkflow:
    """
    Orchestrates payroll validation, anomaly detection, and explanation.
    """

    def run(self, current_df, historical_df):
        validation_agent = PayrollValidationAgent()
        anomaly_agent = PayrollAnomalyAgent()
        explanation_agent = PayrollExplanationAgent()

        results = []

        validations = validation_agent.run(current_df)
        anomalies = anomaly_agent.run(current_df, historical_df)

        for v in validations:
            results.append({
                "employee_id": v["employee_id"],
                "type": "Validation",
                "explanation": explanation_agent.explain_validation(v)
            })

        for a in anomalies:
            results.append({
                "employee_id": a["employee_id"],
                "type": "Anomaly",
                "explanation": explanation_agent.explain_anomaly(a)
            })

        return results
