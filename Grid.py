import csv

class Grid:
    """
    Usage:

    load_houses(house_file.csv)
    load_batteries(battery_file.csv)
    calc_costs(self)
    """

    def __init__(self):
        self.houses = []
        self.batteries = []
        self.size = 50
        self.cable_costs = 9
        self.battery_costs = 5000


    def load_houses(self, file_path: str) -> None:
        """Load houses into class objects"""
        id = 0
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            next(reader)
            for row in reader:
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
            next(reader)
            for row in reader:
                position = row['positie']
                capacity = float(row['capaciteit'])

                battery = Battery(position, capacity, id)
                self.batteries.append(battery)
                id += 1


    def calc_costs(self) -> int:
        """calculate total costs"""
        
        total_costs = 0

        for battery in batteries:
            total_costs += battery_costs

        for house in houses:
            for cable in house.path:
                total_costs += cable_costs

        return total_costs




        
