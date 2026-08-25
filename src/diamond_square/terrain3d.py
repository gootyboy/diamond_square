from .utils import *
from .diamond import diamond_square
from .biomes import *

def _panda3d_box(obj, width, height, depth, pos, color):
    rectangle = obj.loader.loadModel("models/box")
    rectangle.reparentTo(obj.render)

    rectangle.setScale(width / 2, depth / 2, height / 2)

    rectangle.setTextureOff(1)
    rectangle.setLightOff()

    r, g, b = color
    rectangle.setColor(r / 255, g / 255, b / 255, 1)
    rectangle.setPos(*pos)

    return rectangle

class Terrain3D:
    def __init__(self, size, biome: Biome, roughness, scale):
        """The scale parameter does not have to be a integer ≥ 1. It can be any number > 0."""
        self.size = size
        self.biome = biome
        self.roughness = roughness
        self.scale = scale

        self.height_map = diamond_square(size, roughness)

    def draw_panda3d(self, obj):
        """obj is the panda3d class. When using this function inside a panda3d class, pass the panda3d class `self` into obj."""
        for y, row in enumerate(self.height_map):
            for x, h in enumerate(row):
                color = self.biome.height_to_color(h)
                height = (h * 10) ** (1.5)
                _panda3d_box(obj, 0.1 * self.scale, height, 0.1 * self.scale, (x * self.scale * 0.05, y * self.scale * 0.05, 0), color)
