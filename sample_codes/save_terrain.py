# Sample Code for saving a Terrain as an image and a Terrain3D as a .stl and a .obj

# Import diamond-square
from diamond_square import Terrain, Terrain3D, DEFAULT_BIOME, DESERT_BIOME

# "default" is a biome which is included in the library.
# The position parameter is not useful in this case.
# It is useful when drawing it on pgzero or pygame.
default_terrain = Terrain(size=2 ** 5 + 1, biome="default", roughness=0.5, scale=4, pos=(0, 0))

# Saving the default terrain as an image
default_terrain.save_as_img("default.png")

# DESERT_BIOME is a Biome which is included in the library.
# You can either use the string names, or the in-built constants for in-built biomes.
desert_terrain = Terrain(size=2 ** 5 + 1, biome=DESERT_BIOME, roughness=0.5, scale=4, pos=(0, 0))

# Saving the desert terrain as an image
desert_terrain.save_as_img("desert.png")

# Create the Terrain3D
terrain3d = Terrain3D(size=2 ** 8 + 1, biome=DEFAULT_BIOME, roughness=0.6, scale=2, pos=(0, 0, 0))

# Saving terrain as .stl
terrain3d.save_as_stl("terrain3d.stl")

# Saving terrain as .obj
terrain3d.save_as_obj("terrain3d.stl")
