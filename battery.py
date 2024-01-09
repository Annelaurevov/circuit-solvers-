class battery():
    """
    Usage:

    add(self, house)
    remove(self, house)
    """

    def __init__(self, full_capacity, capacity, id: int) -> None:
        self.full = full_capacity
        self.capacity = full_capacity
        self.list = []
        self.id = id

    def add(self, house_id: int) -> bool:
        "Adds the house, after checking if there is enough capacity"
        # adds houses to the battery
        if self.capacity >= house.capacity:
            self.capacity -= house.capacity
            self.list.append(house_id)
            return True
        else:
            return False

    def remove(self, house_id: int) -> None:
        # removes house from stack
        for i, house_id in enumerate(self.list):
            list.pop(i)
            return
            
