def extract_data_from_html(html_line: str) -> str:
    """Extract the title text from an HTML line by locating and slicing it"""
    first_title = html_line.find("title")
    sliced_html_line1 = html_line[first_title:-1]
    closer_index = sliced_html_line1.find("<")
    sliced_html_line2 = sliced_html_line1[6:closer_index]
    return sliced_html_line2
