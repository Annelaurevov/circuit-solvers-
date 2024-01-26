# File containing Grid class
from code.classes.House import House
from code.classes.Battery import Battery

import csv
import json

class Grid:
    """
    Usage:

    __init__(district)

    load_houses(filename)
        loads houses into the grid

    load_batteries(filename)
        loads batteries into the grid

    calc_costs() -> float
        calculates the cost
        """

    def __init__(self, district: int):
        self.houses = []
        self.batteries = []
        self.size = 50
        self.cable_costs = 9
        self.battery_costs = 5000
        self.district = district


    def load_houses(self, file_path: str) -> None:
        """Load houses into class objects"""
        house_id = 0
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:

                x = int(row['x'])
                y = int(row['y'])
                capacity = float(row['maxoutput'])

                house = House((x, y), capacity, house_id)
                self.houses.append(house)

                house_id += 1


    def load_batteries(self, file_path: str) -> None:
        """Load batteries into battery objects"""
        battery_id = 0
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                position = tuple(map(int, row['positie'].split(",")))
                capacity = float(row['capaciteit'])
                battery = Battery(position, capacity, battery_id)
                self.batteries.append(battery)
                battery_id += 1


    def reset(self) -> None:
        """Resets the grid"""
        for battery in self.batteries:
            battery.capacity = battery.full
            battery.houses = []


        for house in self.houses:
            house.path = [house.position]
            house.battery = None


    def is_filled(self) -> bool:
        for house in self.houses:
            if house.battery is None:
                print(f"House {house.id} without battery")
                return False
            # if house.get_path_length() == 0:
            #     print(f"House {house.id} has no path")
            #     return False
        return True

    def calc_costs(self) -> int:
        """calculate total costs"""

        total_costs = 0

        total_costs += self.battery_costs * len(self.batteries)

        for house in self.houses:            
            total_costs += self.cable_costs*(len(house.path) - 1)

        return total_costs


    def write_out(self, path):
        """Write json file"""

        with open(path, 'w', encoding='utf-8') as f:
            data = []

            district_data = dict()
            district_data["district"] = self.district
            district_data["costs-own"] = self.calc_costs()

            data.append(district_data)


            for battery in self.batteries:
                battery_data = dict()
                battery_data["location"] = f"{battery.position[0]},{battery.position[1]}"
                battery_data["capacity"] = battery.full

                houses = []
                for house in battery.houses:
                    house_data = dict()
                    house_data["location"] = f"{house.position[0]},{house.position[1]}"
                    house_data["output"] = house.capacity
                    house_data["cables"] = [f"{x},{y}" for x,y in house.path]
                    houses.append(house_data)
                battery_data["houses"] = houses
                data.append(battery_data)

            json.dump(data, f, indent=4)


    def read_in(self, path):
        file = open(path, 'r')
        data = json.load(file)
        battery_id = 0
        house_id = 0
        for location_data in data[1:]:
            
            position = tuple(map(int, location_data['location'].split(',')))
            capacity = location_data["capacity"]
            battery = Battery(position, capacity, battery_id)
            
            battery_id += 1

            for house_data in location_data["houses"]:
                
                position = tuple(map(int, house_data['location'].split(',')))
                house = House(position, house_data["output"], house_id)
                house_id += 1
                house.path = []
                for cable in house_data["cables"]:
                    house.path.append(tuple(map(int, cable.split(","))))

                house.battery = battery
                battery.houses.append(house)

                self.houses.append(house)
            self.batteries.append(battery)
