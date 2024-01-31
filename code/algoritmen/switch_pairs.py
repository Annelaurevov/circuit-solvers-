# File containing function with Algorithm that switches pairs of houses

from code.algoritmen.manhattan_path import manhattan_path as path
from typing_extensions import TYPE_CHECKING

from code.classes.Grid import Grid


def switch_pairs(grid: Grid) -> bool:
    """
    Switch pairs of houses between batteries to optimize
        the grid configuration.

    Args:
    - grid (object): The grid object representing the smart grid configuration.

    Returns:
    bool: True if a switch was successful and improved the
        configuration, False otherwise.
    """
    switched = False

    # Create a copy of the houses list
    houses = grid.houses.copy()

    # Sort houses by the length of the path in decreasing order
    houses.sort(key=lambda x: len(x.path), reverse=True)

    n = len(houses)
    for i in range(n - 1):

        for j in range(i + 1, n):

            house1 = grid.houses[i]
            battery1 = house1.battery

            house2 = grid.houses[j]
            battery2 = house2.battery

            # Skip if houses are already connected to the same battery
            if battery1 == battery2:
                continue

            current_cost = grid.calc_costs()

            # Temporarily remove houses from their batteries for switching

            assert battery1 is not None
            assert battery2 is not None

            battery1.remove(house1)
            battery2.remove(house2)

            if battery1.can_add(house2) and battery2.can_add(house1):
                # Switch houses between batteries
                battery1.add(house2)
                battery2.add(house1)

                # Recalculate paths
                house1.path = path(house1.position, battery2.position)
                house2.path = path(house2.position, battery1.position)

                if grid.calc_costs() >= current_cost:
                    # If switching does not improve the configuration,
                    # revert the switch
                    battery1.remove(house2)
                    battery2.remove(house1)

                    battery1.add(house1)
                    battery2.add(house2)

                    house1.path = path(house1.position, battery1.position)
                    house2.path = path(house2.position, battery2.position)
                else:
                    switched = True
            else:
                # If switching is not possible, revert the temporary removal
                battery1.add(house1)
                battery2.add(house2)
                house1.path = path(house1.position, battery1.position)
                house2.path = path(house2.position, battery2.position)

    return switched
