# File containing the battery class

class Battery():
    """
    Usage:

    __init__(position, full_capacity, battery_id)
        
    can_add(house) -> bool
        checks whether a house can be added
    
    add(house) -> bool
        adds house if possible
    
    
    remove(house) -> removes house
    """

    def __init__(self, position: tuple[int, int], full_capacity: float, battery_id: int):
        self.full = full_capacity
        self.capacity = full_capacity
        self.id = battery_id
        self.position = position
        self.cost = 5000
        self.houses = []

    def can_add(self, house) -> bool:
        "Checks whether a house can be added"
        if self.capacity >= house.capacity:
            return True
        return False

    def add(self, house) -> bool:
        "Adds the house, after checking if there is enough capacity"
        # adds houses to the battery
        if self.capacity >= house.capacity:
            self.capacity -= house.capacity
            # house.make_path(self.position)
            house.battery = self
            self.houses.append(house)
            return True
        return False

    def remove(self, house) -> None:
        "Removes the selected house"
        # removes house from stack
        for i, house_n in enumerate(self.houses):
            if house == house_n:
                house.battery = None
                house.path = [house.position]
                self.capacity += house.capacity
                self.houses.pop(i)
                return
        raise IndexError

    def __repr__(self) -> str:
        return f"battery {self.id}"
