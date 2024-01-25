import heapq
from math import inf

class Node:
    def __init__(self, parent, house, position) -> None:
        self.parents = [parent]
        if parent is None:
            self.parents = []
        self.position = position
        self.house = house


    def __eq__(self, __value: object) -> bool:
        return self.position == __value.position
    
    def __lt__(self, __value: object) -> bool:
        return False
    
    def __hash__(self) -> int:
        return id(self.position)

    def __repr__(self) -> str:
        return f"Node op {self.position}"



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
    
    def __hash__(self) -> int:
        return id(self.position)

    def __repr__(self) -> str:
        return f"Node op {self.position}"


def get_directions(node):
    x, y = node.position
    return [Node(node, node.house, (x+1, y)), Node(node, node.house, (x-1, y)),
            Node(node, node.house, (x, y+1)), Node(node, node.house, (x, y-1))]


def get_directions2(node, value):
    x, y = node.position
    return [Node2(node, node.house, (x+1, y), value+1), Node2(node, node.house, (x-1, y), value+1),
            Node2(node, node.house, (x, y+1), value+1), Node2(node, node.house, (x, y-1), value+1)]


def distance2(object1, object2):
    "Returns the distance between two objects"
    x1, y1 = object1.position
    x2, y2 = object2.position
    return abs(x1-x2) + abs(y1 - y2)


def run_dijkstra_on_house(seen, house):
    node = Node(None, house, house.position)
    nodes = [(0, node)]
    heapq.heapify(nodes)
    checked_points = []

    distance, new_node = heapq.heappop(nodes)
    iterations = 0
    while new_node not in seen:

        iterations += 1
        if new_node in checked_points:
            distance, new_node = heapq.heappop(nodes)
            continue

        # seen.append(new_node)
        checked_points.append(new_node)
        for direction in get_directions(new_node):
            if direction.position == house.position:
                continue
            heapq.heappush(nodes, (distance + 1, direction))
        distance, new_node = heapq.heappop(nodes)
        if distance2(new_node.house, new_node.house.battery) < distance:
            raise ValueError

    node = new_node
    while node.parents != []:
        house = node.house
        house.path.insert(1, node.position)
        seen.append(node)
        node = node.parents[0]




def run_dijkstra(grid):
    for battery in grid.batteries:
        seen = [Node(None, house, house.position) for house in battery.houses]
        seen = []
        seen.append(Node(None, battery, battery.position))
        houses = battery.houses.copy()
        houses.sort(key=lambda x: distance2(x, battery))
        for house in houses:
            house.path = [house.position]
            run_dijkstra_on_house(seen, house)

        print("solved battery")


def reset_node_grid(node_grid):
    for row in node_grid:
        for node in row:
            node.parents = []
            node.value = inf


def dijkstra_from_battery(grid):
    battery = grid.batteries[0]
    for battery in grid.batteries:
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
            

            for house in houses:
                if house.position == node.position:
                    node.house = house
                    targets.remove(node)
                    seen.append(node)
                    break
            
            while node.parents:
                node = node.parents[-1]
                
                seen.append(node)
                house.path.append(node.position)
