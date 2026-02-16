def validate_temperature(value: float, from_unit: str, to_unit: str) -> None:
    if from_unit not in ["C", "F", "K"] or to_unit not in ["C", "F", "K"]:
        raise ValueError("Invalid unit.Use 'C' ,'F' ,'K'.")

    if from_unit == "K" and value < 0:
        raise ValueError("Kalvin cannot be negative")

    if from_unit == "C" and value < -273.15:
        raise ValueError("Temperature below absolute zero.")


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    validate_temperature(value, from_unit, to_unit)
    if from_unit == to_unit:
        return value

    if from_unit == "C" and to_unit == "F":
        return value * 9 / 5 + 32

    if from_unit == "F" and to_unit == "C":
        return (value - 32) * 5 / 9

    if from_unit == "C" and to_unit == "K":
        return value + 273.15

    if from_unit == "K" and to_unit == "C":
        return value - 273.15

    if from_unit == to_unit:
        return value
