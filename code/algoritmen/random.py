# File containing function with Algorithm that randomly connects 
    # houses and batteries

from code.algoritmen.manhattan_path import manhattan_path as path
import random


def random_connect(grid: object) -> bool:
    """
    Randomly connects houses to batteries in the grid.

    Args:
    - grid (object): The grid object representing the smart grid configuration.

    Returns:
    bool: True if the grid is completely filled, False otherwise.
    """
    houses = grid.houses.copy()
    while houses:
        house = houses.pop()
        batteries = [battery for battery in grid.batteries
                     if battery.can_add(house)]

        if not batteries:
            return False

        battery = random.choice(batteries)
        battery.add(house)
        house.path = path(house.position, battery.position)

    return True


def random_connect_till_connected(grid):
    """Keeps trying random configurations untill everything is connected"""
    while not random_connect(grid):
        grid.reset()
