import sys
import matplotlib.pyplot as plt

from code.classes.Grid import Grid
from code.classes.House import House
from code.classes.Battery import Battery

from code.algoritmen.fill_grid import fill_grid_greedy
from code.algoritmen.switch_pairs import switch_pairs
from code.algoritmen.random import random_connect

from code.data_analyse.data_analysis import get_average, get_deviation, get_high, get_low


from code.vizualization.visualize import visualize


def print_progress(n, max_n):
    characters = round(50 * n / max_n)

    print("Progress: ["+"#"*characters + " "*(50 - characters) + "]", end='\r')

if len(sys.argv) == 1:
    print("Usage: python main.py [-v] <district_number>")
    sys.exit(1)

arguments = sys.argv[1:]

needs_visualize = False
district = None

for arg in arguments:
    if arg == "-v":
        needs_visualize = True

    if "1" <= arg <= "3":
        district = int(arg)

if district is None:
    print("Usage: python main.py [-v] <district_number>")
    sys.exit(1)



if __name__ == "__main__":

    grid = Grid(district)
    grid.load_houses(r"data/district_X/district-X_houses.csv".replace("X", str(district)))
    grid.load_batteries(r"data/district_X/district-X_batteries.csv".replace("X", str(district)))
    

    grid_costs = []

    iterations = 1_000_00

    lowest = 61729

    for i in range(iterations):
        # print_progress(i, iterations)
        while not random_connect(grid):
            grid.reset()
        
        while switch_pairs(grid):
            #print("New cost: ", grid.calc_costs())
            pass

        if grid.calc_costs() < lowest:
            grid.write_out(r"data/outputs/output_district-X-random.json".replace("X", str(district)))
            #print("No fucking way")
            lowest = grid.calc_costs()
        grid_costs.append(grid.calc_costs())
    print("Finished")


    print("Lowest cost: ", get_low(grid_costs))
    plt.title(f"District: {district}\n n = {iterations}\nAverage = {get_average(grid_costs)} $\sigma$ = {get_deviation(grid_costs)}")
    plt.xlabel("grid cost")
    plt.hist(grid_costs)
    plt.show()
    
        # print(grid.calc_costs())
        # grid.write_out(r"data/random_connections/output_district-X_Y.json".replace("X", str(district)).replace("Y", str(grid.calc_costs())))

    # assert grid.is_filled()
    # print("Cost = ", grid.calc_costs())

    # grid.reset()
    # fill_grid_greedy(grid)

    # while switch_pairs(grid):
    #     print("New cost: ", grid.calc_costs())

    assert grid.is_filled()

    grid.write_out(r"data/outputs/output_district-X.json".replace("X", str(district)))

    if needs_visualize:
        visualize(district)
