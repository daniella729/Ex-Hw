import json

my_dict = {"name": "Alice", "age": 30, "city": "New York", "work": None}


json_str = json.dumps(my_dict)

#######################################################


class Cache:

    __slots__ = ["cache", "max_size"]

    def __init__(self, max_size=100):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        if len(self.cache) >= self.max_size:
            self.cache.pop(next(iter(self.cache)))  # Remove the first item (FIFO)
        self.cache[key] = value


cache = Cache(max_size=2)


READ_MODE = "r"
DEFAULT_JSON_FILE = "data.json"


# Loading JSON from a file into a dict


def load_json_file(file_path):
    if file_path in cache:
        print("Loading from cache...")
        return cache[file_path]

    try:
        with open(file_path, READ_MODE) as file:
            # Load the JSON data into a Python dictionary
            data_dict = json.load(file)

        # Now you can work with the data as a Python dictionary
        print(type(data_dict))
        print(data_dict)
        cache[file_path] = data_dict
        return data_dict

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except json.JSONDecodeError:
        print(
            f"Error: Could not decode JSON from the file '{file_path}'. Check file format."
        )


## HW: Create a function that will save a Python dictionary to a JSON file.


if __name__ == "__main__":
    load_json_file(DEFAULT_JSON_FILE)
