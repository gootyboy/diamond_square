# Sample code for drawing terrain in pgzero
# This sample code file displays both interactive mode and a terrain in the same screen

# Imports
from diamond_square import Terrain, PGZeroInteractive
import pgzrun

# Setting the WIDTH and HEIGHT of the window
WIDTH = 900
HEIGHT = 900

# Creating the terrain
terrain = Terrain(
    roughness=1.0,
    biome="default",
    scale=1,
    size=257,
)

# Creating the interactive terrain
interactive_terrain = PGZeroInteractive(
    size=257,
    start_biome="default",
    max_roughness=1.0,
    scale=2,
    start_roughness=0.1
)

# Draw function
def draw():
    # Clearing the screen
    screen.clear()
    # Drawing the terrain
    terrain.draw(screen, pos = (600, 600))
    # Drawing the interactive terrain
    interactive_terrain.for_draw(screen)

# Update function
def update():
    # This function is needed to make sure pgzero updates the display
    pass

# Function for when the user clicked the screen
def on_mouse_down(pos):
    # Interactive terrain function for when the user clicked the screen
    interactive_terrain.for_on_mouse_down(pos)

# Function for when the user un-clicked the screen
def on_mouse_up():
    # Interactive terrain function for when the user un-clicked the screen
    interactive_terrain.for_on_mouse_up()

# Function for when the user moved the mouse on the display
def on_mouse_move(pos):
    # Interactive terrain function for when the user moved the mouse on the display
    interactive_terrain.for_on_mouse_move(pos)

# Runs the pgzero file
pgzrun.go()
