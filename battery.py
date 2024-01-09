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

    def add(self, house) -> bool:
        "Adds the house, after checking if there is enough capacity"
        # adds houses to the battery
        if self.capacity >= house.capacity:
            self.capacity -= house.capacity
            self.houses.append(house)
            return True
        else:
            return False

    def remove(self, house) -> None:
        "Removes the selected house"
        # removes house from stack
        for i, house.id in enumerate(self.list):
            self.houses.pop(i)
            return
            
