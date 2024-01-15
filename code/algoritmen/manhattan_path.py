# file containing program to create manhattan path

def manhattan_path(begin: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Takes a begin point and an end point
    returns a shortest path according to the manhattan distance
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

def distance(object1, object2):
    "Returns the distance between two objects"
    x1, y1 = object1.position
    x2, y2 = object2.position
    return abs(x1-x2) + abs(y1 - y2)
