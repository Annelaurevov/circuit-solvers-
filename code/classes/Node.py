# File containing the node class
from typing_extensions import Self

class Node:
    """
    Node class to save points
    """
    def __init__(self, parent, house, position, value) -> None:
        self.parents = [parent]
        if parent is None:
            self.parents = []
        self.position = position
        self.house = house
        self.value = value


    def __lt__(self, __value: Self) -> bool:
        """
        Uses the less then on the value
        """
        return self.value < __value.value

    def __repr__(self) -> str:
        return f"Node op {self.position}"