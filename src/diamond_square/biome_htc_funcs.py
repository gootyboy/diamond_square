from .utils import *

def default_biome_htc(h: float) -> tuple[int, int, int]:
    """
    This is the height to color function for the default biome.

    Parameters
    ----------
    **h**: float
        The height. Must be a value from 0 to 1 (in the interval [0, 1]).

    Returns
    -------
    **Color**: tuple[int, int, int]
        The color based on the height and the function.
    """
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

def desert_biome_htc(h: float) -> tuple[int, int, int]:
    """
    This is the height to color function for the desert biome.

    Parameters
    ----------
    **h**: float
        The height. Must be a value from 0 to 1 (in the interval [0, 1]).

    Returns
    -------
    **Color**: tuple[int, int, int]
        The color based on the height and the function.
    """
    if h < 0.2:
        return (210, 180, 140)
    if h < 0.4:
        return (237, 201, 175)
    if h < 0.6:
        return (194, 178, 128)
    if h < 0.8:
        return (150, 140, 120)

    return (255, 255, 255)

def tundra_biome_htc(h: float) -> tuple[int, int, int]:
    """
    This is the height to color function for the tundra biome.

    Parameters
    ----------
    **h**: float
        The height. Must be a value from 0 to 1 (in the interval [0, 1]).

    Returns
    -------
    **Color**: tuple[int, int, int]
        The color based on the height and the function.
    """
    if h < 0.05:
        return (0, 0, 120)
    if h < 0.1:
        return (0, 40, 140)
    if h < 0.3:
        return (150, 150, 150)
    if h < 0.4:
        return (180, 180, 180)

    return (255, 255, 255)

def tropical_biome_htc(h: float) -> tuple[int, int, int]:
    """
    This is the height to color function for the tropical biome.

    Parameters
    ----------
    **h**: float
        The height. Must be a value from 0 to 1 (in the interval [0, 1]).

    Returns
    -------
    **Color**: tuple[int, int, int]
        The color based on the height and the function.
    """
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

def volcanic_biome_htc(h: float) -> tuple[int, int, int]:
    """
    This is the height to color function for the volcanic biome.

    Parameters
    ----------
    **h**: float
        The height. Must be a value from 0 to 1 (in the interval [0, 1]).

    Returns
    -------
    **Color**: tuple[int, int, int]
        The color based on the height and the function.
    """
    if h < 0.2:
        return (20, 20, 20)
    if h < 0.4:
        return (40, 40, 40)
    if h < 0.6:
        return (80, 0, 0)
    if h < 0.8:
        return (200, 50, 0)

    return (255, 120, 50)

def swamp_biome_htc(h: float) -> tuple[int, int, int]:
    """
    This is the height to color function for the swamp biome.

    Parameters
    ----------
    **h**: float
        The height. Must be a value from 0 to 1 (in the interval [0, 1]).

    Returns
    -------
    **Color**: tuple[int, int, int]
        The color based on the height and the function.
    """
    if h < 0.2:
        return (20, 40, 20)
    if h < 0.35:
        return (40, 60, 30)
    if h < 0.5:
        return (70, 90, 50)
    if h < 0.7:
        return (90, 120, 70)

    return (130, 160, 110)

def ocean_biome_htc(h: float) -> tuple[int, int, int]:
    """
    This is the height to color function for the ocean biome.

    Parameters
    ----------
    **h**: float
        The height. Must be a value from 0 to 1 (in the interval [0, 1]).

    Returns
    -------
    **Color**: tuple[int, int, int]
        The color based on the height and the function.
    """
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

def mars_biome_htc(h: float) -> tuple[int, int, int]:
    """
    This is the height to color function for the mars biome.

    Parameters
    ----------
    **h**: float
        The height. Must be a value from 0 to 1 (in the interval [0, 1]).

    Returns
    -------
    **Color**: tuple[int, int, int]
        The color based on the height and the function.
    """
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
