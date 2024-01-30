# File containing Battery class

from typing import Tuple, List
from copy import deepcopy
from code.classes.House import House

class Battery:
    """
    Represents a battery in the smart grid.

    Usage:
    - Initialize with __init__(position, full_capacity, battery_id)

    Methods:
    - can_add(house) -> bool: Checks whether a house can be added.
    - add(house) -> bool: Adds a house to the battery if there is enough capacity.
    - remove(house) -> None: Removes a selected house from the battery.
    """
    def __init__(self, position: Tuple[int, int], full_capacity: float, battery_id: int):
        """
        Initialize a Battery object.

        Args:
        - position (tuple[int, int]): Initial position of the battery.
        - full_capacity (float): Full capacity of the battery.
        - battery_id (int): Unique identifier for the battery.
        """
        self.full: float = full_capacity
        self.capacity: float = full_capacity
        self.id: int = battery_id
        self.position: Tuple[int, int] = position
        self.cost: int = 5000
        self.houses: List[House] = []


    def can_add(self, house: House) -> bool:
        """
        Checks whether a house can be added to the battery.

        Args:
        - house (House): The house to be checked for addition.

        Returns:
        bool: True if the house can be added, False otherwise.
        """
        if self.capacity >= house.capacity:
            return True
        return False


    def add(self, house: House) -> bool:
        """
        Adds a house to the battery if there is enough capacity.

        Args:
        - house (House): The house to be added.

        Returns:
        bool: True if the house is added, False otherwise.
        """
        if self.capacity >= house.capacity:
            self.capacity -= house.capacity
            house.battery = self
            self.houses.append(house)
            return True
        return False


    def remove(self, house: House) -> None:
        """
        Removes a selected house from the battery.

        Args:
        - house (House): The house to be removed.

        Raises:
        IndexError: If the specified house is not found in the battery.
        """
        for i, house_n in enumerate(self.houses):
            if house == house_n:
                house.battery = None
                house.path = [house.position]
                self.capacity += house.capacity
                self.houses.pop(i)
                return
        raise IndexError


    def __repr__(self) -> str:
        """
        Returns a string representation of the battery.
        """
        return f"battery {self.id}"


    def copy(self):
        return deepcopy(self)
