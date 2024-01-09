from House import House
from battery import Battery
import csv
import json

class Grid:
    """
    Usage:

    load_houses(house_file.csv)
    load_batteries(battery_file.csv)
    calc_costs(self)
    """

    def __init__(self, district):
        self.houses = []
        self.batteries = []
        self.size = 50
        self.cable_costs = 9
        self.battery_costs = 5000
        self.district = district


    def load_houses(self, file_path: str) -> None:
        """Load houses into class objects"""
        id = 0
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                print(row)
                x = int(row['x'])
                y = int(row['y'])
                capacity = float(row['maxoutput'])

                house = House((x, y), capacity, id)
                self.houses.append(house)
                id += 1


    def load_batteries(self, file_path: str) -> None:
        """Load batteries into battery objects"""
        id = 0
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                position = tuple(map(int, row['positie'].split(",")))
                capacity = float(row['capaciteit'])
                print(position)
                battery = Battery(position, capacity, id)
                self.batteries.append(battery)
                id += 1


    def calc_costs(self) -> int:
        """calculate total costs"""

        total_costs = 0

        for battery in self.batteries:
            total_costs += self.battery_costs

        for house in self.houses:
            for cable in house.path:
                total_costs += self.cable_costs

        return total_costs
    
    def write_out(self, path):
        "Write json file"

        with open(path, 'w', encoding='utf-8') as f:
            data = []
            
            district_data = dict()
            district_data["district"] = self.district
            district_data["costs-shared"] = self.calc_costs()

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
            print(data)
            json.dump(data, f, indent=4)




        
