import heapq

class Node:
    def init(self, parent, position):
        self.position = position
        self.parent = None


def distance(object1, object2):
    "Returns the distance between two objects"
    x1, y1 = object1.position
    x2, y2 = object2.position
    return abs(x1-x2) + abs(y1 - y2)


# def cost(node, battery)




def run_A_star(grid):
    nodes = []
    battery = grid.batteries[0] # TODO for all batteries
    
    houses = battery.houses
    found = [False for house in houses]
    
    for house in houses:
        nodes.append(Node(None, house.position))

    for node in nodes:

    



