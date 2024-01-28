import sys
from code.classes.Grid import Grid
from code.libs.arguments import arguments, Choices
from starting.AlgorithmRunner import AlgorithmRunner

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
    runner.run()