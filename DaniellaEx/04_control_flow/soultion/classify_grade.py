def classify_grade(score: int) -> str:
    if score < 0 or score > 100:
        raise ValueError("Score must be between 0 and 100.")
    if score >= 90 and score <= 100:
        return "A"

    if score >= 80 and score <= 89:
        return "B"

    if score >= 70 and score <= 79:
        return "C"

    if score >= 60 and score <= 69:
        return "D"

    if score >= 0 and score <= 59:
        return "F"
