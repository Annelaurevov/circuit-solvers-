import sys

from code.classes.Grid import Grid
from code.classes.House import House
from code.classes.Battery import Battery

from code.algoritmen.fill_grid import fill_grid_greedy
from code.algoritmen.switch_pairs import switch_pairs

from code.vizualization.visualize import visualize


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
    fill_grid_greedy(grid)

    assert grid.is_filled()
    print("Cost = ", grid.calc_costs())

    while switch_pairs(grid):
        print("New cost: ", grid.calc_costs())

    assert grid.is_filled()

    grid.write_out(r"data/outputs/output_district-X.json".replace("X", str(district)))

    if needs_visualize:
        visualize(district)
