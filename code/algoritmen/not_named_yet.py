import random


seen = set()

class Node:
    def __init__(self, parent, position) -> None:
        self.parents = [parent]
        self.position = position

    def __eq__(self, __value: object) -> bool:
        return self.position == __value.position

def distance(object1, object2):
    "Returns the distance between two objects"
    x1, y1 = object1.position
    x2, y2 = object2.position
    return abs(x1-x2) + abs(y1 - y2)


def heuristic(battery, node):
    return distance(battery, node)


def choose_direction(battery, node):
    options = []
    x, y = node.position
    if not Node(node, (x+1, y)) in node.parents:
        options.append(Node(node, (x+1, y)))

    if not Node(node, (x-1, y)) in node.parents:
        options.append(Node(node, (x-1, y)))

    if not Node(node, (x, y+1)) in node.parents:
        options.append(Node(node, (x, y+1)))

    if not Node(node, (x, y-1)) in node.parents:
            options.append(Node(node, (x, y-1)))


    if Node(node, battery.position) in options:
        return Node(node, battery.position)

    weights = [1 / heuristic(battery, node) for node in options]

    return random.choices(options, weights)[0]


def run_alg(grid):
    battery = grid.batteries[0]

    nodes = {}

    houses = battery.houses
    for house in houses:
        nodes[house] = Node(None, house.position)

    while True:
        for house, node in nodes.items():
            new_node = choose_direction(battery, node)
            for seen_node in seen:
                is_in = False
                if new_node == seen_node:
                    seen_node.parents.append(new_node)
                    nodes.pop(house)
                    is_in = True
            if is_in:
                continue

            seen.add(new_node)
            nodes[house] = new_node
    

    
