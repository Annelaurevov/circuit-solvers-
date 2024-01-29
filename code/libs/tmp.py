import sys
from collections import deque
from code.classes.Grid import Grid

from code.algoritmen.random import random_connect_till_connected
from code.algoritmen.fill_grid import fill_grid_greedy
from code.algoritmen.switch_pairs import switch_pairs
from code.algoritmen.breath_first_greedy import breath_first_greedy
from code.algoritmen.dijkstra import dijkstra_from_battery

class Choices:
    def __init__(self, arguments):

        self.algorithms = deque()


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

        

        self.help_message = """
        Usage: python [option] [district]

        -g          Selects the greedy algorithm to fill grid
        -r          Selects the random algorithm to fill grid
        -i          Selects existing file output as input to fill grid, default: most recent

        -f <name>   Selects a different specified filename for '-i'
        -n <int>    Selects the amount of iterations for the random algorithm '-r'
        -s          Selects the switches algorithm after a filled grid

        -b          Selects the breath-first greedy algorithm after a filled grid
        -m <int>    Selects an amount <1-5> of main branches breath_first_greedy uses '-b'
        -d          Selects the Dijkstra algorithm after a filled grid

        -o <name>   Give name for the output file 
        
        -v          Visualizes the result with pygame
        -p          Shows a histogram of random iterations [-r -n <amount>]

        -h          Shows this message
        """

        self.add_arguments(arguments)



    def add_algorithm(self, algorithm):
        self.algorithms.append(algorithm)

    def run(self):
        while self.algorithms:
            algorithm = self.algorithms.popleft()
            algorithm(self.grid)
        
        self.grid.write_out(f"data/outputs/output_district-{self.district}.json")


    def make_grid(self, args) -> Grid:
        district = args[-1]
        try:
            district = int(district)
            self.district = district
        except ValueError:
            print(self.help_message)
            return None

        self.grid = Grid(district)
        if "-i" in args:
            if args.index("-i") < len(args) - 1 and args[args.index("-i") + 1] == "-f":

                filename = "-" + args[args.index("-f") + 1]
                self.grid.read_in(f"data/outputs/output_district-{self.district}{filename}.json")
            self.grid.read_in(f"data/outputs/output_district-{self.district}.json")
            return self.grid

        self.grid.load_batteries(f"data/district_{self.district}/district-{self.district}_batteries.csv")
        self.grid.load_houses(f"data/district_{self.district}/district-{self.district}_houses.csv")

        return self.grid


    def add_arguments(self, args) -> None:

        if "-h" in args:
            print(self.help_message)
            sys.exit()


        if args.count("-r") + args.count("-g") + args.count("-i") != 1:
            print("Exactly one of -r -g or -i can be used!")
            print(self.help_message)

        if "-g" in args:
            self.add_algorithm(fill_grid_greedy)

        if "-r" in args:
            if "-n" in args:
                iterations = args[args.index("-n") + 1]
                for _ in range(int(iterations)):
                    if "-s" in args:
                        self.add_algorithm(random_connect_till_connected)
                        self.add_algorithm(switch_pairs)
                    else:
                        self.add_algorithm(random_connect_till_connected)
            else:
                self.add_algorithm(random_connect_till_connected)
                if "-s" in args:
                    self.add_algorithm(switch_pairs)



        if "-s" in args:
            self.add_algorithm(switch_pairs)

        if "-b" in args and "-d" in args:
            raise SyntaxError("Choose one of -b or -d or none")

        if "-b" in args:
            m = 1
            if "-m" in args:
                main_branches = args[args.index("-m") + 1]

                m = int(main_branches)
                assert 1 <= m <= 5, "Number of branches should be between 1 and 5."

            self.add_algorithm(lambda grid: breath_first_greedy(grid, m))

        if "-d" in args:
            self.add_algorithm(dijkstra_from_battery)

        # if "-o" in args:
        #     choices.output = args[args.index("-o") + 1]

        if "-v" in args:
            self.visualize = True

        # if "-c" in args:
        #     choices.csv = True

        # try:
        #     if "-h" not in args:
        #         choices.district = int(args[-1])
        # except ValueError:
        #     raise ValueError
