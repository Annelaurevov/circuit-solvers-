class battery():

    def __init__(self, full_capacity, capacity) -> None:
        self.full = full_capacity
        self.capacity = full_capacity
        self.stack = []

    def add(self, house: int, capacity_house: float) -> None:
        # adds houses to the battery
        if self.capacity >= capacity_house:
            self.capacity = self.capacity - capacity_house
            self.stack.append(house)
            return True
        else:
            return False

    def pop(self, house: int) -> None:
        # removes house from stack
        if self.stack:
            return self.stack.pop(house)
        else:
            return None

    
