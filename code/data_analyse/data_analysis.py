# File containing functions used for data analysis
from typing import List, Union

def get_average(data: List[Union[int, float]]) -> float:
    """
    Calculate the average of a list of numerical data.

    Args:
        data (List[Union[int, float]]): A list of numerical data.

    Returns:
        float: The average value of the data.
    """
    return sum(data) / len(data)

def get_deviation(data: List[Union[int, float]]) -> float:
    """
    Calculate the standard deviation of a list of numerical data.

    Args:
        data (List[Union[int, float]]): A list of numerical data.

    Returns:
        float: The standard deviation of the data.
    """
    S2 = 0.0

    avg = get_average(data)
    n = len(data)

    for point in data:
        S2 += (point - avg)**2

    return (S2 / (n - 1))**0.5

def get_low(data: List[Union[int, float]]) -> Union[int, float]:
    """
    Get the lowest value from a list of numerical data.

    Args:
        data (List[Union[int, float]]): A list of numerical data.

    Returns:
        Union[int, float]: The lowest value in the data.
    """
    return min(data)

def get_high(data: List[Union[int, float]]) -> Union[int, float]:
    """
    Get the highest value from a list of numerical data.

    Args:
        data (List[Union[int, float]]): A list of numerical data.

    Returns:
        Union[int, float]: The highest value in the data.
    """
    return max(data)
