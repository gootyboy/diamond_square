# Sample code of saving terrain images

from diamond_square import *

# mybiome is the function which takes in a height and return a color mapping
# The color mapping must be a RGB tuple. Strings are not accepted
def mybiome(h):
    if h < 5:
        return (255, 255, 0)
    else:
        return (255, 0, 0)

# This function adds the biome to the existing list of biomes
add_biome(Biome("mybiome", mybiome))

# "default" is a biome which is included in the library
# Use generate_pgzero_terrain or generate_pygame_terrain if you want to save a terrain as an image
save_terrain(generate_pgzero_terrain(2 ** 5 + 1, "default", 0.5, 4), "test_terrain.png")

# "mybiome" is a custom biome I added at line 9
save_terrain(generate_pgzero_terrain(2 ** 5 + 1, "mybiome", 0.5, 4), "mybiome.png")

# "desert" is a biome which is included in the library
save_terrain(generate_pgzero_terrain(2 ** 5 + 1, "desert", 0.5, 4), "desert.png") 
