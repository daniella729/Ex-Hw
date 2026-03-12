import csv
import os
from typing import Any


class CsvFileAccessor:
    """reading and writing to CSV file."""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def read(self) -> list[dict[str, Any]]:
        if os.path.exists(self.file_path) is False:
            return []
        elif os.path.getsize(self.file_path) == 0:
            return []
        else:
            with open(self.file_path, "r", newline="") as file:
                file_reader = csv.DictReader(file)
                if file_reader.fieldnames is None:
                    return []
                else:
                    return list(file_reader)

    def write(self, rows: list[dict[str, Any]]) -> None:
        if rows:
            fieldnames = list(rows[0].keys())
            with open(self.file_path, "w", newline="") as file:
                file_writer = csv.DictWriter(file, fieldnames)
                file_writer.writeheader()
                file_writer.writerows(rows)
        else:
            return
