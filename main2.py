from code.classes.Grid import Grid
from code.classes.House import House
from code.classes.Battery import Battery
from itertools import permutations

def distance(object1, object2):
    "Returns the distance between two objects"
    x1, y1 = object1.position
    x2, y2 = object2.position
    return abs(x1-x2) + abs(y1 - y2)


def fill_grid(grid, house_id):
    if house_id == len(grid.houses):
        return grid
    house = grid.houses[house_id]
    sorted_batteries = grid.batteries.copy()
    sorted_batteries.sort(key=lambda x: distance(house, x))
    for battery in sorted_batteries:
        if battery.can_add(house):
            print(f"house {house.id} connected to battery {battery.id}")
            battery.add(house)
            if fill_grid(grid, house_id+1):
                return grid
            print("Backtracking")
            battery.remove(house)
    # print("Backtracking")
    # battery.remove(house)


def switch2(grid):
    n = len(grid.houses)
    changes = False
    for i in range(n-2):
        house1 = grid.houses[i]
        for j in range(i+1, n-1):
            house2 = grid.houses[j]
            if house1.battery == house2.battery:
                continue
            old_cost = grid.calc_costs()
            battery1 = house1.battery
            battery2 = house2.battery

            battery1.remove(house1)
            battery2.remove(house2)

            if battery2.can_add(house1) and battery1.can_add(house2):
                battery1.add(house2)
                battery2.add(house1)
                if not grid.calc_costs() < old_cost:
                    battery1.remove(house2)
                    battery2.remove(house1)
                    battery1.add(house1)
                    battery2.add(house2)
                    
                else:
                    changes = True
                    print("New cost: ", grid.calc_costs())
            else:
                battery1.add(house1)
                battery2.add(house2)
    return changes


def switch3(grid):
    n = len(grid.houses)
    changes = False
    for i in range(n-2):
        house1 = grid.houses[i]
        for j in range(i+1, n-1):
            house2 = grid.houses[j]
            for k in range(j+1, n):

                best_option = []

                house3 = grid.houses[k]
                if house1.battery == house2.battery:
                    continue
                if house1.battery == house3.battery:
                    continue
                if house2.battery == house3.battery:
                    continue
                
                battery1 = house1.battery
                battery2 = house2.battery
                battery3 = house3.battery

                tot_cost = grid.calc_costs()

                #print(i,j,k)

                houses = [house1, house2, house3]
                battery1.remove(house1)
                battery2.remove(house2)
                battery3.remove(house3)
                for i, j, k in permutations([0,1,2]):


                    if battery1.can_add(houses[i]) and battery2.can_add(houses[j]) and battery3.can_add(houses[k]):
                        battery1.add(houses[i])
                        battery2.add(houses[j])
                        if not battery3.add(houses[k]):
                            print("Strange")
                        best_option.append((grid.calc_costs(), (i, j, k)))

                        battery1.remove(houses[i])
                        battery2.remove(houses[j])
                        battery3.remove(houses[k])


                i, j, k = min(best_option, key=lambda x: x[0])[1]
                new_cost = min(best_option, key=lambda x: x[0])[0]
                battery1.add(houses[i])
                battery2.add(houses[j])
                battery3.add(houses[k])
                if not (i==0 and j==1 and k==2):
                    changes = True
                    print("New costs", new_cost)
    return changes


district = 3

if __name__ == "__main__":
    grid = Grid(district)
    grid.load_houses(r"data/district_X/district-X_houses.csv".replace("X", str(district)))
    grid.load_batteries(r"data/district_X/district-X_batteries.csv".replace("X", str(district)))
    grid.houses.sort(key=lambda x: -x.capacity)
    fill_grid(grid, 0)
    print("Base solution found!")

    while switch2(grid):
        print("Switching 2s")

    while switch3(grid):
        print("New try")


    grid.write_out(r"data/outputs/output_district-X.json".replace("X", str(district)))

