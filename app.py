import streamlit as st
import pandas as pd
from datetime import datetime
import os

from workflows.payroll_workflow import PayrollWorkflow


# -------------------------------------------------
# Helpers
# -------------------------------------------------
def safe_float(x):
    try:
        return float(x)
    except Exception:
        return 0.0


def generate_salary_slip_df(result):
    rows = []

    for k, v in result["earnings"].items():
        rows.append({
            "Type": "Earning",
            "Component": k,
            "Amount": safe_float(v)
        })

    for k, v in result["deductions"].items():
        rows.append({
            "Type": "Deduction",
            "Component": k,
            "Amount": safe_float(v)
        })

    rows.extend([
        {"Type": "Summary", "Component": "Gross Salary", "Amount": safe_float(result["gross_salary"])},
        {"Type": "Summary", "Component": "Total Deductions", "Amount": safe_float(result["total_deductions"])},
        {"Type": "Summary", "Component": "Net Salary", "Amount": safe_float(result["net_salary"])},
    ])

    return pd.DataFrame(rows)


# -------------------------------------------------
# Streamlit Config
# -------------------------------------------------
st.set_page_config(
    page_title="Payroll Intelligence Agent",
    layout="wide"
)

st.title("💼 Payroll Execution & Intelligence")
st.caption("Payroll execution, validation, anomaly detection & payslips")


# -------------------------------------------------
# Sidebar – Role & Uploads
# -------------------------------------------------
role = st.sidebar.selectbox(
    "Role",
    ["HR", "Finance"],
    label_visibility="collapsed"
)

role_icon = "🧑‍💼" if role == "HR" else "💰"
st.sidebar.header(f"{role_icon} {role} View")

st.sidebar.divider()
st.sidebar.subheader("📤 Payroll Files")

current_file = st.sidebar.file_uploader(
    "Current Payroll (.csv)",
    type=["csv"],
    help="Monthly payroll data"
)

historical_file = st.sidebar.file_uploader(
    "Historical Payroll (.csv)",
    type=["csv"],
    help="Used for anomaly detection"
)


# -------------------------------------------------
# Main Logic
# -------------------------------------------------
if current_file and historical_file:
    current_df = pd.read_csv(current_file)
    historical_df = pd.read_csv(historical_file)

    with st.expander("📄 Preview Uploaded Data", expanded=False):
        st.subheader("Current Payroll")
        st.dataframe(current_df, width="stretch")

        st.subheader("Historical Payroll")
        st.dataframe(historical_df, width="stretch")

    if st.button("▶️ Run Payroll Agent"):
        workflow = PayrollWorkflow()
        results = []

        for _, row in current_df.iterrows():
            employee_id = row["employee_id"]

            result = workflow.run(
                employee_id=employee_id,
                payroll_df=current_df,
                historical_df=historical_df
            )

            result["employee_id"] = employee_id
            result["payroll_period"] = datetime.now().strftime("%B %Y")
            results.append(result)

        summary_df = pd.DataFrame(results)

        # ==================================================
        # PAYROLL SUMMARY (COMMON)
        # ==================================================
        st.subheader("📊 Payroll Run Summary")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Employees", len(summary_df))
        col2.metric("Total Net Pay", f"₹ {summary_df['net_salary'].sum():,.2f}")
        col3.metric("Validation Issues", summary_df["validation_issues"].apply(len).gt(0).sum())
        col4.metric("Anomalies", summary_df["anomalies"].apply(len).gt(0).sum())

        # ==================================================
        # FINANCE VIEW
        # ==================================================
        if role == "Finance":
            st.subheader("💰 Finance Payroll Overview")

            finance_df = summary_df[[
                "employee_id",
                "gross_salary",
                "total_deductions",
                "net_salary"
            ]]

            st.dataframe(finance_df, width="stretch", hide_index=True)

            st.download_button(
                "⬇ Download Finance Payroll Report",
                finance_df.to_csv(index=False),
                file_name="finance_payroll_report.csv",
                mime="text/csv"
            )

            if os.path.exists("data/payroll_audit_summary.csv"):
                with open("data/payroll_audit_summary.csv", "r", encoding="utf-8") as f:
                    st.download_button(
                        "⬇ Download Payroll Audit Log",
                        f.read(),
                        file_name="payroll_audit_summary.csv",
                        mime="text/csv"
                    )

        # ==================================================
        # HR VIEW
        # ==================================================
        if role == "HR":
            st.subheader("🧾 Employee Payslips")

            for r in results:
                status = "⚠️" if r["validation_issues"] or r["anomalies"] else "✅"

                with st.expander(f"{status} Employee ID: {r['employee_id']}"):

                    col1, col2, col3 = st.columns(3)
                    col1.metric("Gross Salary", f"₹ {r['gross_salary']:,.2f}")
                    col2.metric("Total Deductions", f"₹ {r['total_deductions']:,.2f}")
                    col3.metric("Net Salary", f"₹ {r['net_salary']:,.2f}")

                    st.divider()
                    st.markdown("### 🧾 Payslip Breakdown")

                    slip_df = generate_salary_slip_df(r)
                    st.dataframe(slip_df, hide_index=True, width="stretch")

                    st.download_button(
                        "⬇ Download Salary Slip (CSV)",
                        slip_df.to_csv(index=False),
                        file_name=f"salary_slip_{r['employee_id']}.csv",
                        mime="text/csv"
                    )

                    if r["validation_issues"]:
                        st.warning("⚠️ Validation Issues")
                        for issue in r["validation_issues"]:
                            for msg in issue.get("issues", []):
                                st.write(f"- {msg}")

                    if r["anomalies"]:
                        st.error("🚨 Anomalies")
                        for a in r["anomalies"]:
                            d = a["details"]
                            st.write(
                                f"- Salary changed by {d['change_percentage']}% "
                                f"(Prev: {d['previous_gross']}, Current: {d['current_gross']})"
                            )

                    if not r["validation_issues"] and not r["anomalies"]:
                        st.success("No issues detected.")

else:
    st.info("Please upload both current and historical payroll CSV files.")
