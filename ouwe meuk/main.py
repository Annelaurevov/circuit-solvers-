from Grid import Grid
from House import House
from battery import Battery


def distance(object1, object2):
    "Returns the distance between two objects"
    x1, y1 = object1.position
    x2, y2 = object2.position
    return abs(x1-x2) + abs(y1 - y2)


if __name__ == "__main__":
    grid = Grid(1)
    grid.load_houses(r"Huizen&Batterijen/district_1/district-1_houses.csv")
    grid.load_batteries(r"Huizen&Batterijen/district_1/district-1_batteries.csv")
    to_be_placed = grid.houses.copy()

    while to_be_placed:
        house_list = []

        while to_be_placed:
            house = to_be_placed.pop()

            best_distance = 1e100
            best_battery = None

            for battery in grid.batteries:
                if not battery.can_add(house):
                    continue
                if distance(house, battery) < best_distance:
                    best_distance = distance(house, battery)
                    best_battery = battery
            if best_battery is None:

                grid.write_out("test.json")

            house_list.append((best_distance, best_battery, house))
            #print(min((distance(house,battery), battery, house) for battery in grid.batteries))

        house_list.sort(reverse=True, key=lambda x: x[0])
        while house_list:

            _, battery, house = house_list.pop()
            if battery is None:
                break
            if not battery.can_add(house):
                to_be_placed.append(house)
                print("oeps")
            else:
                battery.add(house)

    grid.write_out("test.json")
