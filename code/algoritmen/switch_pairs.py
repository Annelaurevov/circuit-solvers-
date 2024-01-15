# Algorithm that switches pairs of houses
from code.algoritmen.manhattan_path import manhattan_path as path

def switch_pairs(grid: object) -> bool:
    """
    Takes a grid and switches connections if benifitial
    Returns whether a switch was succesfull
    """
    switched = False

    n = len(grid.houses)
    for i in range(n-1):

        for j in range(i+1, n):

            house1 = grid.houses[i]
            battery1 = house1.battery

            house2 = grid.houses[j]
            battery2 = house2.battery

            if battery1 == battery2:
                continue

            current_cost = grid.calc_costs()

            battery1.remove(house1)
            battery2.remove(house2)

            if battery1.can_add(house2) and battery2.can_add(house1):
                battery1.add(house2)
                battery2.add(house1)

                house1.path = path(house1.position, battery2.position)
                house2.path = path(house2.position, battery1.position)

                if grid.calc_costs() >= current_cost:

                    battery1.remove(house2)
                    battery2.remove(house1)

                    battery1.add(house1)
                    battery2.add(house2)

                    house1.path = path(house1.position, battery1.position)
                    house2.path = path(house2.position, battery2.position)
                else:
                    switched = True
            else:
                battery1.add(house1)
                battery2.add(house2)
                house1.path = path(house1.position, battery1.position)
                house2.path = path(house2.position, battery2.position)


    return switched
