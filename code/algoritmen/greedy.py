# File containing function with Algorithm that fills the grid in a greedy way

from code.algoritmen.manhattan_path import manhattan_path as path
from code.algoritmen.manhattan_path import distance


def fill_grid_greedy(grid):
    """
    Fill the grid using a greedy algorithm, prioritizing the
    battery with the shortest Manhattan distance.

    Args:
    - grid: The grid object.

    Notes:
    This function tries to fill the grid by sorting houses by
    capacity in decreasing order.
    It then iteratively assigns each house to the battery with the
    shortest Manhattan distance.

    If the greedy algorithm is unable to find a suitable configuration,
    it prints a message indicating that.

    """
    houses = grid.houses.copy()

    # Sort houses by capacity in decreasing order
    houses.sort(key=lambda x: -x.capacity)

    for house in houses:
        best_battery = min((battery for battery in grid.batteries
                           if battery.can_add(house)),
                           key=lambda battery: distance(house, battery))
        if best_battery is None:
            print("Greedy algorithm not suitable for the current scenario")

        if best_battery.can_add(house):
            best_battery.add(house)
            house.path = path(house.position, best_battery.position)
