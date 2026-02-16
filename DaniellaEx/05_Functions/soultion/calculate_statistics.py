from typing import Optional 


def calculate_statistics(**kwargs:list[float])->dict[str,dict[str,Optional[float]]]:
    for  key ,value in kwargs.items():
