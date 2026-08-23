# Sample code for drawing terrain in pygame.

# Import diamond_square and pygame
from diamond_square import Terrain
import pygame

# Initilizing pygame.
pygame.init()

# Creating the main surface with width 800 and height 600.
screen = pygame.display.set_mode((800, 600))

# Creating the terrain.
terrain = Terrain(
    size=2**8 + 1,
    biome="default",
    roughness=1.0,
    scale=1,
    pos=(10, 10)
)

# Variable to keep track if the pygame window is open.
running = True

# Main loop.
while running:
    # Gets all of the events.
    # Make sure you use the same variable (events) for both your event loop and the events parameter in interactive_terrain.draw().
    events = pygame.event.get()

    # Stops the main loop when the user closes the window.
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Drawing the terrain.
    terrain.draw(screen)

    # Updating the display.
    pygame.display.flip()

# Quits pygame when user closes the window.
pygame.quit()
