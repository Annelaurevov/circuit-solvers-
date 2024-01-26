from itertools import combinations
from random import sample
from code.classes.Battery import Battery
from code.algoritmen.dijkstra2 import dijkstra_from_battery



def run_adv(grid):

    battery_id = 0

    while True:
        houses = sample(grid.houses, 5)
        grid.batteries = []
        #print("Check combination")
        batteries = []
        for house in houses:
            # print(house.id)
            x, y = house.position
            battery = Battery((x-1, y), 1507, battery_id)
            batteries.append(battery)
            grid.batteries.append(battery)
            battery_id += 1
    
        #print("Running dijkstra")
        
        dijkstra_from_battery(grid)
        if grid.is_filled():
            return True