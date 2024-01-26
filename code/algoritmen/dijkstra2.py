import heapq
from math import inf



class Node2:
    def __init__(self, parent, house, position, value) -> None:
        self.parents = [parent]
        if parent is None:
            self.parents = []
        self.position = position
        self.house = house
        self.value = value

    
    def __lt__(self, __value: object) -> bool:
        return self.value < __value.value


    def __repr__(self) -> str:
        return f"Node op {self.position}"




def get_directions2(node, value):
    x, y = node.position
    return [Node2(node, node.house, (x+1, y), value+1), Node2(node, node.house, (x-1, y), value+1),
            Node2(node, node.house, (x, y+1), value+1), Node2(node, node.house, (x, y-1), value+1)]


def distance2(object1, object2):
    "Returns the distance between two objects"
    x1, y1 = object1.position
    x2, y2 = object2.position
    return abs(x1-x2) + abs(y1 - y2)


def reset_node_grid(node_grid):
    for row in node_grid:
        for node in row:
            node.parents = []
            node.value = inf


def lowest_house_cost(grid, targets):
    lowest = 10e10
    lowest_house = None
    for node in targets:
        
        for house in grid.houses:
            if house.position == node.position:
                break
        
        if house.capacity < lowest:
            lowest = house.capacity
            lowest_house = house
    return lowest_house

def dijkstra_from_battery(grid):

    added_houses = []

    for battery in grid.batteries:

        houses_on_battery = []

        for house in grid.houses:
            if house not in added_houses:
                battery.houses.append(house)
        houses = battery.houses.copy()

        node_grid = [[Node2(None, None, (x, y), inf) for x in range(51)] for y in range(51)]
        targets = []

        x, y = battery.position
        battery_node = node_grid[y][x]
        seen = [battery_node]

        for house in houses:
            x, y = house.position
            # print(x, y)
            house.path = [house.position]
            targets.append(node_grid[y][x])





        while targets:
            # print(battery.capacity, lowest_house_cost(grid, targets).capacity)
            if not battery.can_add(lowest_house_cost(grid, targets)):
                break
            reset_node_grid(node_grid)

            

            for node in seen:
                node.value = 0

            queue = seen.copy() # Slow I know
            heapq.heapify(queue)

            not_found = True
            # print(targets)
            while not_found:
                node = heapq.heappop(queue)

                if node in targets:
                    for house in grid.houses:
                        if house.position == node.position:
                            break
                    if battery.can_add(house):
                        battery.add(house)
                        not_found = False
                        break
                x, y = node.position
                if x > 0:
                    neighbour = node_grid[y][x-1]
                    if neighbour.value > node.value+1:
                        neighbour.value = node.value + 1
                        neighbour.parents = [node]
                        heapq.heappush(queue, neighbour)
                if y > 0:
                    neighbour = node_grid[y-1][x]
                    if neighbour.value > node.value + 1:
                        neighbour.value = node.value + 1
                        neighbour.parents = [node]
                        heapq.heappush(queue, neighbour)
                if x < 50:
                    neighbour = node_grid[y][x+1]
                    if neighbour.value > node.value + 1:
                        neighbour.value = node.value + 1
                        neighbour.parents = [node]
                        heapq.heappush(queue, neighbour)
                if y < 50:
                    neighbour = node_grid[y+1][x]
                    if neighbour.value > node.value + 1:
                        neighbour.value = node.value + 1
                        neighbour.parents = [node]
                        heapq.heappush(queue, neighbour)


            for house in houses:
                if house.position == node.position:
                    node.house = house
                    targets.remove(node)
                    houses_on_battery.append(house)
                    added_houses.append(house)
                    seen.append(node)
                    break
            


            while node.parents:
                node = node.parents[0]

                seen.append(node)
                house.path.append(node.position)
        
        battery.houses = houses_on_battery
    for target in targets:
        for house in grid.houses:
            if house.position == target.position:
                break
        
        house.battery = None

