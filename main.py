from utils.data_loader import load_payroll_data
from workflows.payroll_workflow import PayrollWorkflow

def main():
    current_df = load_payroll_data("data/current_payroll.csv")
    historical_df = load_payroll_data("data/historical_payroll.csv")

    workflow = PayrollWorkflow()
    results = workflow.run(current_df, historical_df)

    print("\nPayroll Agent Report")
    print("-" * 40)

    for r in results:
        print(f"[{r['type']}] {r['explanation']}")

if __name__ == "__main__":
    main()
