import sys
from code.classes.Grid import Grid
from starting.arguments import arguments, Choices
from starting.AlgorithmRunner import AlgorithmRunner
from copy import deepcopy
from starting.interface import Interface
import time

def parse_command_line():
    """
    Parse command-line arguments and return Choices, district, and grid.
    """
    help = Choices()
    # if len(sys.argv) == 1:
    #     print(help.help_message)
    #     sys.exit(1)

    if len(sys.argv) == 1:
        choices = Interface()
        choices = choices.run()
        if not choices:
            print(help.help_message)
            sys.exit()

    else:
        choices = sys.argv[1:]
        choices = arguments(choices)

    district = choices.district

    grid = Grid(district)

    return choices, district, grid



if __name__ == "__main__":
    choices, district, grid = parse_command_line()
    start_grid = grid.copy()
    runner = AlgorithmRunner(grid, choices, district)
    runner.run()

