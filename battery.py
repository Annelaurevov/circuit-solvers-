class Battery():
    """
    Usage:

    add(self, house)
    remove(self, house)
    """

    def __init__(self, position, full_capacity, id: int) -> None:
        self.full = full_capacity
        self.capacity = full_capacity
        self.id = id
        self.position = position
        self.houses = []

    def can_add(self, house) -> bool:
        "Checks whether a house can be added"
        if self.capacity >= house.capacity:
            return True
        
        if self.capacity - house.capacity >= 1e-2:
            print("Rounding error")
            raise ValueError
        return False
    def add(self, house) -> bool:
        "Adds the house, after checking if there is enough capacity"
        # adds houses to the battery
        if self.capacity >= house.capacity:
            self.capacity -= house.capacity
            house.make_path(self.position)
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
                self.capacity += house.capacity
                self.houses.pop(i)
                return
        raise IndexError
            
