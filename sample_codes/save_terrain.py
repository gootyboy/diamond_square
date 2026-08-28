# Sample code of saving terrain images.

# Import diamond_square.
from diamond_square import Terrain, DESERT_BIOME

# "default" is a biome which is included in the library.
# The position parameter is not useful in this case.
# It is useful when drawing it on pgzero or pygame.
Terrain(size=2 ** 5 + 1, biome="default", roughness=0.5, scale=4, pos=(0, 0)).save_as_img("default.png")

# DESERT_BIOME is a Biome which is included in the library.
# You can either use the string names, or the in-built constants for in-built biomes.
Terrain(size=2 ** 5 + 1, biome=DESERT_BIOME, roughness=0.5, scale=4, pos=(0, 0)).save_as_img("desert.png")
