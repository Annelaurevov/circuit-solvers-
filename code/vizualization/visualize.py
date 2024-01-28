import json
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (220, 220, 220)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 210, 0)
PURPLE = (255, 0, 255)
ORANGE = (255, 150, 0)
colors = [BLUE, RED, GREEN, PURPLE, ORANGE]

size = (800, 800)
gridsize = (60, 60)

box_width = size[0] // gridsize[0]
box_height = size[1] // gridsize[1]



def visualize(district_number: int) -> None:
    """
    Visualize the SmartGrid for a given district.

    Args:
    - district_number (int): The district number.
    """
    import pygame
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("SmartGrid")
    font = pygame.font.Font(None, 20)
    
    clock = pygame.time.Clock()

    battery = pygame.image.load(r'data/images/battery.png')
    battery = pygame.transform.scale(battery, (2 * box_width, 2 * box_height))

    house = pygame.image.load(r'data/images/house.png').convert_alpha()
    house = pygame.transform.scale(house, (1 * box_width, 1 * box_height))
    file_path = f"data/outputs/output_district-{district_number}.json"
    quit = False 

    def draw_selected_location(screen: pygame.Surface, color, position) -> None:
        """
        Draw a colored circle at a specified position on the screen.

        Args:
        - screen: Pygame screen surface.
        - color: RGB tuple representing the color.
        - position: Tuple (x, y) specifying the position.
        """
        pygame.draw.circle(screen, color, position, 10)  
    
    def draw_text(screen: pygame.Surface, text: str, color, location) -> None:
        """
        Draw text on the screen with a shadow effect.

        Args:
        - screen: Pygame screen surface.
        - text: The text to be displayed.
        - color: RGB tuple representing the color.
        - location: Tuple (x, y) specifying the position.
        """
        text_location = [location[0] - 2 * box_height, location[1] - 2 * box_width]

        offsets = [(1, 1), (-1, -1), (1, -1), (-1, 1)]

        for offset in offsets:
            text_surface = font.render(text, True, color)
            screen.blit(text_surface, (text_location[0] + offset[0], text_location[1] + offset[1]))

        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, text_location)


    def draw_legenda() -> None:
        """
        Draw legend information on the screen.
        """
        # draw district 
        district_location = get_on_screen_coordinates(-2,-1)
        district = "District: " + str(data[0]["district"])
        # draw total total cost of grid
        total_costs_location = get_on_screen_coordinates(-1, -1)
        total_costs = "Total costs: " + str(data[0]["costs-own"])

        draw_text(screen, district, BLACK, district_location)
        draw_text(screen, total_costs, BLACK, total_costs_location)
        
        # draw total of houses and batteries 
        

    def get_on_screen_coordinates(x: int, y: int) -> [int, int]:
        """
        Convert grid coordinates to on-screen pixel coordinates.

        Args:
        - x (int): X-coordinate in the grid.
        - y (int): Y-coordinate in the grid.
        """
        space_x = (gridsize[0] - 50) // 2 * box_width
        space_y = (gridsize[1] - 50) // 2 * box_width
        return (y * box_height + space_y, x * box_width + space_x)


    def draw_grid(size, gridsize) -> None:
        """
        Draw the grid lines on the screen.

        Args:
        - size: Tuple (width, height) representing the screen size.
        - gridsize: Tuple (rows, columns) representing the grid size.
        """
        for i in range(gridsize[0] + 1):
            for j in range(gridsize[1] + 1):
                pygame.draw.line(screen, GRAY, [0, j * box_height], [size[0], j * box_height])
                pygame.draw.line(screen, GRAY, [i * box_width, 0], [i * box_width, size[1]])


    def draw_battery(screen: pygame.Surface, color, location) -> None:
        """
        Draw a battery on the screen.

        Args:
        - screen: Pygame screen surface.
        - color: RGB tuple representing the color.
        - location: Tuple (x, y) specifying the position.
        """
        battery_location = [location[0] - 1, location[1] - 2]

        battery_underlay_rect = pygame.Rect(get_on_screen_coordinates(*battery_location), (2 * box_width, 2 * box_height))

        pygame.draw.rect(screen, color, battery_underlay_rect)

        battery.set_alpha(130)
        screen.blit(battery, get_on_screen_coordinates(*battery_location))
    
            
    def draw_house(screen: pygame.Surface, color, location) -> None:
        """
        Draw a house on the screen.

        Args:
        - screen: Pygame screen surface.
        - color: RGB tuple representing the color.
        - location: Tuple (x, y) specifying the position.
        """
        house_location = [location[0] - 0.5, location[1] - 0.5]

        house_underlay_rect = pygame.Rect(get_on_screen_coordinates(*house_location), (box_width, box_height))
        pygame.draw.rect(screen, color, house_underlay_rect)

        house.set_alpha(130)
        screen.blit(house, get_on_screen_coordinates(*house_location))


    def draw_cables(screen: pygame.Surface, color, cables) -> None:
        """
        Draw cables connecting houses to batteries on the screen.

        Args:
        - screen: Pygame screen surface.
        - color: RGB tuple representing the color.
        - cables: List of coordinates representing cable connections.
        """
        starting_point = tuple(map(int, cables[0].split(",")))
        for end_point in cables[1:]:
            end_point = tuple(map(int, end_point.split(",")))

            pygame.draw.line(screen, color, get_on_screen_coordinates(*starting_point),
                            get_on_screen_coordinates(*end_point), width=2)

            starting_point = end_point
    
    def check_battery(location) -> bool:
        """
        Check if the mouse is over a battery.

        Args:
        - location: Tuple (x, y) specifying the mouse position.

        Returns:
        bool: True if the mouse is over a battery, False otherwise.
        """
        coordinates = [get_on_screen_coordinates(*map(int, location_data['location'].split(','))) for location_data in data[1:]]
        return any(
            coordinates[i][0] - 26 < location[0] <= coordinates[i][0] and
            coordinates[i][1] - 26 < location[1] <= coordinates[i][1]
            for i in range(len(coordinates))
        )
    
    def calc_cost_battery(selected_battery: int) -> int:
        """
        Calculate the total cost associated with the selected battery.

        Args:
            selected_battery: The ID of the selected battery. 

        Notes:
            - This function computes the total cost, which includes a base cost and additional costs based on connected houses' cables.
            - The base cost is calculated as 5000 * 5, assuming a fixed price for each battery and a total of 5 batteries.
            - Additional costs are calculated based on the length of cables connected to each house. 
            Each unit length of cable incurs a cost of 9.
        """
        total_cost = 0

        # TODO: change if we try advanced 
        # total_costs = price batteries * amount of batteries
        total_cost += 5000 * 5

        for house_data in data[selected_battery]["houses"]:
            #print(len(house_data['cables']) - 1)
            total_cost += 9 *(len(house_data['cables']) - 1)

        return total_cost
    
    def calc_output_battery(selected_battery: int) -> float:
        """
        Calculate the total output power associated with the selected battery.

        Args:
            selected_battery: The ID of the selected battery.
        
        Notes:
            - This function computes the total output power provided by the selected battery based on connected houses.
            - It sums up the output power of each connected house.
        """
        total_output = 0
        
        for house_data in data[selected_battery]["houses"]:
            house_output = house_data.get("output", 0)  
            total_output += float(house_output)

        return total_output
        
    def check_which_battery(location) -> int:
        """
        Determine which battery the mouse is over.

        Args:
        - location: Tuple (x, y) specifying the mouse position.
        """
        coordinates = [get_on_screen_coordinates(*map(int, location_data['location'].split(','))) for location_data in data[1:]]
        for i in range(len(coordinates)):
            if coordinates[i][0] - 26 < location[0] <= coordinates[i][0] and \
                coordinates[i][1] - 26 < location[1] <= coordinates[i][1]:
                    return i+1
                    
    def draw_all(screen: pygame.Surface) -> None:
        """
        Draw the entire smart grid on the screen.

        Args:
        - screen: Pygame screen surface.
        """
        draw_grid(size, gridsize)
        
        draw_legenda()

        id = 0
        for location_data in data[1:]:
            color = colors[id]
            id += 1
            draw_battery(screen, color, tuple(map(int, location_data['location'].split(','))))
           
            for house_data in location_data["houses"]:
                draw_house(screen, color, tuple(map(int, house_data['location'].split(','))))
                draw_cables(screen, color, house_data["cables"])

        id = 0
        for location_data in data[1:]:
            color = colors[id]
            id += 1

    def draw_selected_battery(screen: pygame.Surface, selected_battery: int, selected_battery_location) -> None:
        """
        Draws the selected battery, associated houses, and information about the battery on the screen.

        Args:
            screen: Pygame screen surface to draw on.
            selected_battery: The ID of the selected battery.
            selected_battery_location: The location of the selected battery on the grid. 
                It can be either a tuple of integers (x, y) or a string representing a tuple.
        """
        
        draw_legenda()
        
        color = colors[selected_battery - 1]

        # Convert selected_battery_location to tuple if needed
        if isinstance(selected_battery_location, str):
            selected_battery_location = tuple(map(int, selected_battery_location.strip('()').split(',')))

        draw_battery(screen, color, selected_battery_location)

        for house_data in data[selected_battery]["houses"]:
            house_location = tuple(map(int, house_data['location'].split(',')))
            draw_house(screen, color, house_location)
            draw_cables(screen, color, house_data["cables"])
        
        pygame.draw.circle(screen, color_selected_battery, mouse_position, 10)  
        draw_text(screen, "Battery: " + str(selected_battery), BLACK, mouse_position)
        draw_text(screen, "ouput: " + str(int(calc_output_battery(selected_battery))), BLACK, (mouse_position[0], mouse_position[1]+13))
        draw_text(screen, "Cost: " + str(calc_cost_battery(selected_battery)), BLACK, (mouse_position[0], mouse_position[1]+ 26))

        
    try:
        file = open(file_path, 'r')
        data = json.load(file)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        sys.exit(1)
    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True

        screen.fill(WHITE)

        draw_all(screen)

        # Get the current mouse position
        mouse_position = pygame.mouse.get_pos()

        # Draw a red circle at the mouse position
        draw_selected_location(screen, BLACK, mouse_position)
        
        if check_battery(mouse_position):
            selected_battery = check_which_battery(mouse_position)
            selected_battery_location = data[selected_battery]["location"]
            color_selected_battery = colors[selected_battery - 1]
    
            screen.fill(WHITE)

            draw_grid(size, gridsize)

            draw_selected_battery(screen, selected_battery, selected_battery_location)

        pygame.display.flip()
        
        clock.tick(60)

    pygame.quit()

