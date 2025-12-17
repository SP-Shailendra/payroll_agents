import streamlit as st
import pandas as pd

from workflows.payroll_workflow import PayrollWorkflow

st.set_page_config(
    page_title="Payroll Agent",
    layout="wide"
)

st.title("💼 Payroll Validation & Intelligence Agent")
st.caption("Read-only payroll validation, anomaly detection, and explanation")

# -------------------------
# File Upload Section
# -------------------------
st.sidebar.header("Upload Payroll Files")

current_file = st.sidebar.file_uploader(
    "Upload Current Payroll CSV",
    type=["csv"]
)

historical_file = st.sidebar.file_uploader(
    "Upload Historical Payroll CSV",
    type=["csv"]
)

# -------------------------
# Main Execution
# -------------------------
if current_file and historical_file:
    current_df = pd.read_csv(current_file)
    historical_df = pd.read_csv(historical_file)

    st.subheader("📄 Current Payroll Preview")
    st.dataframe(current_df, use_container_width=True)

    st.subheader("📄 Historical Payroll Preview")
    st.dataframe(historical_df, use_container_width=True)

    if st.button("Run Payroll Agent"):
        workflow = PayrollWorkflow()
        results = workflow.run(current_df, historical_df)

        st.subheader("🚨 Payroll Issues & Insights")

        if not results:
            st.success("No payroll issues detected.")
        else:
            for r in results:
                if r["type"] == "Validation":
                    st.warning(f"**Validation Issue**\n\n{r['explanation']}")
                else:
                    st.error(f"**Anomaly Detected**\n\n{r['explanation']}")

else:
    st.info("Please upload both current and historical payroll CSV files.")
