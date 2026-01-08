from utils.data_loader import load_payroll_data
from workflows.payroll_workflow import PayrollWorkflow

def main():
    # Load data
    current_df = load_payroll_data("data/current_payroll.csv")
    historical_df = load_payroll_data("data/historical_payroll.csv")

    workflow = PayrollWorkflow()

    print("\nPayroll Agent Report")
    print("-" * 50)

    results = []

    # Run payroll for each employee
    for _, row in current_df.iterrows():
        employee_id = row["employee_id"]

        result = workflow.run(
            employee_id=employee_id,
            payroll_df=current_df,
            historical_df=historical_df
        )

        results.append(result)

        # Console Output (same spirit as before, richer now)
        print(f"\nEmployee ID: {employee_id}")
        print(f"Gross Salary     : {result['gross_salary']}")
        print(f"Total Deductions : {result['total_deductions']}")
        print(f"Net Salary       : {result['net_salary']}")

        if result.get("anomaly", {}).get("anomaly"):
            print("⚠️  Anomaly Detected")

        print(f"Explanation      : {result['explanation']}")

    return results


if __name__ == "__main__":
    main()
