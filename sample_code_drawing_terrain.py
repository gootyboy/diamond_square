# Sample code for drawing terrain
# This sample code file displays both interactive mode and a terrain in the same screen

from src.diamond_square import generate_terrain, generate_pgzero_interactive
import pgzrun

WIDTH = 900
HEIGHT = 900

terrain = generate_terrain(
    roughness=1.0,
    biome="default",
    scale=1,
    size=257,
)

interactive_terrain = generate_pgzero_interactive(
    size=257,
    start_biome="default",
    max_roughness=1.0,
    scale=2,
    start_roughness=0.1
)

def draw():
    screen.clear()
    terrain.draw(screen, pos = (600, 600))
    interactive_terrain.for_draw(screen)

def update():
    pass

def on_mouse_down(pos):
    interactive_terrain.for_on_mouse_down(pos)

def on_mouse_up():
    interactive_terrain.for_on_mouse_up()

def on_mouse_move(pos):
    interactive_terrain.for_on_mouse_move(pos)

pgzrun.go()