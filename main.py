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


def print_progress(n: int, max_n: int) -> None:
    """
    Print progress bar for itarations during random algorithm
    """
    characters = round(50 * n / max_n)
    print(f"Progress: [{'#' * characters}{' ' * (50 - characters)}]", end='\r')


def plot_histogram(district: int, iterations: int, grid_costs: List[float]) -> None:
    """
    Plot histogram
    """
    plt.title(f"District: {district}\n n = {iterations}\nAverage = {round(np.mean(grid_costs), 2)} $\sigma$ = {round(np.std(grid_costs), 2)}")
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


def print_final_costs(costs: float) -> None:
    """
    Print final costs
    """
    text = f"Final cost {costs}"
    print("-" * len(text))
    print(text)
    print("-" * len(text))
    print()


def load_structures(grid: Grid, district: int) -> None:
    """
    Load structures into the grid
    """
    grid.load_houses(f"data/district_{district}/district-{district}_houses.csv")
    grid.load_batteries(f"data/district_{district}/district-{district}_batteries.csv")


def breath_or_dijkstra(grid: Grid, choices: Choices) -> None:
    """
    Apply either breath-first greedy or Dijkstra's algorithm based on choices
    Prints out desired text
    """
    if choices.breath:
        breath_first_greedy(grid, choices.m)
    elif choices.dijkstra:
        dijkstra_from_battery(grid)


def print_random_algo_text(choices: Choices) -> None:
    """
    Print random-related text
    """
    print("\n- filling grid with random algorithm")
    if choices.switches:
        print("- optimizing filled grid with switch pairs algorithm")

    if choices.n == 1:
        if choices.breath:
            print("- optimizing filled grid with breath first greedy")
            print(f"- using {choices.m} main {'branch' if choices.m == 1 else 'branches'}")
        elif choices.dijkstra:
            print("- optimizing filled grid with dijkstra")
    else:
        print("- using " + str(choices.n) + " iterations")
        
        if choices.breath:
            print("- optimizing each iteration with breath first greedy")
            print(f"- using {choices.m} main {'branch' if choices.m == 1 else 'branches'}")
        elif choices.dijkstra:
            print("- optimizing each iteration with dijkstra")
        
        print("- finding lowest cost")
        if choices.hist:
            print("- showing histogram plot")

    if len(choices.output) != 0:
        print("- saving output as: '" + choices.output + "'")


def print_greedy_algo_text(choices: Choices) -> None:
    """
    Print greedy-related text
    """
    print("\n- filling grid with greedy algorithm")

    if choices.switches:
        print("- optimizing grid with switch pairs algorithm")
        
    if choices.breath:
        print("- optimizing filled grid with breath first greedy")
        print(f"- using {choices.m} main {'branch' if choices.m == 1 else 'branches'}")
    elif choices.dijkstra:
        print("- optimizing filled grid with dijkstra")
        
    if len(choices.output) != 0:
        print("- saving output as: '" + choices.output + "'")


def print_input_algo_text(choices: Choices) -> None:
    """
    Print input-related text
    """
    print("\n- grid filled with existing output")
    if choices.filename:
        print("- using file: '" + choices.filename.lstrip("-") + "'")
    else:
        print("- using previous run output")

    if choices.switches:
        print("- optimizing grid with switch pairs algorithm")

    if choices.breath:
        print("- optimizing filled grid with breath first greedy")
        print(f"- using {choices.m} main {'branch' if choices.m == 1 else 'branches'}")
    elif choices.dijkstra:
        print("- optimizing filled grid with dijkstra")
        
    if len(choices.output) != 0:
        print("- saving output as: '" + choices.output + "'")


def start_random(grid: Grid, choices: Choices, district: int) -> None:
    """
    Sart with random algorithm
    """
    load_structures(grid, district)
    print_random_algo_text(choices)

    lowest = float('inf')
    grid_costs = []

    for i in range(choices.n):
        if choices.n != 1:
            print_progress(i, choices.n)

        while not random_connect(grid):
            grid.reset()

        while choices.switches and switch_pairs(grid):
            pass

        breath_or_dijkstra(grid, choices)

        current_cost = grid.calc_costs()
        heapq.heappush(grid_costs, current_cost)
        if current_cost < lowest:
            lowest = current_cost
            grid.write_out(f"data/outputs/output_district-{district}.json")

    if choices.hist:
        plot_histogram(district, choices.n, grid_costs)

    print_final_costs(grid_costs[0])



def start_greedy(grid: Grid, choices: Choices, district: int) -> None:
    """
    Start with greedy algorithm
    """
    load_structures(grid, district)
    fill_grid_greedy(grid)

    if choices.switches:
        while switch_pairs(grid):
            pass

    breath_or_dijkstra(grid, choices)

    grid.write_out(f"data/outputs/output_district-{district}.json")
    print_final_costs(grid.calc_costs())


def start_with_input(grid: Grid, choices: Choices, district: int) -> None:
    """
    Start with existing output as input for chosen
    """
    print_input_algo_text(choices)
    grid.read_in(f"data/outputs/output_district-{district}{choices.filename}.json")

    assert grid.is_filled()

    if choices.switches:
        while switch_pairs(grid):
            pass

    breath_or_dijkstra(grid, choices)

    grid.write_out(f"data/outputs/output_district-{district}.json")
    print_final_costs(grid.calc_costs())


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
    if choices.algorithm == 'random':
        start_random(grid, choices, district)

    if choices.algorithm == 'greedy':
        start_greedy(grid, choices, district)

    if choices.algorithm == 'file':
        start_with_input(grid, choices, district)

    assert grid.is_filled()

    if choices.visualize:
        visualize(district)

    if len(choices.output) != 0:
        grid.write_out(f"data/outputs/output_district-{district}-{choices.output}.json")


