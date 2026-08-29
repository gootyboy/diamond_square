"""
This file has the Biome class, add_biome and remove_biome function, and in-built biomes.
"""

from typing import Callable
from .biome_funcs import *
import numpy as np

ADDED_BIOMES = dict()
"""This is the dict of the biome names. {name: obj}."""

class Biome:
    """Class to create new biomes."""
    def __init__(self, name: str, htc_func: Callable[[float], tuple[int, int, int]], height_to_3d: Callable[[float], float] | None = None) -> None:
        """
        Creates a new biome.

        Parameters
        ----------
        name: str
            The name of the biome.

        htc_func (( float)) -> tuple[int, int, int]
            A function that maps a height value to a color. The function must have
            the following form::

                def height_to_color(h: float) -> float[int, int, int]:
                    if h < ...: # float between 0 and 1
                        return ... # RGB tuple
                    elif h < ...: # float between 0 and 1
                        return ... # RGB tuple
                    ...
                    else:
                        return ... # RGB tuple
                # The function should return a RGB Tuple. Strings or Hex codes will not work.

        height_to_3d (( float)) -> float
            Optional function only necessary for 3D drawing in Terrain3D. 
            A function that takes a height value (between 0 and 1) and returns another value, telling the code how much to stretch the pixel into 3d.
            If height_to_3d = lambda h: h, then the 3d heights of the pixels are equal to the height map.
            The best function to use is in the form lambda h: (h * 10) ** dramatic. dramatic is how dramatic you want your biome to be.

            Examples:
            - For biomes like DEFAULT_BIOME, height_to_3d is (h * 10) ** 1.5 
              Stretches higher values drastically to create tall, dramatic mountain peaks.
              
            - For biomes like DESERT_BIOME, height_to_3d is (h * 10) ** 1.2 or just h
              Keeps the terrain flatter and more gradual to simulate rolling desert dunes.
        """

        self.name = name
        """The name of the Biome."""

        self.height_to_color = htc_func
        """The height to color function."""

        if height_to_3d == None:
            height_to_3d = lambda h: (h * 10) ** 1.4

        self.height_to_3d = height_to_3d
        """Function that takes a height value and returns another value, which tells the code how much to stretch the pixel into 3d."""

    def __str__(self) -> str:
        """
        String representation of the Biome. Returns the name of the Biome.

        Returns
        -------
        str
            The name of the biome.
        """
        return self.name

    def __repr__(self) -> str:
        """
        Returns the representation of the Biome.

        Returns
        -------
        str
            The representation of the Biome such that exec(repr(biome)) = biome.

        """
        return f"Biome({repr(self.name)}, {repr(self.height_to_color)}, {repr(self.height_to_3d)})"

    def add_to_biomes(self):
        """
        Adds a Biome to the list of biomes so that it can be used in a terrain.

        Returns
        ------
        Biome
            The biome that was added (self).

        Raises
        ------
        TypeError
            If there already exists another biome with the same name as the biome parameter.
        """
        if self.name in ADDED_BIOMES:
            raise TypeError(f"You cannot add a biome with the same name as another biome in the added biomes list: {list(ADDED_BIOMES.keys())}.")

        ADDED_BIOMES[f"{self.name}"] = self

        return self

    def remove_from_biomes(self):
        """
        Removes a Biome to the list of biomes.

        Returns
        ------
        Biome
            The biome that was added (self).

        Raises
        ------
        TypeError
            If the biome is not already added.
        """
        deleted_val = ADDED_BIOMES.pop(self.name, None)
        if deleted_val == None:
            raise TypeError(f'"{self.name}" biome is not in the list. Biomes must be added before they can be removed.')
        else:
            return self

    def get_average_color(self):
        """
        Gets the average color of the biome based on the htc function.

        Returns
        -------
        tuple[int, int, int]
            The average color of the biome.
        """
        colors = []
        for i in np.arange(0, 1, 0.001):
            colors.append(self.height_to_color(i))

        rgb = list(zip(*colors))
        red = sum(rgb[0]) / len(rgb[0])
        green = sum(rgb[1]) / len(rgb[1])
        blue = sum(rgb[2]) / len(rgb[2])

        return (int(red), int(green), int(blue))

DEFAULT_BIOME = Biome("default", default_biome_htc, default_biome_ht3d).add_to_biomes()
"""The default Biome."""

DESERT_BIOME = Biome("desert", desert_biome_htc, desert_biome_ht3d).add_to_biomes()
"""The desert Biome."""

TUNDRA_BIOME = Biome("tundra", tundra_biome_htc, tundra_biome_ht3d).add_to_biomes()
"""The tundra Biome."""

TROPICAL_BIOME = Biome("tropical", tropical_biome_htc, tropical_biome_ht3d).add_to_biomes()
"""The tropical Biome."""

VOLCANIC_BIOME = Biome("volcanic", volcanic_biome_htc, volcanic_biome_ht3d).add_to_biomes()
"""The volcanic Biome."""

SWAMP_BIOME = Biome("swamp", swamp_biome_htc, swamp_biome_ht3d).add_to_biomes()
"""The swamp Biome."""

OCEAN_BIOME = Biome("ocean", ocean_biome_htc, ocean_biome_ht3d).add_to_biomes()
"""The ocean Biome."""

MARS_BIOME = Biome("mars", mars_biome_htc, mars_biome_ht3d).add_to_biomes()
"""The mars Biome."""
