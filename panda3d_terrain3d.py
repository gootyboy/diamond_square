# This sample file demonstrates how to create and draw 3d terrains.

# Import diamond_square
from src.diamond_square import *

# Generate 3D Terrain.
terrain = Terrain3D(size=2 ** 8 + 1, biome=DEFAULT_BIOME, roughness=0.6, scale=5, pos=(0, 0, 0))

# Panda3D main class. Panda3DBase is a class included in diamond_square.
class Panda3DTerrain3D(Panda3DBase):
    def __init__(self):
        super().__init__()

        # Drawing the terrain.
        # You must pass in self for the obj parameter.
        terrain.draw_panda3d(obj=self)

# Creating the panda3d app.
app = Panda3DTerrain3D()

# Running the app.
app.run()
