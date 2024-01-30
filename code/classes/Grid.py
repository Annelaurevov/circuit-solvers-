# File containing Grid class

from Typing import Tuple, List
from code.classes.House import House
from code.classes.Battery import Battery
from copy import deepcopy

import csv
import json

class Grid:
    """
    Represents a smart grid.

    Usage:
    - Initialize with __init__(district)
    - Load houses using load_houses(filename)
    - Load batteries using load_batteries(filename)
    - Calculate costs using calc_costs()

    Methods:
    - load_houses(file_path: str) -> None: Load houses into class objects on grid.
    - load_batteries(file_path: str) -> None: Load batteries into battery objects on grid.
    - reset() -> None: Resets the grid by deleting paths, but keeping houses and batteries.
    - is_filled() -> bool: Checks if all houses are connected to batteries.
    - calc_costs() -> int: Calculates the total costs.
    - write_out(path: str) -> None: Writes the grid data to a JSON file.
    - read_in(path: str) -> None: Reads the grid data from a JSON file.
    """
    def __init__(self, district: int):
        """
        Initialize a Grid object.

        Args:
        - district (int): District number.
        """
        self.houses: List[House] = []
        self.batteries: List[Battery] = []
        self.size: int = 50
        self.cable_costs: int = 9
        self.battery_costs: int = 5000
        self.district: int = district


    def load_houses(self, file_path: str) -> None:
        """
        Load houses into class objects.

        Args:
        - file_path (str): Path to the CSV file containing house data.
        """
        house_id: int = 0
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                x: int = int(row['x'])
                y: int = int(row['y'])
                capacity: float = float(row['maxoutput'])

                house: House = House((x, y), capacity, house_id)
                self.houses.append(house)

                house_id += 1


    def load_batteries(self, file_path: str) -> None:
        """
        Load batteries into battery objects.

        Args:
        - file_path (str): Path to the CSV file containing battery data.
        """
        battery_id: int = 0
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                position: Tuple[int, int] = Tuple(map(int, row['positie'].split(",")))
                capacity: float = float(row['capaciteit'])
                battery: Battery = Battery(position, capacity, battery_id)
                self.batteries.append(battery)
                battery_id += 1


    def copy(self):


        return deepcopy(self)



    def reset(self) -> None:
        """
        Resets the grid by deleting house paths.
        """
        for battery in self.batteries:
            battery.capacity = battery.full
            battery.houses = []

        for house in self.houses:
            house.path = [house.position]
            house.battery = None


    def is_filled(self) -> bool:
        """
        Checks if all houses are connected to batteries.

        Returns:
        bool: True if all houses are connected, False otherwise.
        """
        for house in self.houses:
            if house.battery is None:
                return False
        return True


    def calc_costs(self) -> int:
        """
        Calculates the total costs.

        Returns:
        int: Total costs associated with the grid.
        """
        total_costs: int = 0

        for battery in self.batteries:
            total_costs += battery.cost

        for house in self.houses:
            total_costs += self.cable_costs * (len(house.path) - 1)

        return total_costs


    def write_out(self, path: str) -> None:
        """
        Writes the grid data to a JSON file.

        Args:
        - path (str): Path to the output JSON file.
        """
        with open(path, 'w', encoding='utf-8') as f:
            data: List[dict] = []

            district_data: dict = dict()
            district_data["district"] = self.district
            district_data["costs-own"] = self.calc_costs()

            data.append(district_data)

            for battery in self.batteries:
                battery_data: dict = dict()
                battery_data["location"] = f"{battery.position[0]},{battery.position[1]}"
                battery_data["capacity"] = battery.full

                houses: List[dict] = []
                for house in battery.houses:
                    house_data: dict = dict()
                    house_data["location"] = f"{house.position[0]},{house.position[1]}"
                    house_data["output"] = house.capacity
                    house_data["cables"] = [f"{x},{y}" for x, y in house.path]
                    houses.append(house_data)
                battery_data["houses"] = houses
                data.append(battery_data)

            json.dump(data, f, indent=4)


    def read_in(self, path: str) -> None:
        """
        Reads the grid data from a JSON file.

        Args:
        - path (str): Path to the input JSON file.
        """
        file = open(path, 'r')
        data = json.load(file)
        battery_id = 0
        house_id = 0
        for location_data in data[1:]:
            position = Tuple(map(int, location_data['location'].split(',')))
            capacity = location_data["capacity"]
            battery = Battery(position, capacity, battery_id)

            battery_id += 1

            for house_data in location_data["houses"]:
                position = Tuple(map(int, house_data['location'].split(',')))
                house = House(position, house_data["output"], house_id)
                house_id += 1
                house.path = []
                for cable in house_data["cables"]:
                    house.path.append(Tuple(map(int, cable.split(","))))

                house.battery = battery
                battery.houses.append(house)

                self.houses.append(house)
            self.batteries.append(battery)
