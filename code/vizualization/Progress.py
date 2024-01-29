import sys

class Progress:
    def __init__(self):
        self.progression = {}
        self.counters = 0

    def add_counter(self, maxval):
        self.progression[self.counters] = (0, maxval)
        self.counters += 1
        return self.counters - 1
    
    def update_counters(self, counter, value):
        maxval = self.progression[counter][1]
        assert isinstance(maxval, int), "Update counters issue"
        self.progression[counter] = (value, maxval)

    def print_counters(self, bars = 50):
        message = ""
        finished = True
        for counter in range(self.counters):
            val, maxval = self.progression[counter]
            assert isinstance(val, int) and isinstance(maxval, int)
            
            devision = (bars * val) // maxval
            # print(devision)
            assert isinstance(val, int) and isinstance(maxval, int) and isinstance(devision, int)
            message += f"Progression {counter:{len(str(self.counters))}}: [{'#'*devision}{' '*(bars - devision)}] {val}/{maxval}\n"
            if val != maxval:
                finished = False
        


        if finished:
            sys.stdout.write(message)
            sys.stdout.flush()
            return True
        message += "\033[F" * (self.counters)
        sys.stdout.write(message)
        sys.stdout.flush()
        # print(message, end='\r')
        return False
