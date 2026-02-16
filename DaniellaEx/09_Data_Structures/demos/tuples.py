from collections import namedtuple
from dataclasses import dataclass
from pympler import asizeof

# Tuples used as dict keys

my_dict = {(1, 2): "x=1 and y=2", (2, 2): "x=2 and y=2"}

# Memory size of tuples vs lists

my_list = [1, 2, 3, 4, 5]
my_tuple = (1, 2, 3, 4, 5)
tuples_list = [(1, 2), (3, 4), (5, 6)]
tuples_tuple = ((1, 2), (3, 4), (5, 6))
tuple_of_lists = ([1, 2], [3, 4], [5, 6])


def my_func():
    return 1, 2, 3


a, b, c = my_func()


my_tuple = 1, 2, 3, 4, 5


@dataclass(slots=True)
class PointClass:
    x: int
    y: int


PointTuple = namedtuple("PointTuple", ["x", "y"])


my_point_class = PointClass(1, 2)
my_point_tuple = PointTuple(1, 2)


print(my_point_class.x, my_point_class.y)
print(my_point_tuple.x, my_point_tuple.y)


# Print their sizes in memory

print("Size of point class:", asizeof.asizeof(my_point_class))
print("Size of point tuple:", asizeof.asizeof(my_point_tuple))
