from code.algoritmen.manhattan_path import manhattan_path as path
from code.algoritmen.manhattan_path import distance as battery_distance

def distance(other_house, cable):
    "Returns the distance between house and cable"
    x1, y1 = other_house.position
    x2, y2 = cable
    return abs(x1 - x2) + abs(y1 - y2)

def run_depth_first(grid):

    for battery in grid.batteries:
        best_configuration = None
        lowest_costs = float('inf')  # Initialize with positive infinity

        for main_house in battery.houses:
            remaining_houses = [house for house in battery.houses if house != main_house]

            for other_house in remaining_houses:
                # Calculate distance to battery
                distance_battery = battery_distance(battery, other_house)

                # Calculate distance to each cable in the main house's path
                for cable in main_house.path:
                    distance_cable = distance(other_house, cable)

                    # If cable is closer than battery, make a new path
                    if distance_cable < distance_battery:
                        cable_position = cable
                        other_house.path = path(other_house.position, cable_position)

            # Calculate costs
            costs = grid.calc_costs()

            # Update best configuration if the current one has lower costs
            if costs < lowest_costs:
                best_configuration = grid.copy()  # Assuming you have a method to copy the grid
                lowest_costs = costs

        # Apply the best configuration after exploring all possibilities for the current battery
        grid = best_configuration

    return grid
