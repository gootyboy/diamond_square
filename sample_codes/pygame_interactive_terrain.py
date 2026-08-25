# Sample code for drawing interactive terrain in pygame.

# Import diamond_square and pygame
from diamond_square import PyGameInteractive
import pygame

# Initilizing pygame.
pygame.init()

# Creating the main surface with width 1000 and height 1000.
screen = pygame.display.set_mode((1000, 1000))

# Creating the interactive terrain.
interactive_terrain = PyGameInteractive(
    size=2**8 + 1,
    start_biome="default",
    max_roughness=1.0,
    min_roughness=0.0,
    start_roughness=0.1, 
    scale=2,
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

    screen.fill("black")

    # Drawing the interactive terrain.
    interactive_terrain.draw(screen, events)

    # Updating the display.
    pygame.display.flip()

# Quits pygame when user closes the window.
pygame.quit()
