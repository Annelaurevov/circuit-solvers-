class Choices:
    def __init__(self):
        self.algorithm = None
        self.visualize = False
        self.hist = False
        self.n = 1
        self.switches = False
        self.breath = False
        self.m = 1
        self.district = None
        self.help = False

        self.help_message = """
        Usage: python [option] [district]

        -g          Selects the greedy algorithm
        -r          Selects the random algotithm
        -n          Selects how many times the random algorithm should be used
        -s          Selects the switches algorithm after greedy or random
        -b          Selects the breath first greedy algorithm after others
        -m          Selects how many main branches breath first greedy uses <1-5>
        -h          Shows this message
        -v          Visualizes the result
        -p          Shows histogram of iterations
        """


def arguments(args):
    choices = Choices()

    if "-h" in args:
        choices.help = True

    if "-r" in args and "-g" in args:
        raise SyntaxError
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
    if "-g" in args:
        choices.algorithm = "greedy"

    if "-s" in args:
        choices.switches = True

    if "-b" in args:
        choices.breath = True
        if "-m" in args:
            main_branches = args[args.index("-m") + 1]
            try:
                choices.m = int(main_branches)
                assert 1 <= choices.m <= 5, "Number of branches should be between 1 and 5."
            except ValueError:
                raise ValueError

    if "-v" in args:
        choices.visualize = True

    try:
        if "-h" not in args:
            choices.district = int(args[-1])
    except ValueError:
        raise ValueError

    return choices
