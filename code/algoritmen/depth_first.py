from code.algoritmen.manhattan_path import manhattan_path as path
from code.algoritmen.manhattan_path import distance as battery_distance
from typing import List, Any
import heapq
from itertools import combinations


def run_depth_first(grid, max_branches):


    def battery_costs(battery, grid) -> int:
        """
        calculates costs per battery section
        """

        total_costs = grid.battery_costs
        cable_costs = grid.cable_costs

        for house in battery.houses:            
            total_costs += cable_costs*(len(house.path) - 1)

        return total_costs


    def update_paths(main_houses, battery):
        """
        updates the path of the non_main-houses from battery to find the shortest cable length: battery or main branch
        """

        for main_house in main_houses:
            main_house.path = path(main_house.position, battery.position)

        #print("Main Houses:")
        #for main_house in main_houses:
            #print(f"House {main_house.id} at position {main_house.position}")

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


    def add_config_costs(main_houses, battery, grid, config_heap):
        """
        Adds the configuration and its costs to the heap.
        """
        config = tuple(house.id for house in main_houses)
        costs = battery_costs(battery, grid)
        config_cost = (costs, config)
        heapq.heappush(config_heap, config_cost)



    def find_cheapest(config_heap):
        if not config_heap:
            return None

        cheapest_config = heapq.heappop(config_heap)
        return cheapest_config[1]



    def generate_combinations(objects, max_branches):
        all_combinations = []
        for r in range(1, max_branches + 1):
            combinations_at_depth = list(combinations(objects, r))
            all_combinations.extend(combinations_at_depth)
        return all_combinations


    for battery in grid.batteries:

        config_heap = []
        
        houses = generate_combinations(battery.houses, max_branches)

        for combination in houses:
            update_paths(combination, battery)
            add_config_costs(combination, battery, grid, config_heap)


        cheapest_config = find_cheapest(config_heap)
        print(cheapest_config)

        if cheapest_config:
            print("Cheapest Configuration:", cheapest_config)
            print("Price: " + str(config_heap[0][0]))

        best_houses = []

        for value in cheapest_config:
            for house in battery.houses:
                if value == house.id:
                    best_houses.append(house)

        if best_houses:
            update_paths(best_houses, battery)
            print("Houses updated")
        else:
            print("No matching houses found")
                
        update_paths(best_houses, battery)
        print("House updated")
        
    








