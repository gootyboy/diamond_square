# Sample code for drawing terrain in pgzero.

# Imports diamond_square and pgzrun.
from diamond_square import Terrain
import pgzrun

# Setting the WIDTH and HEIGHT of the window.
WIDTH = 1100
HEIGHT = 1100

# Creating the terrain.
terrain = Terrain(
    size=2 ** 9 + 1,
    biome="default",
    roughness=0.6,
    scale=2,
    pos=(10, 10)
)

# draw function for all of the main drawing.
def draw():
    # Clearing the screen to ensure that the interactive terrain updates correctly.
    screen.clear()

    # Drawing the terrain.
    terrain.draw(screen)

# update function.
def update():
    # This function is needed to make sure pgzero updates the display.
    pass

pgzrun.go()
