"""
All functions and classes are accessible through this file.
"""
from diamond_square.core import *
from biomes import _BIOMES as _BIOMES
from pgzero.rect import Rect
from pgzero.screen import Screen as PGZeroScreen
from PIL import Image
import pygame
from pygame.surface import Surface as PyGameSurface

@overload
def generate_terrain(size: int, biome: str = "default", roughness: float = 0.6, scale: int = 4, pos: tuple[int, int] = (0, 0)) -> Terrain:
    """
    Creates the terrain. You may also use Terrain(...) instead of generate_terrain(...).

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

    Returns
    -------
    **terrain**: Terrain
        The Terrain object.
    """
@overload
def generate_terrain(size: int, biome: Biome = DEFAULT_BIOME, roughness: float = 0.6, scale: int = 4, pos: tuple[int, int] = (0, 0)) -> Terrain:
    """
    Creates the terrain. You may also use Terrain(...) instead of generate_terrain(...).

    Parameters
    ----------
    **size**: int
        The size. Must be in the form 2 ** n + 1.
    biome: str
        The Biome object.
    roughness: float
        Controls the amount of randomness is added to each pixel.
    scale: int
        This determines how large the pixels are. Must be an integer greater than 1.
    pos: tuple[int, int]
        The topleft position of the terrain. 

    Returns
    -------
    **terrain**: Terrain
        The Terrain object.
    """

def generate_terrain(size: int, biome: Union[str, Biome], roughness: float = 0.6, scale: int = 4, pos: tuple[int, int] = (0, 0)) -> Terrain:
    return Terrain(size, biome, roughness, scale, pos)

@overload
def generate_pgzero_interactive(size: int, start_biome: str = "default", max_roughness: float = 1.0,  min_roughness: float = 0, start_roughness: float = 0, scale: int = 4, pos: tuple[float, float] = (0, 0)):
    """
    Creates a interactive mode for pgzero. You may also use PGZeroInteractive(...) instead of generate_pgzero_interactive(...)

    Parameters
    ----------
    **size**: int
        The size. Must be in the form 2 ** n + 1.
    **start_biome**: str
        The biome name to start on.
    **max_roughness**: float
        The maximum roughness allowed on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
    **min_roughness**: float
        The maximum roughness allowed on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
    **start_roughness**: float
        The starting roughness on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
    **scale**: int
        This determines how large the pixels are. Must be an integer greater than 1.
    **pos**: tuple[float, float]
        The topleft position of the interactive terrain.

    Returns
    -------
    **interactive terrain**: PGZeroInteractive
        The interactive terrain generated.
    """
@overload
def generate_pgzero_interactive(size: int, start_biome: Biome = DEFAULT_BIOME, max_roughness: float = 1.0,  min_roughness: float = 0, start_roughness: float = 0, scale: int = 4, pos: tuple[float, float] = (0, 0)):
    """
    Creates a interactive mode for pgzero. You may also use PGZeroInteractive(...) instead of generate_pgzero_interactive(...)

    Parameters
    ----------
    **size**: int
        The size. Must be in the form 2 ** n + 1.
    **start_biome**: str
        The Biome object to start on.
    **max_roughness**: float
        The maximum roughness allowed on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
    **min_roughness**: float
        The maximum roughness allowed on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
    **start_roughness**: float
        The starting roughness on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
    **scale**: int
        This determines how large the pixels are. Must be an integer greater than 1.
    **pos**: tuple[float, float]
        The topleft position of the interactive terrain.

    Returns
    -------
    **interactive terrain**: PGZeroInteractive
        The interactive terrain generated.
    """

def generate_pgzero_interactive(size, start_biome: Union[str, Biome], max_roughness = 1.0,  min_roughness = 0, start_roughness = 0, scale = 4, pos = (0, 0)):
    return PGZeroInteractive(size, start_biome, max_roughness, min_roughness, start_roughness, scale, pos)

@overload
def generate_pygame_interactive(size: int, start_biome: str = "default", max_roughness: float = 1.0,  min_roughness: float = 0, start_roughness: float = 0, scale: int = 4, pos: tuple[float, float] = (0, 0)):
    """
    Creates a interactive mode for pygame. You may also use PyGameInteractive(...) instead of generate_pygame_interactive

    :param size: The size. Must be in the form 2 ** n + 1.
    :param start_biome: The Biome object to start on.
    :param max_roughness: The maximum roughness allowed on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
    :param min_roughness: The maximum roughness allowed on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
    :param start_roughness: The starting roughness on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
    :param scale: This determines how large the pixels are. Must be an integer greater than 1.
    :param pos: The topleft position of the interactive terrain.
    """
@overload
def generate_pygame_interactive(size: int, start_biome: Biome = DEFAULT_BIOME, max_roughness: float = 1.0,  min_roughness: float = 0, start_roughness: float = 0, scale: int = 4, pos: tuple[float, float] = (0, 0)):
    """
    Creates a interactive mode for pygame.

    :param size: The size. Must be in the form 2 ** n + 1.
    :param start_biome: The Biome object to start on.
    :param max_roughness: The maximum roughness allowed on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
    :param min_roughness: The maximum roughness allowed on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
    :param start_roughness: The starting roughness on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
    :param scale: This determines how large the pixels are. Must be an integer greater than 1.
    :param pos: The topleft position of the interactive terrain.
    """

def generate_pygame_interactive(size, start_biome: Union[str, Biome], max_roughness = 1.0,  min_roughness = 0, start_roughness = 0, scale = 4, pos = (0, 0)):
    return PyGameInteractive(size, start_biome, max_roughness, min_roughness, start_roughness, scale, pos)
