class Choices:
    def __init__(self):
        self.algorithm = None
        self.visualize = False
        self.n = 1
        self.switches = False
        self.district = None


def arguments(args):
    choices = Choices()
    if "-r" in args and "-g" in args:
        raise SyntaxError
    if "-r" in args:
        choices.algorithm = "random"
        if "-n" in args:
            iterations = args(args.index("-n") + 1)
            try:
                choices.n = int(iterations)
            except ValueError:
                raise ValueError
    if "-g" in args:
        choices.algorithm = "greedy"

    if "-s" in args:
        choices.switches = True

    if "-v" in args:
        choices.visualize = True

    try:
        choices.district = int(args[-1])
    except ValueError:
        raise ValueError

    return choices
