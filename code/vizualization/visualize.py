
import json
import sys

# if len(sys.argv) != 2:
#     print("Usage: python file.py <district_number>")
#     sys.exit(1)





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






def visualize(district_number: int):
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



    def draw_text(screen, text, color, location):
        text_location = [location[0] - 2 * box_height, location[1] - 2 * box_width]

        offsets = [(1, 1), (-1, -1), (1, -1), (-1, 1)]

        for offset in offsets:
            text_surface = font.render(text, True, color)
            screen.blit(text_surface, (text_location[0] + offset[0], text_location[1] + offset[1]))

        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, text_location)


    def draw_total_costs():
        total_costs_location = get_on_screen_coordinates(-1, -1)

        total_costs = "Total costs: " + str(data[0]["costs-own"])

        draw_text(screen, total_costs, BLACK, total_costs_location)


    def get_on_screen_coordinates(x, y):
        space_x = (gridsize[0] - 50) // 2 * box_width
        space_y = (gridsize[1] - 50) // 2 * box_width
        return [y * box_height + space_y, x * box_width + space_x]


    def draw_grid(size, gridsize):
        for i in range(gridsize[0] + 1):
            for j in range(gridsize[1] + 1):
                pygame.draw.line(screen, GRAY, [0, j * box_height], [size[0], j * box_height])
                pygame.draw.line(screen, GRAY, [i * box_width, 0], [i * box_width, size[1]])


    def draw_battery(screen, color, location):
        battery_location = [location[0] - 1, location[1] - 2]

        battery_underlay_rect = pygame.Rect(get_on_screen_coordinates(*battery_location), (2 * box_width, 2 * box_height))
        pygame.draw.rect(screen, color, battery_underlay_rect)

        battery.set_alpha(130)
        screen.blit(battery, get_on_screen_coordinates(*battery_location))


    def draw_house(screen, color, location):
        house_location = [location[0] - 0.5, location[1] - 0.5]

        house_underlay_rect = pygame.Rect(get_on_screen_coordinates(*house_location), (box_width, box_height))
        pygame.draw.rect(screen, color, house_underlay_rect)

        house.set_alpha(130)
        screen.blit(house, get_on_screen_coordinates(*house_location))


    def draw_cables(screen, color, cables):
        starting_point = tuple(map(int, cables[0].split(",")))
        for end_point in cables[1:]:
            end_point = tuple(map(int, end_point.split(",")))

            pygame.draw.line(screen, color, get_on_screen_coordinates(*starting_point),
                            get_on_screen_coordinates(*end_point), width=2)

            starting_point = end_point


    def draw_all(screen):
        draw_grid(size, gridsize)
        
        draw_total_costs()

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

            battery_capacity = location_data['capacity']
            draw_text(screen, f"Capacity: {battery_capacity}", color, get_on_screen_coordinates(*map(int, location_data['location'].split(','))))



    try:
        file = open(file_path, 'r')
        data = json.load(file)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        sys.exit(1)
    # -------- Main Program Loop -----------
    while not quit:

        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True


        # --- Game logic should go here

        # --- Screen-clearing code goes here

        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(WHITE)

        # --- Drawing code should go here
        draw_all(screen)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()
