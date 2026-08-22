# This file demonstrates how to create your own biomes.

# Import diamond_square
from diamond_square import Biome, Terrain

# mybiome is the function which takes in a height and return a color mapping.
# The color mapping must be a RGB tuple. Strings are not accepted.
def mybiome(h: float) -> tuple[int, int, int]:
    if h <= 0.5:
        return (255, 255, 255)
    else:
        return (0, 0, 0)

# This function adds the biome to the existing list of biomes.
MYBIOME = Biome(name="mybiome", htc_func=mybiome).add_to_biomes()

# When using a custom made biome, you may use the Biome object or the name.
# "mybiome" is a custom biome I created at line 8 and added at line 15.
Terrain(size=2 ** 5 + 1, biome="mybiome", roughness=0.5, scale=4, pos=(0, 0)).save_as_img("mybiome.png")

# MYBIOME is the Biome object.
Terrain(size=2 ** 5 + 1, biome=MYBIOME, roughness=0.5, scale=4, pos=(0, 0)).save_as_img("mybiome2.png")
