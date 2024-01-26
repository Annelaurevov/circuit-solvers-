import sys
from typing import List
import matplotlib.pyplot as plt
import numpy as np
import heapq

from code.classes.Grid import Grid
from code.classes.House import House
from code.classes.Battery import Battery
from code.libs.arguments import Choices

from code.algoritmen.fill_grid import fill_grid_greedy
from code.algoritmen.switch_pairs import switch_pairs
from code.algoritmen.random import random_connect
from code.algoritmen.breath_first_greedy import breath_first_greedy
from code.algoritmen.dijkstra import dijkstra_from_battery

from code.data_analyse.data_analysis import get_average, get_deviation, get_high, get_low
from code.vizualization.visualize import visualize
from code.libs.arguments import arguments


class AlgorithmRunner:
    def __init__(self, grid: Grid, choices: Choices, district: int):
        self.grid = grid
        self.choices = choices
        self.district = district


    def print_progress(self, n: int, max_n: int) -> None:
        """
        Print progress bar for iterations during the random algorithm
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
        Plot histogram
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


    def print_final_costs(self, costs: float) -> None:
        """
        Print final costs
        """
        text = f"Final cost {costs}"
        print("-" * len(text))
        print(text)
        print("-" * len(text))
        print()


    def load_structures(self) -> None:
        """
        Load structures into the grid
        """
        self.grid.load_houses(f"data/district_{self.district}/district-{self.district}_houses.csv")
        self.grid.load_batteries(f"data/district_{self.district}/district-{self.district}_batteries.csv")


    def breath_or_dijkstra(self) -> None:
        """
        Apply either breath-first greedy or Dijkstra's algorithm based on choices
        Prints out desired text
        """
        if self.choices.breath:
            breath_first_greedy(self.grid, self.choices.m)
        elif self.choices.dijkstra:
            dijkstra_from_battery(self.grid)


    def print_algorithm_text(self) -> None:
        """
        Print text related to a specific algorithm type
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


    def start_random(self) -> None:
        """
        Start with random algorithm
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
            heapq.heappush(grid_costs, current_cost)
            if current_cost < lowest:
                lowest = current_cost
                self.grid.write_out(f"data/outputs/output_district-{self.district}.json")

        if self.choices.hist:
            self.plot_histogram(grid_costs)

        self.print_final_costs(grid_costs[0])

    def start_greedy(self) -> None:
        """
        Start with greedy algorithm
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
        Start with existing output as input for chosen
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


if __name__ == "__main__":
    # Check valid CLI input
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

    # Runs desired algorithm(s)
    runner = AlgorithmRunner(grid, choices, district)
    if choices.algorithm == 'random':
        runner.start_random()

    if choices.algorithm == 'greedy':
        runner.start_greedy()

    if choices.algorithm == 'file':
        runner.start_with_input()

    assert grid.is_filled()

    if choices.visualize:
        visualize(district)

    if len(choices.output) != 0:
        grid.write_out(f"data/outputs/output_district-{district}-{choices.output}.json")


