def analyze_log_content(log_content: str) -> dict:
    """Count the number of ERROR, WARNING, and INFO messages in log content."""
    result: dict = {"ERROR": 0, "WARNING": 0, "INFO": 0}
    splited_line = log_content.split("\n")
    for line in splited_line:
        if "ERROR" in line:
            result["ERROR"] += 1
        elif "WARNING" in line:
            result["WARNING"] += 1
        elif "INFO" in line:
            result["INFO"] += 1

    return result
