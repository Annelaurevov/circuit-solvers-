from Grid import Grid
from House import House
from battery import Battery

if __name__ == "__main__":
    grid = Grid(2)
    grid.load_houses(r"Huizen&Batterijen/district_2/district-2_houses.csv")
    grid.load_batteries(r"Huizen&Batterijen/district_2/district-2_batteries.csv")
    

    for house in grid.houses:
        for battery in grid.batteries[:2]:
            if battery.add(house):
                break
    grid.write_out("test.json")

