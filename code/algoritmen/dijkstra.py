# File containing dijkstra algorithm

import heapq
from math import inf
from code.classes.Grid import Grid
from code.classes.Node import Node


def reset_node_grid(node_grid):
    """
    Sets all the nodes at distance infty
    """
    for row in node_grid:
        for node in row:
            node.parents = []
            node.value = inf


def dijkstra_from_battery(grid: Grid) -> None:
    """
    Runs the dijkstra algorithm from the battery
    """

    # Check all the batteries
    for battery in grid.batteries:
        houses = battery.houses.copy()

        # Make a node grid

        node_grid = [[Node(None, None, (x, y), inf)
                      for x in range(51)] for y in range(51)]
        targets = []

        x, y = battery.position
        battery_node = node_grid[y][x]

        # Start from battery
        seen = [battery_node]

        # Set targets
        for house in houses:
            x, y = house.position
            house.path = [house.position]
            targets.append(node_grid[y][x])

        # While not all targets found
        while targets:
            reset_node_grid(node_grid)
            for node in seen:
                node.value = 0

            queue = seen.copy()
            heapq.heapify(queue)

            while node not in targets:
                node = heapq.heappop(queue)

                x, y = node.position

                # Add neighbours to heapqueue
                if x > 0:
                    neighbour = node_grid[y][x-1]
                    if neighbour.value > node.value+1:
                        neighbour.value = node.value + 1
                        neighbour.parents = [node]
                        heapq.heappush(queue, neighbour)

                if y > 0:
                    neighbour = node_grid[y-1][x]
                    if neighbour.value > node.value+1:
                        neighbour.value = node.value + 1
                        neighbour.parents = [node]
                        heapq.heappush(queue, neighbour)

                if x < 50:
                    neighbour = node_grid[y][x+1]
                    if neighbour.value > node.value+1:
                        neighbour.value = node.value + 1
                        neighbour.parents = [node]
                        heapq.heappush(queue, neighbour)

                if y < 50:
                    neighbour = node_grid[y+1][x]
                    if neighbour.value > node.value+1:
                        neighbour.value = node.value + 1
                        neighbour.parents = [node]
                        heapq.heappush(queue, neighbour)

            # Find house corresponding to the node
            for house in houses:
                if house.position == node.position:
                    node.house = house
                    targets.remove(node)
                    seen.append(node)
                    break

            # Retrace path
            while node.parents:
                node = node.parents[-1]

                seen.append(node)
                house.path.append(node.position)
