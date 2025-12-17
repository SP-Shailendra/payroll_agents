def mask_employee_id(emp_id: str) -> str:
    if len(emp_id) <= 2:
        return "***"
    return emp_id[:2] + "***" + emp_id[-1]
