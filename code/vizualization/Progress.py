import sys
import time
import os

class Progress:
    def __init__(self):
        self.last_printed = -10e10
        self.progression = {}
        self.counters = 0

    def add_counter(self, maxval):
        """
        Adds a counter to the class
        Returns an id for the counter
        """
        self.progression[self.counters] = (0, maxval)
        self.counters += 1
        return self.counters - 1

    def update_counters(self, counter, value):
        """
        Updates the counters
        Input: counter_id, value
        """
        maxval = self.progression[counter][1]
        assert isinstance(maxval, int), "Update counters issue"
        self.progression[counter] = (value, maxval)


    def get_first_not_finished(self):
        for counter in range(self.counters):
            val, maxval = self.progression[counter]
            if val != maxval:
                return counter


    def print_counters(self, progress_id):
        """
        Prints the counters as progressbars
        optional set dt as time to update
        """
        # print(self.get_first_not_finished(), progress_id)

        if progress_id != self.get_first_not_finished():
            return False

        bars = round(os.get_terminal_size()[0]*2/3)
        bars -= 9
        bars -= len(str(self.counters))
        message = ""
        finished = True
        for counter in range(self.counters):
            val, maxval = self.progression[counter]
            assert isinstance(val, int) and isinstance(maxval, int)
            
            devision = (bars * val) // maxval
            # print(devision)
            assert isinstance(val, int) and isinstance(maxval, int) and isinstance(devision, int)
            message += f"Core {counter:{len(str(self.counters))}}: [{'▇'*devision}{'░'*(bars - devision)}] {val}/{maxval}\n"
            if val != maxval:
                finished = False


        if finished:
            self.last_printed = time.time()
            sys.stdout.write(message)
            sys.stdout.flush()
            return True

        self.last_printed = time.time()
        message += "\033[F" * (self.counters)
        sys.stdout.write(message)
        sys.stdout.flush()
        return False
