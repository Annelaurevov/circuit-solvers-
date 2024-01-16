# Algorithm that randomly connects houses and batteries
from code.algoritmen.manhattan_path import manhattan_path as path
import random

def random_connect(grid: object) -> bool:
    """
    Takes a grid and randomly connects a house to a battery
    Returns whether the grid is completely filled
    """

    houses = grid.houses.copy()
    while houses:
        house = houses.pop()
        batteries = grid.batteries.copy()
        batteries = [battery for battery in batteries if battery.can_add(house)]
        if batteries == []:
            return False
        battery = random.choice(batteries)
        battery.add(house)
        house.path = path(house.position, battery.position)
    return True
