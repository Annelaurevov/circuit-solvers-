from code.algoritmen.manhattan_path import manhattan_path as path
from code.algoritmen.manhattan_path import distance as battery_distance

def run_depth_first(grid):

    for battery in grid.batteries:
        best_configuration = 0
        lowest_costs = float('inf')

        for main_house in battery.houses:

            main_house.path = path(main_house.position, battery.position)

            remaining_houses = [house for house in battery.houses if house != main_house]

            for other_house in remaining_houses:
                # Calculate the lengths of the battery distance and each cable distance
                other_house.path = path(other_house.position, battery.position)
                len_battery_path = len(other_house.path)
                potential_paths = []

                # Calculate the length of each cable in the main house's path
                for cable in main_house.path:
                    len_cable_path = len(path(other_house.position, cable))

                    # If the cable path is shorter than the battery distance, add the new path to potential paths
                    if len_cable_path < len_battery_path:
                        new_path = path(other_house.position, cable)
                        potential_paths.append(new_path)
                        print("new path: " + str(len_cable_path) + " ipv " + str(len_battery_path))
                        print(new_path)
                    else:
                        # If not, add the original path to potential paths
                        potential_paths.append(other_house.path)

                # Choose the best path from potential paths based on the length
                best_path = min(potential_paths, key=len)

                # Update other_house.path with the best path
                other_house.path = best_path

            # Calculate costs
            costs = grid.calc_costs()
            print("costs = " + str(costs))

            # Update best configuration if the current one has lower costs
            if costs < lowest_costs:
                best_configuration = main_house.id
                lowest_costs = costs

        print("lowest costs = " + str(lowest_costs))

        # Apply the best configuration after exploring all possibilities for the current battery
        for main_house in battery.houses:
            if main_house.id == best_configuration:
                main_house.path = path(main_house.position, battery.position)

                remaining_houses = [house for house in battery.houses if house != main_house]

                for other_house in remaining_houses:
                    # Calculate the lengths of the battery distance and each cable distance
                    other_house.path = path(other_house.position, battery.position)
                    len_battery_path = len(other_house.path)
                    potential_paths = []

                    # Calculate the length of each cable in the main house's path
                    for cable in main_house.path:
                        len_cable_path = len(path(other_house.position, cable))

                        # If the cable path is shorter than the battery distance, add the new path to potential paths
                        if len_cable_path < len_battery_path:
                            new_path = path(other_house.position, cable)
                            potential_paths.append(new_path)
                            print("new path: " + str(len_cable_path) + " ipv " + str(len_battery_path))
                            print(new_path)
                        else:
                            # If not, add the original path to potential paths
                            potential_paths.append(other_house.path)

                    # Choose the best path from potential paths based on the length
                    best_path = min(potential_paths, key=len)

                    # Update other_house.path with the best path
                    other_house.path = best_path
