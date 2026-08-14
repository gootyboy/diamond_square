# Sample code of saving terrain images

# Import diamond_square
from diamond_square import Biome, generate_terrain

# mybiome is the function which takes in a height and return a color mapping
# The color mapping must be a RGB tuple. Strings are not accepted
def mybiome(h):
    if h < 5:
        return (255, 255, 0)
    else:
        return (255, 0, 0)

# This function adds the biome to the existing list of biomes
Biome("mybiome", mybiome).add_biome()

# "default" is a biome which is included in the library
generate_terrain(2 ** 5 + 1, "default", 0.5, 4).save_as_img("test_terrain.png")

# "mybiome" is a custom biome I added at line 8
generate_terrain(2 ** 5 + 1, "mybiome", 0.5, 4).save_as_img("mybiome.png")

# "desert" is a biome which is included in the library
generate_terrain(2 ** 5 + 1, "desert", 0.5, 4).save_as_img("desert.png")
