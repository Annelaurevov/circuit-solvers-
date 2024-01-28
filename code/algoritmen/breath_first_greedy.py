# File containing function with Algorithm that optimized filled grid in breath first greedy way

from code.algoritmen.manhattan_path import manhattan_path as path
from code.algoritmen.manhattan_path import keep_unique_paths
from code.algoritmen.manhattan_path import distance as battery_distance
from typing import List, Any, Tuple
import heapq
from itertools import combinations
from code.classes.House import House
from code.classes.Battery import Battery
from code.classes.Grid import Grid


def battery_costs(battery: Battery, grid: Grid) -> int:
    """
    Calculates the total costs for a battery section, including cable costs for connected houses.

    Args:
    - battery (Battery): The battery for which to calculate costs.
    - grid (Grid): The grid containing information about cable and battery costs.

    Returns:
    int: The total costs for the specified battery section.
    """
    total_costs = grid.battery_costs
    cable_costs = grid.cable_costs

    for house in battery.houses:
        total_costs += cable_costs * (len(house.path) - 1)

    return total_costs


def update_paths(main_houses: List[House], battery: Battery) -> None:
    """
    Updates the paths of non-main houses from the battery, choosing the shortest cable length between battery and main branch.

    Args:
    - main_houses (List[House]): List of main houses forming the main branch.
    - battery (Battery): The battery for which to update paths for non-main houses.

    Returns:
    None
    """
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


def add_config_costs(main_houses: List[House], battery: Battery, grid: Grid, config_heap: List[Tuple[int, Tuple[int, ...]]]) -> None:
    """
    Adds the configuration and its costs to the heap as a tuple.

    Args:
    - main_houses (List[House]): List of main houses forming the main branch.
    - battery (Battery): The battery for which to calculate costs.
    - grid (Grid): The grid containing information about cable and battery costs.
    - config_heap (List[Tuple[int, Tuple[int, ...]]]): The heap storing configurations and their costs.

    Returns:
    None
    """
    config = tuple(house.id for house in main_houses)
    costs = battery_costs(battery, grid)
    config_cost = (costs, config)
    heapq.heappush(config_heap, config_cost)


def find_cheapest(config_heap: List[Tuple[int, Tuple[int, ...]]]) -> Tuple[int, ...]:
    """
    Finds the cheapest configuration from the heap.

    Args:
    - config_heap (List[Tuple[int, Tuple[int, ...]]]): The heap storing configurations and their costs.

    Returns:
    Tuple[int, ...]: The tuple representing the cheapest configuration.
    """
    if not config_heap:
        return tuple()

    cheapest_config = heapq.heappop(config_heap)
    return cheapest_config


def generate_combinations(objects: List[Any], max_branches: int) -> List[Tuple[Any, ...]]:
    """
    Generates all combinations of objects up to the specified depth.

    Args:
    - objects (List[Any]): List of objects for which to generate combinations.
    - max_branches (int): The maximum depth for combinations.

    Returns:
    List[Tuple[Any, ...]]: The list of generated combinations.
    """
    all_combinations = []
    for r in range(1, max_branches + 1):
        combinations_at_depth = list(combinations(objects, r))
        all_combinations.extend(combinations_at_depth)
    return all_combinations


def print_progress(battery: Battery, cheapest_config: int) -> None:
    """
    Prints progress when the cheapest configuration for a battery is found.

    Args:
    - battery (Battery): The battery for which the progress is printed.
    - cheapest_config (int): The cheapest configuration information.

    Returns:
    None
    """
    if cheapest_config:
        print("Battery: " + str(battery.id + 1))
        print("Cheapest house configuration:", ' & '.join(str(id) for id in cheapest_config[1]))
        print("Price:", cheapest_config[0] + "\n")


def give_best_config(config_heap: List[Tuple[int, Tuple[int, ...]]], battery: Battery) -> None:
    """
    Finds the last best configuration and updates it accordingly.

    Args:
    - config_heap (List[Tuple[int, Tuple[int, ...]]]): The heap storing configurations and their costs.
    - battery (Battery): The battery for which to update the best configuration.

    Returns:
    None
    """
    cheapest_config = find_cheapest(config_heap)

    # print_progress(battery, cheapest_config)

    best_houses = [house for house in battery.houses if house.id in cheapest_config[1]]
    update_paths(best_houses, battery)


def breath_first_greedy(grid: Grid, max_branches: int) -> None:
    """
    Runs the algorithm using a breath-first greedy approach.

    Args:
    - grid (Grid): The grid containing information about houses, batteries, and costs.
    - max_branches (int): The maximum depth for generating combinations.

    Returns:
    None
    """
    for battery in grid.batteries:
        config_heap = []

        houses = generate_combinations(battery.houses, max_branches)

        for combination in houses:
            update_paths(combination, battery)
            keep_unique_paths(battery)
            add_config_costs(combination, battery, grid, config_heap)

        give_best_config(config_heap, battery)

        keep_unique_paths(battery)
