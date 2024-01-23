from code.algoritmen.manhattan_path import manhattan_path as path
from code.algoritmen.manhattan_path import distance as battery_distance
from typing import List, Any


def update_paths(main_houses, battery):
    for main_house in main_houses:
        main_house.path = path(main_house.position, battery.position)

    remaining_houses = [house for house in battery.houses if house not in main_houses]

    for other_house in remaining_houses:
        other_house.path = path(other_house.position, battery.position)
        len_battery_path = len(other_house.path)
        potential_paths = []

        for main_house_temp in main_houses:
            for cable in main_house_temp.path:
                len_cable_path = len(path(other_house.position, cable))

                if len_cable_path < len_battery_path:
                    new_path = path(other_house.position, cable)
                    potential_paths.append(new_path)
                else:
                    potential_paths.append(other_house.path)

        best_path = min(potential_paths, key=len)
        other_house.path = best_path


def give_best_config(best_configurations, battery):
    for best_configuration in best_configurations.values():
        main_houses = [house for house in battery.houses if house.id in best_configuration]
        update_paths(main_houses, battery)


def depth_first_search_recursive(main_houses, battery, grid, max_depth, current_depth, current_configuration):
    if current_depth > max_depth:
        return {}, float('inf')  

    best_configurations = {}
    lowest_costs = float('inf')

    for main_house in main_houses:
        remaining_main_houses = [house for house in main_houses if house != main_house]

        update_paths([main_house], battery)

        costs = grid.calc_costs()

        if costs < lowest_costs:
            best_configuration = current_configuration + [main_house.id]
            lowest_costs = costs

            remaining_best_configurations, remaining_lowest_costs = depth_first_search_recursive(
                remaining_main_houses, battery, grid, max_depth, current_depth + 1, best_configuration
            )

            if remaining_lowest_costs < lowest_costs:
                best_configurations = remaining_best_configurations
                lowest_costs = remaining_lowest_costs
            else:
                best_configurations[lowest_costs] = best_configuration

    return best_configurations, lowest_costs


def run_depth_first(grid, max_depth):
    for battery in grid.batteries:
        print(f"Exploring depth-first search for battery {battery.id} with max_depth={max_depth}...")
        best_configurations, lowest_costs = depth_first_search_recursive(
            battery.houses, battery, grid, max_depth, 1, []
        )
        give_best_config(best_configurations, battery)
        print(f"Best configurations for battery {battery.id}: {best_configurations}, Lowest costs: {lowest_costs}")

    print("real costs " + str(grid.calc_costs()))
