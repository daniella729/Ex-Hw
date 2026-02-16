def extract_pid(log_line: str) -> int:
    """Extract the PID number from a log line and convert it to an integer"""
    pid_index = log_line.find("pid")
    sliced_log_line1 = log_line[pid_index:-1]
    closer_index = sliced_log_line1.find("]")
    sliced_log_line2 = sliced_log_line1[4:closer_index]
    return int(sliced_log_line2)
