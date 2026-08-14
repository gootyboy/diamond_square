from typing import overload, Union

_BIOMES = []

class Biome:
    """Class to create new biomes."""
    def __init__(self: Biome, name: str, height_to_color_func: function) -> None:
        """
        Create a new biome.

        :param name:
            The name of the biome.

        :param height_to_color_func:
            A function that maps a height value to a color. The function must have
            the following form::

                def height_to_color(h):
                    if h < 0.1:
                        ...
                    elif h < 0.4:
                        ...
                    else:
                        ...

            The function should return a RGB Tuple. Strings or Hex codes will not work.

        """

        self.name = name
        """The name of the Biome"""

        self.height_to_color = height_to_color_func
        """The height to color function"""

    def __str__(self: Biome) -> str:
        """
        String representation of the Biome. Returns the name of the Biome.

        :return str: Name of the biome
        """
        return self.name

    def __repr__(self: Biome) -> str:
        """
        Returns the representation of the Biome. biome = exec(repr(biome))

        :return str: The representation.
        """
        return f"Biome({repr(self.name)}, {repr(self.height_to_color)})"

    def add_biome(self: Biome) -> None:
        """Adds the biome to the list of biomes."""
        add_biome(self)

def _default_func(h):
    if h < 0.2:
        return (0, 0, int(100 + h * 80))
    if h < 0.3:
        return (0, 50, int(150 + h * 80))
    if h < 0.35:
        return (194, 178, 128)
    if h < 0.5:
        return (34, 139, 34)
    if h < 0.6:
        return (0, 100, 0)
    if h < 0.75:
        return (120, 110, 100)
    if h < 0.9:
        return (160, 160, 160)
    return (255, 255, 255)

def _desert_func(h):
    if h < 0.2:
        return (210, 180, 140)
    if h < 0.4:
        return (237, 201, 175)
    if h < 0.6:
        return (194, 178, 128)
    if h < 0.8:
        return (150, 140, 120)
    return (255, 255, 255)

def _tundra_func(h):
    if h < 0.05:
        return (0, 0, 120)
    if h < 0.1:
        return (0, 40, 140)
    if h < 0.3:
        return (150, 150, 150)
    if h < 0.4:
        return (180, 180, 180)
    return (255, 255, 255)

def _tropical_func(h):
    if h < 0.2:
        return (0, 30, 150)
    if h < 0.3:
        return (0, 80, 180)
    if h < 0.4:
        return (240, 220, 130)
    if h < 0.6:
        return (34, 180, 34)
    if h < 0.75:
        return (0, 120, 0)
    return (255, 255, 255) 

def _volcanic_func(h):
    if h < 0.2:
        return (20, 20, 20)
    if h < 0.4:
        return (40, 40, 40)
    if h < 0.6:
        return (80, 0, 0)
    if h < 0.8:
        return (200, 50, 0)
    return (255, 120, 50)

def _swamp_func(h):
    if h < 0.2:
        return (20, 40, 20)
    if h < 0.35:
        return (40, 60, 30)
    if h < 0.5:
        return (70, 90, 50)
    if h < 0.7:
        return (90, 120, 70)
    return (130, 160, 110)

def _ocean_func(h):
    if h < 0.2:
        return (0, 10, 40)
    if h < 0.4:
        return (0, 30, 80)
    if h < 0.6:
        return (0, 60, 120)
    if h < 0.8:
        return (0, 100, 160)
    if h < 0.9:
        return (200, 190, 140)
    return (240, 220, 180)

def _mars_func(h):
    if h < 0.2:
        return (60, 30, 20)
    if h < 0.35:
        return (110, 50, 30)
    if h < 0.55:
        return (160, 70, 40)
    if h < 0.7:
        return (200, 120, 80)
    if h < 0.85:
        return (230, 200, 170)
    return (240, 240, 240)

def add_biome(biome: Biome):
    if biome.name in [b.name for b in _BIOMES]:
        raise TypeError(f"\"{biome}\" biome is already in the added biomes list: {list(map(str, _BIOMES))}.")

    _BIOMES.append(biome)

DEFAULT_BIOME = Biome("default", _default_func)
DESERT_BIOME = Biome("desert", _desert_func)
TUNDRA_BIOME = Biome("tundra", _tundra_func)
TROPICAL_BIOME = Biome("tropical", _tropical_func)
VOLCANIC_BIOME = Biome("volcanic", _volcanic_func)
SWAMP_BIOME = Biome("swamp", _swamp_func)
OCEAN_BIOME = Biome("ocean", _ocean_func)
MARS_BIOME = Biome("mars", _mars_func)

add_biome(DEFAULT_BIOME)
add_biome(DESERT_BIOME)
add_biome(TUNDRA_BIOME)
add_biome(TROPICAL_BIOME)
add_biome(VOLCANIC_BIOME)
add_biome(SWAMP_BIOME)
add_biome(OCEAN_BIOME)
add_biome(MARS_BIOME)

@overload
def remove_biome(biome_name: str):
    ...

@overload
def remove_biome(biome: Biome):
    ...

def remove_biome(arg):
    name = arg if isinstance(arg, str) else arg.name
    for b in _BIOMES:
        if b.name == name:
            _BIOMES.remove(b)
            return

    raise TypeError(f'"{name}" biome is not in the list.')
