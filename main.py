from Grid import Grid
from House import House
from battery import Battery

if __name__ == "__main__":
    grid = Grid(1)
    grid.load_houses(r"Huizen&Batterijen/district_1/district-1_houses.csv")
    grid.load_batteries(r"Huizen&Batterijen/district_1/district-1_batteries.csv")
    grid.write_out("test.json")


