def extract_key(log_line: str, key: str) -> str:
    """Extract the value of a given key from a log line by locating and slicing it"""
    key_index = log_line.find(key)
    sliced_log_line1 = log_line[key_index:-1]
    closer_index = sliced_log_line1.find("]")
    sliced_log_line2 = sliced_log_line1[1 + len(key) : closer_index]
    return sliced_log_line2
