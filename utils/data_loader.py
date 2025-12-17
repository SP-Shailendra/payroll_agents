import pandas as pd

def load_payroll_data(path: str) -> pd.DataFrame:
    """
    Loads payroll CSV data into a DataFrame.
    """
    return pd.read_csv(path)
