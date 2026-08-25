# Sample code for drawing interactive terrain in pgzero.

# Imports diamond_square and pgzrun.
from diamond_square import PGZeroInteractive
import pgzrun

# Setting the WIDTH and HEIGHT of the window.
WIDTH = 900
HEIGHT = 900

# Creating the interactive terrain.
interactive_terrain = PGZeroInteractive(
    size=2 ** 8 + 1,
    start_biome="default",
    max_roughness=1.0,
    min_roughness=0.0,
    scale=2,
    start_roughness=0.1,
    pos=(10, 10)
)

# draw function for all of the main drawing.
def draw():
    # Clearing the screen to ensure that the interactive terrain updates correctly.
    screen.clear()

    # Drawing the interactive terrain.
    interactive_terrain.draw_func(screen)

# update function.
def update():
    # This function is needed to make sure pgzero updates the display.
    pass

# on_mouse_down function for when the user clicked the screen.
def on_mouse_down(pos):
    # Interactive terrain function for when the user clicked the screen.
    interactive_terrain.on_mouse_down_func(pos)

# on_mouse_up function for when the user releases the mouse click the screen.
def on_mouse_up():
    # Interactive terrain function for when the user releases the mouse click the screen.
    interactive_terrain.on_mouse_up_func()

# on_mouse_move function for when the user moved the mouse on the display.
def on_mouse_move(pos):
    # Interactive terrain function for when the user moved the mouse on the display.
    interactive_terrain.on_mouse_move_func(pos)

# Runs the pgzero file.
pgzrun.go()
