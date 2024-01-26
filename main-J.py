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


choices = sys.argv[1:]

choices = arguments(choices)


if __name__ == "__main__":

    district = choices.district

    
    if choices.help:
        print(choices.help_message)
        sys.exit()

    grid = Grid(district)
    # grid.load_houses(r"data/district_X/district-X_houses.csv".replace("X", str(district)))
    # grid.load_batteries(r"data/district_X/district-X_batteries.csv".replace("X", str(district)))


    if choices.algorithm == 'random':
        lowest = 10e10
        grid_costs = []
        for i in range(choices.n):
            print_progress(i, choices.n)
            while not random_connect(grid):
                grid.reset()

            while choices.switches and switch_pairs(grid):
                pass
            if grid.calc_costs() < lowest:
                grid.write_out(r"data/outputs/output_district-X.json".replace("X", str(district)))
                lowest = grid.calc_costs()
            grid_costs.append(grid.calc_costs())
        if choices.hist:
                plot_histogram(district, choices.n, grid_costs)


    if choices.algorithm == 'greedy':
        fill_grid_greedy(grid)
        if choices.switches:
            while switch_pairs(grid):
                pass
        print("Finished -g")


    grid.read_in(f"data/outputs/output_district-{district}-random2.json")

    # battery = Battery((0,0), 10e10, -1)
    # for house in grid.houses:
    #     house.battery = battery
    #     battery.houses.append(house)
    #     house.path = [house.position]
    # grid.batteries = [battery]

 #     run_dijkstra(grid)
    # dijkstra_from_battery(grid)
    low = grid.calc_costs()
    while True:
        print(f"cost = {grid.calc_costs()}")
        grid = Grid(district)
        grid.read_in(f"data/outputs/output_district-{district}-random2.json")
        run_adv(grid)
        if grid.calc_costs() < low:
            low = grid.calc_costs()

            grid.write_out(f"data/outputs/output_district-{district}.json")

            if choices.visualize:
                visualize(district)



    for battery in grid.batteries:
        print(f"battery {battery.id} has #{len(battery.houses)} totalling capacity {sum(house.capacity for house in battery.houses)}")

    assert grid.is_filled()

    grid.write_out(f"data/outputs/output_district-{district}.json")

    if choices.visualize:
        visualize(district)
