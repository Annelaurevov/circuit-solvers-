import pygame
import json

file = open(r"outputs/output_district-2.json", 'r')
data = json.load(file)
 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (220, 220, 220)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 210, 0)
PURPLE = (255, 0, 255)
ORANGE = (255, 150, 0)
colors = [BLUE, RED, GREEN, PURPLE, ORANGE]

pygame.init()

size = (800, 800)
gridsize = (60, 60)
screen = pygame.display.set_mode(size)
box_width = size[0] // gridsize[0]
box_height = size[1] // gridsize[1]

pygame.display.set_caption("My Game")
done = False
clock = pygame.time.Clock()

battery = pygame.image.load(r'images/battery.png')
battery = pygame.transform.scale(battery, (2 * box_width, 2 * box_height))

house = pygame.image.load(r'images/house.png').convert_alpha()
house = pygame.transform.scale(house, (1 * box_width, 1 * box_height))


def get_on_screen_coordinates(x, y):
    return [y * box_width, x * box_height]


def draw_grid(size, gridsize):
    for i in range(gridsize[0]):
        for j in range(gridsize[1]):
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
    
    id = 0
    for location_data in data[1:]:
        color = colors[id]
        id += 1
        
        draw_battery(screen, color, tuple(map(int, location_data['location'].split(','))))

        for house_data in location_data["houses"]:
            draw_house(screen, color, tuple(map(int, house_data['location'].split(','))))
            draw_cables(screen, color, house_data["cables"])


# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

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
