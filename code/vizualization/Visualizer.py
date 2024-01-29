# File containing Visualizer class
import pygame
import json
import sys

class Visualizer:
    def __init__(self, district_number: int):
        """
        Represents a visualization tool for a smart grid district.

        Usage:
        - Initialize with __init__(district_number)

        Methods:
        - initialize_pygame() -> None: Initialize the Pygame window.
        - transform_image(image, width, height) -> pygame.Surface: Transform the size of an image.
        - load_data() -> None: Load district data from a JSON file.
        - draw_selected_location(color, position) -> None: Draw a selected location on the screen.
        - draw_text(text, color, location) -> None: Draw text on the screen.
        - draw_legenda() -> None: Draw the legend on the screen.
        - get_on_screen_coordinates(x, y) -> [int, int]: Convert grid coordinates to on-screen coordinates.
        - draw_grid() -> None: Draw the grid on the screen.
        - draw_battery(color, location) -> None: Draw a battery on the screen.
        - draw_house(color, location) -> None: Draw a house on the screen.
        - draw_cables(color, cables) -> None: Draw cables on the screen.
        - check_battery(location) -> bool: Check if the mouse is over a battery.
        - calc_cost_battery(selected_battery) -> int: Calculate the cost of a selected battery.
        - calc_output_battery(selected_battery) -> float: Calculate the output of a selected battery.
        - check_which_battery(location) -> int: Check which battery the mouse is over.
        - draw_all() -> None: Draw the entire visualization.
        - draw_selected_battery(selected_battery, selected_battery_location) -> None: Draw the selected battery and its details.
        - run() -> None: Run the visualization loop.
        """
        self.district_number = district_number
        self.size = (800, 800)
        self.gridsize = (60, 60)

        # Calculate the size of each grid cell
        self.box_width = self.size[0] // self.gridsize[0]
        self.box_height = self.size[1] // self.gridsize[1]

        # Define color constants
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (220, 220, 220)
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 210, 0)
        self.PURPLE = (255, 0, 255)
        self.ORANGE = (255, 150, 0)
        self.colors = [self.BLUE, self.RED, self.GREEN, self.PURPLE, self.ORANGE]

        # Initialize attributes for Pygame
        self.screen = None
        self.font = None
        self.clock = None
        self.quit = False

        # Initialize data attributes
        self.data = None
        self.selected_battery = None
        self.selected_battery_location = None
        self.color_selected_battery = None

        # Load images and transform their size
        self.battery_image = self.transform_image(pygame.image.load(r'data/images/battery.png'), 2, 2)
        self.house_image = self.transform_image(pygame.image.load(r'data/images/house.png'), 1, 1)


    def initialize_pygame(self) -> None:
        """
        Initialize the Pygame window.
        """
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("SmartGrid")
        self.font = pygame.font.Font(None, 20)
        self.clock = pygame.time.Clock()


    def transform_image(self, image, width: int, height: int):
        """
        Transform the size of an image.

        Args:
        - image (pygame.Surface): The image to be resized.
        - width (int): The desired width of the image in grid cells.
        - height (int): The desired height of the image in grid cells.

        Returns:
        pygame.Surface: The resized image surface.
        """
        return pygame.transform.scale(image, (width * self.box_width, height * self.box_height))



    def load_data(self) -> None:
        """
        Load district data from a JSON file.
        """
        file_path = f"data/outputs/JSON/output_district-{self.district_number}.json"
        try:
            file = open(file_path, 'r')
            self.data = json.load(file)
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            sys.exit(1)


    def draw_selected_location(self, color, position) -> None:
        """
        Draw a selected location on the screen.

        Args:
        - color: The color of the selected location.
        - position: The position of the selected location.
        """
        pygame.draw.circle(self.screen, color, position, 10)


    def draw_text(self, text, color, location) -> None:
        """
        Draw text on the screen.

        Args:
        - text: The text to be displayed.
        - color: The color of the text.
        - location: The location where the text should be drawn.
        """
        starting_point = tuple(map(int, cables[0].split(",")))
        for end_point in cables[1:]:
            end_point = tuple(map(int, end_point.split(",")))

            pygame.draw.line(screen, color, get_on_screen_coordinates(*starting_point),
                            get_on_screen_coordinates(*end_point), width=2)

            starting_point = end_point
        text_location = [location[0] - 2 * self.box_height, location[1] - 2 * self.box_width]

        offsets = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        for offset in offsets:
            text_surface = self.font.render(text, True, color)
            self.screen.blit(text_surface, (text_location[0] + offset[0], text_location[1] + offset[1]))

        text_surface = self.font.render(text, True, self.WHITE)
        self.screen.blit(text_surface, text_location)


    def draw_legenda(self) -> None:
        """
        Draw the legend on the screen.
        """
        district_location = self.get_on_screen_coordinates(-2, -1)
        district = "District: " + str(self.data[0]["district"])
        
        total_costs_location = self.get_on_screen_coordinates(-1, -1)
        total_costs = "Total costs: " + str(self.data[0]["costs-own"])
        
        self.draw_text(district, self.BLACK, district_location)
        self.draw_text(total_costs, self.BLACK, total_costs_location)


    def get_on_screen_coordinates(self, x: int, y: int) -> [int, int]:
        """
        Convert grid coordinates to on-screen coordinates.

        Args:
        - x (int): X-coordinate in grid cells.
        - y (int): Y-coordinate in grid cells.

        Returns:
        [int, int]: The corresponding on-screen coordinates.
        """
        space_x = (self.gridsize[0] - 50) // 2 * self.box_width
        space_y = (self.gridsize[1] - 50) // 2 * self.box_width
        return (y * self.box_height + space_y, x * self.box_width + space_x)


    def draw_grid(self) -> None:
        """
        Draw the grid on the screen.
        """
        for i in range(self.gridsize[0] + 1):
            for j in range(self.gridsize[1] + 1):
                pygame.draw.line(self.screen, self.GRAY, [0, j * self.box_height], [self.size[0], j * self.box_height])
                pygame.draw.line(self.screen, self.GRAY, [i * self.box_width, 0], [i * self.box_width, self.size[1]])


    def draw_battery(self, color, location) -> None:
        """
        Draw a battery on the screen.

        Args:
        - color: The color of the battery.
        - location: The location of the battery.
        """
        battery_location = [location[0] - 1, location[1] - 2]
        battery_underlay_rect = pygame.Rect(self.get_on_screen_coordinates(*battery_location), (2 * self.box_width, 2 * self.box_height))
        
        pygame.draw.rect(self.screen, color, battery_underlay_rect)
        self.battery_image.set_alpha(130)
        self.screen.blit(self.battery_image, self.get_on_screen_coordinates(*battery_location))


    def draw_house(self, color, location) -> None:
        """
        Draw a house on the screen.

        Args:
        - color: The color of the house.
        - location: The location of the house.
        """
        house_location = [location[0] - 0.5, location[1] - 0.5]
        house_underlay_rect = pygame.Rect(self.get_on_screen_coordinates(*house_location), (self.box_width, self.box_height))
        pygame.draw.rect(self.screen, color, house_underlay_rect)
        self.house_image.set_alpha(130)
        self.screen.blit(self.house_image, self.get_on_screen_coordinates(*house_location))


    def draw_cables(self, color, cables) -> None:
        """
        Draw cables on the screen.

        Args:
        - color: The color of the cables.
        - cables: The coordinates of the cables.
        """
        starting_point = tuple(map(int, cables[0].split(",")))
        for end_point in cables[1:]:
            end_point = tuple(map(int, end_point.split(",")))
            pygame.draw.line(self.screen, color, self.get_on_screen_coordinates(*starting_point),
                            self.get_on_screen_coordinates(*end_point), width=2)
            starting_point = end_point


    def check_battery(self, location) -> bool:
        """
        Check if the mouse is over a battery.

        Args:
        - location: The mouse position.

        Returns:
        bool: True if the mouse is over a battery, False otherwise.
        """
        coordinates = [self.get_on_screen_coordinates(*map(int, location_data['location'].split(','))) for location_data in self.data[1:]]
        return any(
            coordinates[i][0] - 26 < location[0] <= coordinates[i][0] and
            coordinates[i][1] - 26 < location[1] <= coordinates[i][1]
            for i in range(len(coordinates))
        )


    def calc_cost_battery(self, selected_battery: int) -> int:
        """
        Calculate the cost of a selected battery.

        Args:
        - selected_battery (int): The selected battery.

        Returns:
        int: The total cost of the battery.
        """
        total_cost = 0
        total_cost += 5000
        for house_data in self.data[selected_battery]["houses"]:
            total_cost += 9 * (len(house_data['cables']) - 1)
        return total_cost


    def calc_output_battery(self, selected_battery: int) -> float:
        """
        Calculate the output of a selected battery.

        Args:
        - selected_battery (int): The selected battery.

        Returns:
        float: The total output of the battery.
        """
        total_output = 0
        for house_data in self.data[selected_battery]["houses"]:
            house_output = house_data.get("output", 0)
            total_output += float(house_output)
        return total_output


    def check_which_battery(self, location) -> int:
        """
        Check which battery the mouse is over.

        Args:
        - location: The mouse position.

        Returns:
        int: The index of the selected battery.
        """
        coordinates = [self.get_on_screen_coordinates(*map(int, location_data['location'].split(','))) for location_data in self.data[1:]]
        for i in range(len(coordinates)):
            if coordinates[i][0] - 26 < location[0] <= coordinates[i][0] and \
                    coordinates[i][1] - 26 < location[1] <= coordinates[i][1]:
                return i + 1


    def draw_all(self) -> None:
        """
        Draw the entire visualization.
        """
        self.draw_grid()
        self.draw_legenda()
        id = 0
        for location_data in self.data[1:]:
            color = self.colors[id]
            id += 1
            self.draw_battery(color, tuple(map(int, location_data['location'].split(','))))
            for house_data in location_data["houses"]:
                self.draw_house(color, tuple(map(int, house_data['location'].split(','))))
                self.draw_cables(color, house_data["cables"])


    def draw_selected_battery(self, selected_battery: int, selected_battery_location) -> None:
        """
        Draw the selected battery and its details.

        Args:
        - selected_battery (int): The selected battery.
        - selected_battery_location: The location of the selected battery.
        """
        self.draw_legenda()
        color = self.colors[selected_battery - 1]

        if isinstance(selected_battery_location, str):
            selected_battery_location = tuple(map(int, selected_battery_location.strip('()').split(',')))
        
        self.draw_battery(color, selected_battery_location)
        for house_data in self.data[selected_battery]["houses"]:
            house_location = tuple(map(int, house_data['location'].split(',')))
            self.draw_house(color, house_location)
            self.draw_cables(color, house_data["cables"])

        pygame.draw.circle(self.screen, self.color_selected_battery, self.mouse_position, 10)
        self.draw_text("Battery: " + str(selected_battery), self.BLACK, self.mouse_position)
        self.draw_text("ouput: " + str(int(self.calc_output_battery(selected_battery))), self.BLACK,
                       (self.mouse_position[0], self.mouse_position[1] + 13))
        self.draw_text("Cost: " + str(self.calc_cost_battery(selected_battery)), self.BLACK,
                       (self.mouse_position[0], self.mouse_position[1] + 26))


    def run(self):
        """
        Run the pygame isualization loop.
        """
        self.initialize_pygame()
        self.load_data()

        while not self.quit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit = True

            self.screen.fill(self.WHITE)
            self.draw_all()
            self.mouse_position = pygame.mouse.get_pos()
            self.draw_selected_location(self.BLACK, self.mouse_position)

            if self.check_battery(self.mouse_position):
                self.selected_battery = self.check_which_battery(self.mouse_position)
                self.selected_battery_location = self.data[self.selected_battery]["location"]
                self.color_selected_battery = self.colors[self.selected_battery - 1]
                self.screen.fill(self.WHITE)
                self.draw_grid()
                self.draw_selected_battery(self.selected_battery, self.selected_battery_location)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

