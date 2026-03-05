# Sample code for drawing terrain in pygame
# This sample code file displays both interactive mode and a terrain in the same screen

import pygame
from diamond_square import generate_pygame_terrain, generate_pygame_interactive

pygame.init()
screen = pygame.display.set_mode((800, 600))

terrain = generate_pygame_terrain(
    roughness=1.0,
    biome="default",
    scale=1,
    size=257
)

interactive_terrain = generate_pygame_interactive(
    max_roughness=1.0,
    start_biome="default",
    start_roughness=0.1, 
    scale=1,
    size=2 ** 9 + 1,
)

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    interactive_terrain.draw(screen, events)
    terrain.draw(screen, pos=(300, 300))
    pygame.display.flip()

pygame.quit()