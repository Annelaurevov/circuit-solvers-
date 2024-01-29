import sys
from code.classes.Grid import Grid
from starting.arguments import arguments, Choices
from starting.AlgorithmRunner import AlgorithmRunner
import time

def parse_command_line():
    """
    Parse command-line arguments and return Choices, district, and grid.
    """
    help = Choices()
    if len(sys.argv) == 1:
        print(help.help_message)
        sys.exit(1)

    choices = sys.argv[1:]
    choices = arguments(choices)
    district = choices.district
    grid = Grid(district)

    if choices.help:
        print(choices.help_message)
        sys.exit()

    return choices, district, grid


if __name__ == "__main__":
    choices, district, grid = parse_command_line()

    runner = AlgorithmRunner(grid, choices, district)


    start = time.time()
    times = []
    runs = 0
    while time.time() - start <= 60:
        runs += 1
        runner.run()
        runner.grid.reset()
        print(f"{time.time() - start = }")
    print(f"Time elapsed = {time.time() - start}\n runs = {runs}\n Average time = {(time.time() - start) / runs}")