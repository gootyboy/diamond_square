import inspect
from typing import overload
from .biomes import Biome, DEFAULT_BIOME, ADDED_BIOMES
from .core_algorithm import core_diamond_square
from .terrain_saving import _TerrainSaving as _TerrainSaving
import pygame
import pgzero.rect

class Terrain:
    """Class for pgzero and pygame terrains."""
    @overload
    def __init__(self, size: int, biome: str = "default", roughness: float = 0.6, scale: int = 4, pos: tuple[int, int] = (0, 0)) -> None:
        """
        Creates the terrain.

        Parameters
        ----------
        **size**: int
            The size. Must be in the form 2 ** n + 1.
        **biome**: str
            The biome name.
        **roughness**: float
            Controls the amount of randomness is added to each pixel.
        **scale**: int
            This determines how large the pixels are. Must be an integer greater than 1.
        **pos**: tuple[int, int]
            The topleft position of the terrain.

        Raises
        ------
        TypeError
            If the biome is not in the ADDED_BIOMES list.
        """
    @overload
    def __init__(self, size: int, biome: Biome = DEFAULT_BIOME, roughness: float = 0.6, scale: int = 4, pos: tuple[int, int] = (0, 0)) -> None:
        """
        Creates the terrain.

        Parameters
        ----------
        **size**: int
            The size. Must be in the form 2 ** n + 1.
        **biome**: Biome
            The Biome object.
        **roughness**: float
            Controls the amount of randomness is added to each pixel.
        **scale**: int
            This determines how large the pixels are. Must be an integer greater than 1.
        **pos**: tuple[int, int]
            The topleft position of the terrain.

        Raises
        ------
        TypeError
            If the biome is not in the ADDED_BIOMES list.
        """
    @overload
    def __init__(self, height_map: list[list[float]], biome: str = "default", scale: int = 4, pos: tuple[int, int] = (0, 0)) -> None: ...
    @overload
    def __init__(self, height_map: list[list[float]], biome: Biome = DEFAULT_BIOME, scale: int = 4, pos: tuple[int, int] = (0, 0)) -> None: ...

    def __init__(self, *args, **kwargs) -> None:
        sig_size = inspect.Signature([
            inspect.Parameter('size', inspect.Parameter.POSITIONAL_OR_KEYWORD),
            inspect.Parameter('biome', inspect.Parameter.POSITIONAL_OR_KEYWORD, default="default"),
            inspect.Parameter('roughness', inspect.Parameter.POSITIONAL_OR_KEYWORD, default=0.6),
            inspect.Parameter('scale', inspect.Parameter.POSITIONAL_OR_KEYWORD, default=4),
            inspect.Parameter('pos', inspect.Parameter.POSITIONAL_OR_KEYWORD, default=(0, 0)),
        ])

        # Overload B: (height_map, biome="default", scale=4, pos=(0, 0))
        sig_map = inspect.Signature([
            inspect.Parameter('height_map', inspect.Parameter.POSITIONAL_OR_KEYWORD),
            inspect.Parameter('biome', inspect.Parameter.POSITIONAL_OR_KEYWORD, default="default"),
            inspect.Parameter('scale', inspect.Parameter.POSITIONAL_OR_KEYWORD, default=4),
            inspect.Parameter('pos', inspect.Parameter.POSITIONAL_OR_KEYWORD, default=(0, 0)),
        ])

        # 2. Determine which overload to use by inspecting what was passed
        # Check if 'height_map' was passed as a keyword, or if the first argument is a list
        is_map_variant = 'height_map' in kwargs or (len(args) > 0 and isinstance(args[0], list))

        if is_map_variant:
            # Bind using the height_map signature rules
            bound = sig_map.bind(*args, **kwargs)
            bound.apply_defaults()
            params = bound.arguments

            height_map = params['height_map']
            biome = params['biome']
            scale = params['scale']
            pos = params['pos']

            if not isinstance(height_map, list):
                raise TypeError("height_map must be a 2D list of floats.")

            size = len(height_map)
            roughness = 0.0

            self.heights = height_map
            """The heights in the height map."""
            
            self._roughness = roughness
            """The roughness of the terrain (If the height map is given, then roughness is set to 0.0). Do not change the value of this variable. Use self.roughness instead of self._roughness."""

        else:
            # Bind using the size signature rules
            bound = sig_size.bind(*args, **kwargs)
            bound.apply_defaults()
            params = bound.arguments

            size = params['size']
            biome = params['biome']
            roughness = params['roughness']
            scale = params['scale']
            pos = params['pos']

            if not isinstance(size, int):
                raise TypeError("size must be an integer.")

            self.heights = core_diamond_square(size, roughness)
            """The heights in the height map."""
            
            self._roughness = roughness
            """The roughness of the terrain. Do not change the value of this variable. Use self.roughness instead of self._roughness."""

        # 3. Handle shared Biome validation logic
        if isinstance(biome, Biome):
            biome_name = biome.name
            """The biome name of the terrain."""
        elif isinstance(biome, str):
            biome_name = biome
            """The biome name of the terrain."""
            biome = ADDED_BIOMES.get(f"{biome_name}")
        else:
            raise TypeError(f"The 'biome' parameter mist be a string (the name) or a Biome (the object).")

        if biome is None:
            raise TypeError(f"Biome name must be in {list(ADDED_BIOMES.items())}")

        # 4. Assign final properties
        self.biome: str = biome_name
        """The biome name of the terrain."""

        self.biome_obj: Biome = biome
        """The Biome of the terrain."""

        self._size = size
        """The size of the terrain. Do not change the value of this variable. Use self.size instead of self._size."""

        self.scale = scale
        """The scale of the terrain. This determines how large the pixels are. Must be an integer greater than 1."""

        self.pos = pos
        """The topleft position of the terrain."""

    @property
    def roughness(self):
        """The roughness of the terrain."""
        return self._roughness

    @roughness.setter
    def roughness(self, value):
        """Sets the roughness of the terrain."""
        self._roughness = value
        self.re_generate()

    @property
    def size(self):
        """The size of the terrain. Size must be in the form 2 ** n + 1."""
        return self._size

    @size.setter
    def size(self, value):
        """Sets the size of the terrain. Size must be in the form 2 ** n + 1."""
        self._size = value
        self.re_generate()

    def draw(self, screen_or_surface) -> None:
        """
        Draws the terrain on pgzero or pygame determined by the screen_or_surface parameter.

        Parameters
        ----------
        **screen_or_surface**: Screen | Surface
            This is the screen in pgzero or a Surface in pygame.
        """
        ox, oy = self.pos
        is_pgzero = not isinstance(screen_or_surface, pygame.surface.Surface)
        for y in range(self.size):
            for x in range(self.size):
                color = self.biome_obj.height_to_color(self.heights[y][x])
                if is_pgzero:
                    screen_or_surface.draw.rect(pgzero.rect.Rect(ox + x * self.scale, oy + y * self.scale, self.scale, self.scale), color=color)
                else:
                    pygame.draw.rect(screen_or_surface, color, pygame.rect.Rect(ox + x * self.scale, oy + y * self.scale, self.scale, self.scale))

    def save_as_img(self, save_path: str):
        """
        Saves the terrain as an image.

        Parameters
        ----------
        **save_path**: str
            The path to save the image to.

        Returns
        -------
        Terrain
            The terrain that was saved (self).
        """
        _TerrainSaving.save_as_img(self.size, self.scale, self.heights, self.biome_obj, save_path)

        return self

    def re_generate(self):
        """Re-Generates the terrain (creates a new height map)."""
        self.heights = core_diamond_square(self.size, self.roughness)
