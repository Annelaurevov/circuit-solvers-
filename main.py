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


from copy import deepcopy

if __name__ == "__main__":
    choices, district, grid = parse_command_line()
    start_grid = grid.copy()
    runner = AlgorithmRunner(grid, choices, district)
<<<<<<< HEAD
    runner.run()
=======
    start = time.time()
    runner.run()
    print("Time = ", time.time()-start)

    
    times = []
    runs = 0
    # while time.time() - start <= 60:
    #     runs += 1
    #     runner = AlgorithmRunner(start_grid.copy(), choices, district)
    #     runner.run()
    #     print(f"{time.time() - start = }")
    # print(f"Time elapsed = {time.time() - start}\n runs = {runs}\n Average time = {(time.time() - start) / runs}")
>>>>>>> 21a94e90e0702642a4db8080803c4ddf8f9fa53f
