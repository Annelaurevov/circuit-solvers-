# File containing House class

from Typing import Tuple, List

class House:
    """
    Represents a house in the smart grid.

    Usage:
    - Initialize with __init__(position, capacity, house_id)

    Methods:
    - make_path(position): Makes a path to a certain position
    - get_path_length(): Returns the length of the path
    """
    def __init__(self, position: Tuple[int, int], capacity: float, house_id: int):
        """
        Initialize a House object.

        Args:
        - position (tuple[int, int]): Initial position of the house.
        - capacity (float): Capacity of the house.
        - house_id (int): Unique identifier for the house.
        """
        self.position: Tuple[int, int] = position
        self.capacity: float = capacity
        self.path: List[Tuple[int, int]] = [position]
        self.battery = None
        self.id: int = house_id


    def get_path_length(self) -> int:
        """
        Returns the length of the path.

        Returns:
        int: The length of the path.
        """
        return len(self.path) - 1
