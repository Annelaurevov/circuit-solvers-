# House Class

class House:
    def __init__(self, position, capacity):
        self.position = position
        self.capacity = capacity
        self.path = []
    
    def make_path(self, position):
        "Make path to other position"
        self.path = [self.position]
        posx, posy = position
        Hposx, Hposy = self.position

        while Hposx > posx:
            Hposx -= 1
            self.path.append((Hposx, Hposy))

        while Hposx < posx:
            Hposx += 1
            self.path.append((Hposx, Hposy))


        while Hposy > posy:
            Hposy -= 1
            self.path.append((Hposx, Hposy))

        while Hposy < posy:
            Hposy += 1
            self.path.append((Hposx, Hposy))
