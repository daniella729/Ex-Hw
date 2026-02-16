def filter_adults(people: list[dict]) -> list[dict]:
    is_adults: list[dict] = list(filter(lambda person: person["age"] >= 18), people)
    return is_adults


def get_names(people: list[dict]) -> list[str]:
    names: list[str] = list(map(lambda person: person["name"], people))
    return names


def sort_by_age(people: list[dict]) -> list[dict]:
    sort_by_age: list[dict] = list(sorted(people, key=lambda person: person["age"]))
    return sort_by_age
