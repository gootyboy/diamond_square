# Sample code for drawing terrain in pygame
# This sample code file displays both interactive mode and a terrain in the same screen

# Imports
import pygame
from diamond_square import generate_terrain, generate_pygame_interactive

# Initilizing pygame and setting the display size
pygame.init()
screen = pygame.display.set_mode((800, 600))

# Creating the terrain
terrain = generate_terrain(
    roughness=1.0,
    biome="default",
    scale=1,
    size=257
)

# Creating the interactive terrain
interactive_terrain = generate_pygame_interactive(
    max_roughness=1.0,
    start_biome="default",
    start_roughness=0.1, 
    scale=1,
    size=2 ** 9 + 1,
)

# Main loop
running = True
while running:
    # Gets the events
    # Make sure you use the same variable (events) for both your event loop and the events parameter in inertactive_terrain.draw()
    events = pygame.event.get()
    # Stops the main loop when the user closes the window
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Drawing the interactive terrain
    interactive_terrain.draw(screen, events)
    # Drawing the terrain
    terrain.draw(screen, pos=(300, 300))
    # Updating the display
    pygame.display.flip()

# Quits pygame when user closes the window
pygame.quit()
