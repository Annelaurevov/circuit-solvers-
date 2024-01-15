# File containing house Class

class House:
    """
    Usage:

    init(position, capacity, id: int)

    make_path(position)
    Makes path to certain position
    """
    def __init__(self, position: tuple[int, int], capacity: float, house_id: int):
        self.position = position
        self.capacity = capacity
        self.path = [position]
        self.battery = None
        self.id = house_id

    # def make_path(self, position: tuple[int, int]) -> None:
    #     "Make path to other position"
    #     self.path = [self.position]
    #     posx, posy = position
    #     Hposx, Hposy = self.position

    #     while Hposx > posx:
    #         Hposx -= 1
    #         self.path.append((Hposx, Hposy))

    #     while Hposx < posx:
    #         Hposx += 1
    #         self.path.append((Hposx, Hposy))


    #     while Hposy > posy:
    #         Hposy -= 1
    #         self.path.append((Hposx, Hposy))

    #     while Hposy < posy:
    #         Hposy += 1
    #         self.path.append((Hposx, Hposy))

    def get_path_length(self) -> int:
        """Returns the length of the path"""
        return len(self.path) - 1
