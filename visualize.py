# tool om te visualiseren welke connecties er zijn


import pygame
import json

file = open(r"outputs/output_district-1.json", 'r')
# file = open(r"test.json", 'r')



data = json.load(file)
 
# Define some colors
BLACK = (0, 0, 0)

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
colors = [BLUE, RED, GREEN, PURPLE, YELLOW]

pygame.init()




# Set the width and height of the screen [width, height]
size = (600, 600)
gridsize = (60, 60)
screen = pygame.display.set_mode(size)

battery = pygame.image.load(r'images/battery.png')
battery = pygame.transform.scale(battery, (2*size[0]//gridsize[0], 2*size[1]//gridsize[1]))


house = pygame.image.load(r'images/house.png')
house = pygame.transform.scale(house, (2*size[0]//gridsize[0], 2*size[1]//gridsize[1]))


pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

def get_on_screen_coordinates(x, y):
    return [y * size[0]//gridsize[0], x * size[1]//gridsize[1]]


def draw_on_screen(screen):
    for i in range(gridsize[0]):

        for j in range(gridsize[1]):
            pygame.draw.line(screen, GRAY, [0, j*size[1]//gridsize[1]], [size[1], j*size[1]//gridsize[1]])
            pygame.draw.line(screen, GRAY, [i*size[0]//gridsize[0], 0], [i*size[0]//gridsize[0], size[0]])
    id = 0
    for location_data in data[1:]:
        color = colors[id]
        id += 1
        battery_location = list(map(int, location_data['location'].split(',')))
        battery_location = [battery_location[0] - 1, battery_location[1] - 1]
        
        screen.blit(battery, get_on_screen_coordinates(*battery_location))

        for houses in location_data["houses"]:
            house_location = list(map(int, houses['location'].split(',')))
            house_location = [house_location[0] - 1, house_location[1] - 1]
            screen.blit(house, get_on_screen_coordinates(*house_location))

            cables = houses["cables"]

            starting_point = tuple(map(int, cables[0].split(",")))
            for end_point in cables[1:]:
                end_point = tuple(map(int, end_point.split(",")))
                
                pygame.draw.line(screen, color, get_on_screen_coordinates(*starting_point), get_on_screen_coordinates(*end_point), width=2)
                starting_point = end_point 



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
    draw_on_screen(screen)
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
