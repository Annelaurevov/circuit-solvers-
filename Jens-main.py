import sys
import matplotlib.pyplot as plt

from code.classes.Grid import Grid
from code.classes.House import House
from code.classes.Battery import Battery

from code.algoritmen.fill_grid import fill_grid_greedy
from code.algoritmen.switch_pairs import switch_pairs
from code.algoritmen.random import random_connect

from code.algoritmen.not_named_yet import run_alg
from code.algoritmen.dijkstra import run_dijkstra, dijkstra_from_battery
from code.algoritmen.advanced_alg import run_adv


from code.data_analyse.data_analysis import get_average, get_deviation, get_high, get_low


from code.vizualization.visualize import visualize

from code.libs.arguments import arguments


import scipy.stats as stats
import numpy as np


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


from code.libs.tmp import Choices





if __name__ == "__main__":
    choices = Choices(sys.argv[1:])
    grid = choices.make_grid(sys.argv[1:])

    district = choices.district

    
    if choices.help:
        print(choices.help_message)
        sys.exit()

    choices.run()
    
    if choices.visualize:
        visualize(district)


