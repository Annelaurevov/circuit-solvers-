# File containing the visualization of the progress
import sys
import os


class Progress:
    """
    A class to track and display progress for multiple tasks using counters.

    Attributes:
        progression (dict): A dictionary holding the progress of each counter.
        counters (int): The total number of counters added.

    Methods:
        add_counter(maxval):
        Adds a new progress counter.

        update_counters(counter, value):
        Updates the specified counter with a new value.

        get_first_not_finished():
        Returns the ID of the first counter that hasn't finished.

        finished():
        Checks if all counters are finished.

        print_counters(progress_id):
        Prints the progress bars for all counters.
    """

    def __init__(self):
        """
        Initializes the Progress object with no counters.
        """

        self.progression = {}  # Dictionary to store progress counters
        self.counters = 0  # Total number of counters

    def add_counter(self, maxval):
        """
        Adds a new counter to track progress with a specified maximum value.

        Parameters:
            maxval (int):
            The maximum value of the new counter, representing 100% progress.

        Returns:
            int: The ID of the newly added counter.
        """
        # Initialize counter with 0 progress
        self.progression[self.counters] = (0, maxval)

        self.counters += 1  # Increment total counter count
        return self.counters - 1  # Return ID of the new counter

    def update_counters(self, counter, value):
        """
        Updates the value of a specified counter.

        Parameters:
            counter (int): The ID of the counter to update.
            value (int): The new value for the counter.

        Raises:
            AssertionError: If the max value of the counter is not an integer.
        """
        # Retrieve the max value of the counter
        maxval = self.progression[counter][1]

        assert isinstance(maxval, int), "Update counters issue"

        # Update the counter with the new value
        self.progression[counter] = (value, maxval)

    def get_first_not_finished(self):
        """
        Finds the first counter that has not reached its maximum value.

        Returns:
            int: The ID of the first counter that is not finished,
                 or None if all are finished.
        """
        for counter in range(self.counters):
            val, maxval = self.progression[counter]
            if val != maxval:
                return counter

    def finished(self):
        """
        Checks if all counters have reached their maximum values.

        Returns:
            bool: True if all counters are finished, False otherwise.
        """
        for counter in range(self.counters):
            val, maxval = self.progression[counter]
            if val != maxval:
                return False
        return True

    def print_counters(self, progress_id):
        """
        Prints the progress bars for all counters.
        Only updates the display if necessary
        to avoid rapid, unnecessary updates.

        Parameters:
            progress_id (int):
            The ID of the counter to check before printing.
            Printing only occurs if this counter is the first
            unfinished counter
            or if all counters are finished.

        Returns:
            bool: True if the counters were printed, False otherwise.
        """
        if progress_id != self.get_first_not_finished() and \
           not self.finished():
            return False

        # Calculate Usable width
        width = (os.get_terminal_size()[0] - 9 - len(str(self.counters)))

        # Use only 2/3
        bars = round(width * 2 / 3)

        message = ""
        for counter in range(self.counters):
            val, maxval = self.progression[counter]
            division = (bars * val) // maxval
            message += (f"Core {counter:{len(str(self.counters))}}: "
                        f"[{'▇' * division}{'░' * (bars - division)}] "
                        f"{val}/{maxval}\n")

        if self.finished():
            sys.stdout.write(message)
            sys.stdout.flush()
            return True

        # Move cursor up to overwrite previous progress bars
        message += "\033[F" * self.counters
        sys.stdout.write(message)
        sys.stdout.flush()
        return False
