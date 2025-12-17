class PayrollAnomalyAgent:
    """
    Detects anomalies by comparing current payroll with historical data.
    """

    def run(self, current_df, historical_df, threshold=0.2):
        anomalies = []

        historical_map = historical_df.set_index("employee_id")

        for _, row in current_df.iterrows():
            emp_id = row["employee_id"]

            if emp_id not in historical_map.index:
                continue

            previous = historical_map.loc[emp_id]
            prev_gross = previous["gross_salary"]
            curr_gross = row["gross_salary"]

            if prev_gross > 0:
                change_ratio = (curr_gross - prev_gross) / prev_gross

                if abs(change_ratio) > threshold:
                    anomalies.append({
                        "employee_id": emp_id,
                        "issue_type": "Salary Anomaly",
                        "severity": "High",
                        "details": {
                            "previous_gross": prev_gross,
                            "current_gross": curr_gross,
                            "change_percentage": round(change_ratio * 100, 2)
                        }
                    })

        return anomalies
