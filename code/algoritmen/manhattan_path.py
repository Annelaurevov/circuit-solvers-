# File containing functions that relate to path formation

def manhattan_path(begin: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Generate a shortest path according to the Manhattan distance between two points.

    Args:
    - begin (tuple[int, int]): The starting point coordinates.
    - end (tuple[int, int]): The ending point coordinates.

    Returns:
    list[tuple[int, int]]: The list of coordinates representing the Manhattan path.
    """
    current_x, current_y = begin
    end_x, end_y = end

    path = [(current_x, current_y)]

    while current_x < end_x:
        current_x += 1
        path.append((current_x, current_y))

    while current_x > end_x:
        current_x -= 1
        path.append((current_x, current_y))

    while current_y < end_y:
        current_y += 1
        path.append((current_x, current_y))

    while current_y > end_y:
        current_y -= 1
        path.append((current_x, current_y))

    return path


def distance(object1, object2) -> int:
    """
    Calculate the Manhattan distance between two objects.

    Args:
    - object1: The first object.
    - object2: The second object.

    Returns:
    int: The Manhattan distance between the two objects.
    """
    x1, y1 = object1.position
    x2, y2 = object2.position
    return abs(x1 - x2) + abs(y1 - y2)


def keep_unique_paths(battery) -> None:
    """
    Remove duplicate cables and connect unique paths for each house in a battery.

    Args:
    - battery: The battery object.
    """
    for house1 in battery.houses:
        for house2 in battery.houses:
            if house1 != house2:
                intersection = list(set(house1.path) & set(house2.path))
                if len(intersection) >= 2:
                    house2.path = house2.path[:(len(house2.path) - len(intersection) + 1)]

