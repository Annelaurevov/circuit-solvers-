from code.algoritmen.manhattan_path import manhattan_path as path
from code.algoritmen.manhattan_path import distance as battery_distance
from typing import List, Any, Tuple
import heapq
from itertools import combinations
from code.classes.House import House
from code.classes.Battery import Battery
from code.classes.Grid import Grid


def battery_costs(battery: Battery, grid: Grid) -> int:
    """
    Calculates costs per battery section
    """
    total_costs = grid.battery_costs
    cable_costs = grid.cable_costs

    for house in battery.houses:
        total_costs += cable_costs * (len(house.path) - 1)

    return total_costs


def update_paths(main_houses: List[House], battery: Battery) -> None:
    """
    Updates the path of the non-main houses from the battery to find the shortest cable length: battery or main branch
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
    Adds the configuration and its costs to the heap with a tuple
    """
    config = tuple(house.id for house in main_houses)
    costs = battery_costs(battery, grid)
    config_cost = (costs, config)
    heapq.heappush(config_heap, config_cost)


def find_cheapest(config_heap: List[Tuple[int, Tuple[int, ...]]]) -> Tuple[int, ...]:
    """
    Finds the cheapest configuration from the heap
    """
    if not config_heap:
        return tuple()

    cheapest_config = heapq.heappop(config_heap)
    return cheapest_config


def generate_combinations(objects: List[Any], max_branches: int) -> List[Tuple[Any, ...]]:
    """
    Generates all combinations of objects up to the specified depth
    """
    all_combinations = []
    for r in range(1, max_branches + 1):
        combinations_at_depth = list(combinations(objects, r))
        all_combinations.extend(combinations_at_depth)
    return all_combinations


def give_best_config(config_heap: List[Tuple[int, Tuple[int, ...]]], battery: Battery) -> None:
    """
    Finds the last best configuration and updates it accordingly
    """
    cheapest_config = find_cheapest(config_heap)

    if cheapest_config:
        print("Battery: " + str(battery.id + 1))
        print("Cheapest house configuration:", ', '.join(str(id) for id in cheapest_config[1]))
        print("Price:", cheapest_config[0])
        print("")

    best_houses = [house for house in battery.houses if house.id in cheapest_config[1]]
    update_paths(best_houses, battery)


def breath_first_greedy(grid: Grid, max_branches: int) -> None:
    """
    Runs the alogrithm
    """
    for battery in grid.batteries:
        config_heap = []
        
        houses = generate_combinations(battery.houses, max_branches)

        for combination in houses:
            update_paths(combination, battery)
            add_config_costs(combination, battery, grid, config_heap)

        give_best_config(config_heap, battery)



        
        
    








