from solution.repository.csv_accessor import CsvFileAccessor
from pathlib import Path


def test_write_empty_rows(tmp_path: Path) -> None:
    file_path = tmp_path / "test1.csv"
    accessor = CsvFileAccessor(str(file_path))
    accessor.write([])
    result = accessor.read()
    assert result == []


def test_write_and_read_rows(tmp_path: Path) -> None:
    file_path = tmp_path / "test2.csv"
    accessor = CsvFileAccessor(str(file_path))

    rows = [
        {"description": "Salary", "amount": 5000},
        {"description": "Food", "amount": 1000},
    ]
    accessor.write(rows)
    result = accessor.read()
    assert len(result) == 2
    assert result[1]["description"] == "Food"


def test_read_non_exist_file() -> None:
    accessor = CsvFileAccessor("ex1.csv")
    result = accessor.read()
    assert result == []
