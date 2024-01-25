import sys
import matplotlib.pyplot as plt

from code.classes.Grid import Grid
from code.classes.House import House
from code.classes.Battery import Battery

from code.algoritmen.fill_grid import fill_grid_greedy
from code.algoritmen.switch_pairs import switch_pairs
from code.algoritmen.random import random_connect
from code.algoritmen.breath_first_greedy import breath_first_greedy

from code.data_analyse.data_analysis import get_average, get_deviation, get_high, get_low


from code.vizualization.visualize import visualize

from code.libs.arguments import arguments


import scipy.stats as stats
import numpy as np
import heapq


def print_progress(n, max_n):
    characters = round(50 * n / max_n)

    print("Progress: ["+"#"*characters + " "*(50 - characters) + "]", end='\r')


if len(sys.argv) == 1:
    print("Usage: python main.py [-v] <district_number>")
    sys.exit(1)


def plot_histogram(district, iterations, grid_costs):
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


def print_final_costs(costs):
    text = "Final cost " + str(costs)
    print("-" * len(text))
    print(text)
    print("-" * len(text))


def start_random(grid, choices, district):
    lowest = float('inf')
    grid_costs = []

    for i in range(choices.n):
        print_progress(i, choices.n)
        
        while not random_connect(grid):
            grid.reset()

        while choices.switches and switch_pairs(grid):
            pass
        
        if choices.breath:
            breath_first_greedy(grid, choices.m)

        current_cost = grid.calc_costs()
        heapq.heappush(grid_costs, current_cost)
        if current_cost < lowest:
            lowest = current_cost
            grid.write_out(r"data/outputs/output_district-X.json".replace("X", str(district)))

    if choices.hist:
        plot_histogram(district, choices.n, grid_costs)

    print_final_costs(grid_costs[0])


def start_greedy(grid, choices, district):
    fill_grid_greedy(grid)

    if choices.switches:
        while switch_pairs(grid):
            pass

    if choices.breath:
        breath_first_greedy(grid, choices.m)

    grid.write_out(r"data/outputs/output_district-X.json".replace("X", str(district)))
    print_final_costs(grid.calc_costs())



choices = sys.argv[1:]
choices = arguments(choices)


if __name__ == "__main__":

    district = choices.district
    
    if choices.help:
        print(choices.help_message)
        sys.exit()

    grid = Grid(district)
    grid.load_houses(r"data/district_X/district-X_houses.csv".replace("X", str(district)))
    grid.load_batteries(r"data/district_X/district-X_batteries.csv".replace("X", str(district)))
    
 
    if choices.algorithm == 'random':
        start_random(grid, choices, district)


    if choices.algorithm == 'greedy':
        start_greedy(grid, choices, district)

    assert grid.is_filled()

    if choices.visualize:
        visualize(district)
