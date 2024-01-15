from code.algoritmen.manhattan_path import manhattan_path as path
from code.algoritmen.manhattan_path import distance

def fill_grid_greedy(grid):
    """Tries to fill the grid with a greedy algorithm"""
    houses = grid.houses.copy()

    houses_connected = 0

    # Sort houses by capacity in decreasing order
    houses.sort(key=lambda x: -x.capacity)

    for house in houses:
        best_battery = min((battery for battery in grid.batteries if battery.can_add(house)),
                            key=lambda battery: distance(house, battery))
        if best_battery is None:
            print("oeps")

        if best_battery.can_add(house):
            best_battery.add(house)
            house.path = path(house.position, best_battery.position)
