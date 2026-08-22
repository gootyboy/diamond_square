# Sample code of saving terrain images.

# Import diamond_square.
from diamond_square import Biome, Terrain, DESERT_BIOME

# mybiome is the function which takes in a height and return a color mapping.
# The color mapping must be a RGB tuple. Strings are not accepted.
def mybiome(h: float) -> tuple[int, int, int]:
    if h <= 0.5:
        return (255, 255, 255)
    else:
        return (0, 0, 0)

# This function adds the biome to the existing list of biomes.
MYBIOME = Biome(name="mybiome", htc_func=mybiome).add_to_biomes()

# "default" is a biome which is included in the library.
# The position parameter is not useful in this case.
# It is useful when drawing it on pgzero or pygame.
Terrain(size=2 ** 5 + 1, biome="default", roughness=0.5, scale=4, pos=(0, 0)).save_as_img("test_terrain.png")

# "mybiome" is a custom biome I created at line 8 and added at line 15.
Terrain(size=2 ** 5 + 1, biome="mybiome", roughness=0.5, scale=4, pos=(0, 0)).save_as_img("mybiome.png")

# DESERT_BIOME is a Biome which is included in the library.
# You can either use the string names, or the in-built constants for in-built biomes.
Terrain(size=2 ** 5 + 1, biome=DESERT_BIOME, roughness=0.5, scale=4, pos=(0, 0)).save_as_img("desert.png")

# When saving a custom made biome, you may use the Biome object or the name.
Terrain(size=2 ** 5 + 1, biome=MYBIOME, roughness=0.5, scale=4, pos=(0, 0)).save_as_img("mybiome2.png")
