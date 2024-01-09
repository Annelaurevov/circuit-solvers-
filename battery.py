class battery():

    def __init__(self, full_capacity, capacity, id: int) -> None:
        self.full = full_capacity
        self.capacity = full_capacity
        self.list = []
        self.id = id

    def add(self, house: int) -> None:
        "Adds the house, after checking if there is enough capacity"
        # adds houses to the battery
        if self.capacity >= house.capacity:
            self.capacity -= house.capacity
            self.list.append(house)
            return True
        else:
            return False

    def remove(self) -> None:
        # removes house from stack
        for i, house in enumerate(self.list):
            list.pop(i)
            return
