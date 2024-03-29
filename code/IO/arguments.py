# File containing class with Choices that are used for running main

import sys

MESSAGE = \
    """
    Usage: python [option] [district]

                No options and district will show a GUI,
                    prompting the user to select algorithms.

    -g          Selects the greedy algorithm to fill grid
    -r          Selects the random algorithm to fill grid
    -i          Selects existing file output as input to fill grid,
                    default: most recent

    -f <name>   Selects a different specified filename for '-i'
    -n <int>    Selects the amount of iterations for the random algorithm '-r'
    -s          Selects the switches algorithm after a filled grid

    -b          Selects the breath-first greedy algorithm after a filled grid
    -m <int>    Selects an amount <1-5> of main
                    branches that breath_first_greedy uses ('-b')
    -d          Selects the Dijkstra algorithm after a filled grid

    -o <name>   Give name for the output file

    -c          Saves csv file from random iterations in outputs/csv
    -v          Visualizes the result with pygame
    -p          Shows a histogram of random iterations [-r -n <amount>]

    -h          Shows this message
    """


class Choices:
    def __init__(self):
        self.algorithm = None
        self.filename = ""
        self.n = 1
        self.switches = False
        self.breath = False
        self.m = 1
        self.dijkstra = False
        self.hist = False
        self.visualize = False
        self.district = None
        self.output = ""
        self.csv = False
        self.help = False
        self.previous = False

        self.help_message = MESSAGE


def arguments(args):
    choices = Choices()

    if "-h" in args:
        print(choices.help_message)
        sys.exit()
        return

    if len(args) > 2:
        if args.count("-r") + args.count("-g") + args.count("-i") != 1:
            raise SyntaxError(
                "Exactly one of -r, -g, or -i should be selected")

    if "-g" in args:
        choices.algorithm = "greedy"

    if "-r" in args:
        choices.algorithm = "random"
        if "-n" in args:
            iterations = args[args.index("-n") + 1]
            try:
                choices.n = int(iterations)
            except ValueError:
                raise ValueError
            if "-p" in args:
                choices.hist = True

    if "-i" in args:
        choices.algorithm = "file"
        if args.index("-i") < len(args) - 1 and \
                args[args.index("-i") + 1] == "-f":
            choices.previous = False
            choices.filename = "-" + args[args.index("-f") + 1]

    if "-s" in args:
        choices.switches = True

    if "-b" in args and "-d" in args:
        raise SyntaxError("Choose one of -b or -d or none")

    if "-b" in args:
        choices.breath = True
        if "-m" in args:
            main_branches = args[args.index("-m") + 1]
            try:
                choices.m = int(main_branches)
                assert 1 <= choices.m <= 5, \
                    "Number of branches should be between 1 and 5."
            except ValueError:
                raise ValueError

    if "-d" in args:
        choices.dijkstra = True

    if "-o" in args:
        choices.output = args[args.index("-o") + 1]
        print(choices.output)

    if "-v" in args:
        choices.visualize = True

    if "-c" in args:
        choices.csv = True

    try:
        if "-h" not in args:
            choices.district = int(args[-1])
    except ValueError:
        raise ValueError

    return choices
