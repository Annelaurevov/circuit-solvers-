# File containing function to parse the command line operations

import sys
from code.classes.Grid import Grid
from code.IO.arguments import arguments, Choices
from code.IO.Interface import Interface
from typing import Tuple


def parse_command_line() -> Tuple[Grid, Choices]:
    """
    Parse command-line arguments and return a
    tuple containing the grid and choices.

    Returns:
    Tuple[Grid, Choices]: A tuple containing the smart grid and user choices.
    """
    help = Choices()

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

    return grid, choices
