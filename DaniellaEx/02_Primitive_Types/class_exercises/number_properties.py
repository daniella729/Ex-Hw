import sys

number = int(input("Enter an integer:"))
print(f"Number:{(number)}")
print(f"Type:{type(number)}")
print(f"Size in bytes:{sys.getsizeof(number)}")
print(f"Number squared:{pow(number,2)}")
print(f"As float:{float(number)}")
print(f"As string:{str(number)}")
print(f"Is positive:{number >0}")
