import sys
import csv
from typing import List
import matplotlib.pyplot as plt
import numpy as np

from code.classes.Grid import Grid
from code.classes.House import House
from code.classes.Battery import Battery
from code.libs.arguments import Choices
from code.vizualization.Visualizer import Visualizer

from code.algoritmen.fill_grid import fill_grid_greedy
from code.algoritmen.switch_pairs import switch_pairs
from code.algoritmen.random import random_connect
from code.algoritmen.breath_first_greedy import breath_first_greedy
from code.algoritmen.dijkstra import dijkstra_from_battery

from code.data_analyse.data_analysis import get_average, get_deviation, get_high, get_low
# from code.vizualization.visualize import visualize
from code.libs.arguments import arguments


class AlgorithmRunner:
    """
    Represents an algorithm runner for the smart grid.

    Usage:
    - Initialize with __init__(grid, choices, district)
    - Call run() to execute the algorithm based on the user's choices.

    Methods:
    - print_progress(n, max_n) -> None: Prints a progress bar for iterations during the random algorithm.
    - plot_histogram(grid_costs) -> None: Plots a histogram of grid costs.
    - print_algorithm_text() -> None: Prints text related to a specific algorithm type.
    - print_final_costs(costs) -> None: Prints final costs.
    - load_structures() -> None: Loads houses and batteries into the grid.
    - breath_or_dijkstra() -> None: Applies either breath-first greedy or Dijkstra's algorithm based on choices.
    - get_selected_options() -> str: Get the selected options for inclusion in the CSV header.
    - write_results_to_csv(data: List[List[float]]) -> None: Writes results to a CSV file.
    - start_random() -> None: Starts the random algorithm.
    - start_greedy() -> None: Starts the greedy algorithm.
    - start_with_input() -> None: Starts with existing output as input.
    - run() -> None: Final run function.
    """

    def __init__(self, grid: Grid, choices: Choices, district: int):
        """
        Initializes the AlgorithmRunner object.

        Args:
        - grid (Grid): The smart grid.
        - choices (Choices): User choices for algorithm options.
        - district (int): The district number.
        """
        self.grid = grid
        self.choices = choices
        self.district = district
        self.visualizer = Visualizer(district)


    def print_progress(self, n: int, max_n: int) -> None:
        """
        Prints a progress bar for iterations during the random algorithm.

        Args:
        - n (int): Current iteration.
        - max_n (int): Maximum number of iterations.
        """
        characters = round(50 * n / max_n)
        progress_bar = f"Progress: [{'#' * characters}{' ' * (50 - characters)}]"

        if n == max_n - 1:
            progress_bar = f"Progress: [{'#' * 50}]"
            progress_bar += "\n"
        
        sys.stdout.write('\r' + progress_bar)
        sys.stdout.flush()


    def plot_histogram(self, grid_costs: List[float]) -> None:
        """
        Plots a histogram of grid costs.

        Args:
        - grid_costs (List[float]): List of grid costs.
        """
        plt.title(
            f"District: {self.district}\n"
            f"n = {self.choices.n}\n"
            f"Average = {round(np.mean(grid_costs), 2)} "
            f"$\sigma$ = {round(np.std(grid_costs), 2)}"
        )

        plt.xlabel("grid cost")
        plt.hist(grid_costs, bins=100, density=True)

        sigma = np.std(grid_costs)
        mu = np.mean(grid_costs)
        x = np.linspace(min(grid_costs), max(grid_costs), 1000)
        y = 1 / (2 * np.pi * sigma ** 2) ** 0.5 * np.exp(-1 / 2 * (x - mu) ** 2 / sigma ** 2)

        print(min(grid_costs), max(grid_costs))
        print(f"{mu=}, {sigma=}")

        plt.plot(x, y)
        plt.show()


    def print_algorithm_text(self) -> None:
        """
        Prints text related to a specific algorithm type.
        """
        # Start with the filling of the grid
        if self.choices.algorithm not in ["greedy", "random"]:
            print("\n- filling grid with existing output")
            if self.choices.filename:
                print("- using file: '" + self.choices.filename.lstrip("-") + "'")
            else:
                print("- using previous run output")
        else:
            print(f"\n- filling grid with " + self.choices.algorithm + " algorithm")

        # Print specific text for random with iterations
        if self.choices.n != 1 and self.choices.algorithm == "random":
            print("- using " + str(self.choices.n) + " iterations")

            if self.choices.switches:
                print("- optimizing each iteration with switch pairs algorithm")

            if self.choices.breath:
                print("- optimizing each iteration with breath first greedy")
                print(f"- using {self.choices.m} main {'branch' if self.choices.m == 1 else 'branches'}")
            elif self.choices.dijkstra:
                print("- optimizing each iteration with dijkstra")
                
            print("- finding lowest cost")

            if self.choices.csv:
                print("- writing out csv file as: " + self.get_selected_options())

            if self.choices.hist:
                print("- showing histogram plot")


            if len(self.choices.output) != 0:
                print("- saving output as: '" + self.choices.output + "'")

            return 

        # Generic options
        if self.choices.switches:
            print("- optimizing filled grid with switch pairs algorithm")

        if self.choices.breath:
            print("- optimizing filled grid with breath first greedy")
            print(f"- using {self.choices.m} main {'branch' if self.choices.m == 1 else 'branches'}")
        elif self.choices.dijkstra:
            print("- optimizing filled grid with dijkstra")
            
        if len(self.choices.output) != 0:
            print("- saving output as: '" + self.choices.output + "'")


    def print_final_costs(self, costs: float) -> None:
        """
        Prints final costs.

        Args:
        - costs (float): The final cost value.
        """
        text = f"Final cost {costs}"
        print("-" * len(text))
        print(text)
        print("-" * len(text))
        print()


    def load_structures(self) -> None:
        """
        Loads houses and batteries into the grid.
        """
        self.grid.load_houses(f"data/district_{self.district}/district-{self.district}_houses.csv")
        self.grid.load_batteries(f"data/district_{self.district}/district-{self.district}_batteries.csv")


    def breath_or_dijkstra(self) -> None:
        """
        Applies either breath-first greedy or Dijkstra's algorithm based on choices.
        Prints out desired text.
        """
        if self.choices.breath:
            breath_first_greedy(self.grid, self.choices.m)
        elif self.choices.dijkstra:
            dijkstra_from_battery(self.grid)


    def get_selected_options(self) -> str:
        """
        Get the selected options for inclusion in the CSV header.

        Returns:
        - str: String containing the selected options concatenated.
        """
        selected_options = []

        if self.choices.switches:
            selected_options.append('SwitchPairs')
        if self.choices.breath:
            selected_options.append('BreathFirst')
        if self.choices.dijkstra:
            selected_options.append('Dijkstra')

        # If no specific algorithm is selected, use 'Random' in the header
        if not any([self.choices.switches, self.choices.breath, self.choices.dijkstra]):
            selected_options.append('Random')

        selected_options.append(str(self.choices.n))

        return "".join(selected_options)


    def write_results_to_csv(self, data: List[List[float]]) -> None:
        """
        Writes results to a CSV file.

        Args:
        - data (List[List[float]]): List containing data to be written to the CSV file.
        """
        header = self.get_selected_options()
        csv_filename = f"data/outputs/results_district-{self.district}-{header}.csv"

        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([header])
            for row in data:
                writer.writerow(row)


    def start_random(self) -> None:
        """
        Starts the random algorithm and writes results for each iteration to a CSV file.
        """
        self.print_algorithm_text()
        self.load_structures()

        lowest = float('inf')
        grid_costs = []

        for i in range(self.choices.n):
            if self.choices.n != 1:
                self.print_progress(i, self.choices.n)

            while not random_connect(self.grid):
                self.grid.reset()

            while self.choices.switches and switch_pairs(self.grid):
                pass

            self.breath_or_dijkstra()

            current_cost = self.grid.calc_costs()
            grid_costs.append([current_cost])

            if current_cost < lowest:
                lowest = current_cost
                self.grid.write_out(f"data/outputs/output_district-{self.district}.json")

        if self.choices.csv:
            self.write_results_to_csv(grid_costs)

        if self.choices.hist:
            self.plot_histogram(grid_costs)

        self.print_final_costs(lowest)


        def start_greedy(self) -> None:
            """
            Starts the greedy algorithm.
            """
            self.print_algorithm_text()
            self.load_structures()
            fill_grid_greedy(self.grid)

            if self.choices.switches:
                while switch_pairs(self.grid):
                    pass

            self.breath_or_dijkstra()

            self.grid.write_out(f"data/outputs/output_district-{self.district}.json")
            self.print_final_costs(self.grid.calc_costs())


        def start_with_input(self) -> None:
            """
            Starts with existing output as input.
            """
            self.print_algorithm_text()
            self.grid.read_in(f"data/outputs/output_district-{self.district}{self.choices.filename}.json")

            assert self.grid.is_filled()

            if self.choices.switches:
                while switch_pairs(self.grid):
                    pass

            self.breath_or_dijkstra()

            self.grid.write_out(f"data/outputs/output_district-{self.district}.json")
            self.print_final_costs(self.grid.calc_costs())


    def run(self) -> None:
        """
        Final run function.
        """
        if self.choices.algorithm == 'random':
            self.start_random()
        elif self.choices.algorithm == 'greedy':
            self.start_greedy()
        elif self.choices.algorithm == 'file':
            self.start_with_input()

        assert self.grid.is_filled()

        if self.choices.visualize:
            self.visualizer.run()

        if len(self.choices.output) != 0:
            self.grid.write_out(f"data/outputs/output_district-{self.district}-{self.choices.output}.json")
