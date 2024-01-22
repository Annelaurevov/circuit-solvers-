import random
from code.classes.House import House

seen = set()

class Node:
    def __init__(self, parent, house, position) -> None:
        self.parents = [parent]
        if parent is None:
            self.parents = []
        self.position = position
        self.house = house

    def __eq__(self, __value: object) -> bool:
        return self.position == __value.position
    
    def __hash__(self) -> int:
        return id(self.position)

    def __repr__(self) -> str:
        return f"Node op {self.position}"

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

    if not Node(node, node.house, (x+1, y)) in node.parents:
        options.append(Node(node, node.house, (x+1, y)))

    if not Node(node, node.house, (x-1, y)) in node.parents:
        options.append(Node(node, node.house, (x-1, y)))

    if not Node(node, node.house, (x, y+1)) in node.parents:
        options.append(Node(node, node.house, (x, y+1)))

    if not Node(node, node.house, (x, y-1)) in node.parents:
            options.append(Node(node, node.house, (x, y-1)))


    if Node(node, node.house, battery.position) in options:
        return Node(node, node.house, battery.position)

    weights = [1 / heuristic(battery, node) for node in options]
    weights = []
    best_dist = min(heuristic(battery, node) for node in options)
    for node in options:
        if heuristic(battery, node) == best_dist:
            weights.append(1)
        else:
            weights.append(0)

    return random.choices(options, weights)[0]


def run_alg(grid):
    battery = grid.batteries[0]
    for battery in grid.batteries:
        nodes = {}
        nodes2 = []

        houses = battery.houses
        for house in houses:
            house.path = [house.position]
            nodes[house] = Node(None, house, house.position)
            nodes2.append(Node(None, house, house.position))
        
        while len(nodes2) != 1:
            len(nodes2)
            node = nodes2.pop(0)
            house = node.house
            new_node = choose_direction(battery, node)
            house.path.append(new_node.position)
            if not new_node in seen:
                nodes2.append(new_node)
                seen.add(new_node)
            else:
                for node in seen:
                    if node == new_node:

                        node.parents.append(new_node)
                        break
    
    # stack = [nodes2.pop(0)]
    # while stack:
    #     #print(node.position, node.house.id)
    #     node = stack.pop(0)
    #     house = node.house
    #     house.path.append(node.position)
    #     print(len(node.parents))
    #     for parent_node in node.parents:
    #         stack.append(parent_node)
    


    # while len(nodes) != 1:
    #     print(len(nodes))
    #     for house, node in nodes.items():
    #         new_node = choose_direction(battery, node)
    #         print(f"House {house.id} goes to {new_node.position}")
    #         is_in = False
    #         for seen_node in seen:
                
    #             if new_node == seen_node:
    #                 seen_node.parents.append(new_node)
    #                 nodes.pop(house)
    #                 is_in = True
    #         if is_in:
    #             break

    #         seen.add(new_node)
    #         nodes[house] = new_node


    # print(nodes.items())
    # house, startnode = list(nodes.items())[0]
    # stack = [startnode]
    # while stack:
    #     node = stack.pop()
    #     print(node.house.id, node.position)
    #     house = node.house
    #     house.path.append(node.position)
    #     for parent in node.parents:
    #         stack.append(parent)

