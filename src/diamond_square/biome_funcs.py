from .utils import *

def _darken_color(rgb, factor=0.2):
    """
    Darkens an RGB color tuple by a given factor (0.0 to 1.0).
    factor=0.2 means 20% darker.
    """
    # Ensure the factor is between 0 and 1
    factor = max(0.0, min(1.0, factor))
    
    # Calculate the multiplier (e.g., 20% darker means keeping 80% of the brightness)
    multiplier = 1.0 - factor
    
    # Multiply each channel and round to the nearest integer
    r = int(rgb[0] * multiplier)
    g = int(rgb[1] * multiplier)
    b = int(rgb[2] * multiplier)
    
    return (r, g, b)

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
    tan = (210, 180, 140)
    if h < 0.3:
        return _darken_color(tan, 0.05)
    if h < 0.5:
        return _darken_color(tan, 0.1)
    if h < 0.8:
        return _darken_color(tan, 0.15)
    else:
        return _darken_color(tan, 0.2)

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
    if h < 0.3:
        return (0, 30, 150)
    if h < 0.4:
        return (0, 80, 180)
    if h < 0.6:
        return (240, 220, 130)
    if h < 0.8:
        return (34, 180, 34)
    else:
        return (0, 120, 0)

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
    if h < 0.7:
        return (0, 60, 120)
    if h < 0.9:
        return (0, 100, 160)
    if h < 0.95:
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


def default_biome_ht3d(h: float) -> float:
    """
    Height to 3D function for the default biome.
    This function only necessary for 3D drawing in Terrain3D. 
    This function takes a height value (between 0 and 1) and returns another value, telling the code how much to stretch the pixel into 3d.
    """
    return (h * 10) ** (1.5)

def desert_biome_ht3d(h: float) -> float:
    """
    Height to 3D function for the desert biome.
    This function only necessary for 3D drawing in Terrain3D. 
    This function takes a height value (between 0 and 1) and returns another value, telling the code how much to stretch the pixel into 3d.
    """
    return (h * 10) ** 1.2

def tundra_biome_ht3d(h: float) -> float:
    """
    Height to 3D function for the tundra biome.
    This function only necessary for 3D drawing in Terrain3D. 
    This function takes a height value (between 0 and 1) and returns another value, telling the code how much to stretch the pixel into 3d.
    """
    return (h * 10) ** 1.7

def tropical_biome_ht3d(h: float) -> float:
    """
    Height to 3D function for the tropical biome.
    This function only necessary for 3D drawing in Terrain3D. 
    This function takes a height value (between 0 and 1) and returns another value, telling the code how much to stretch the pixel into 3d.
    """
    return (h * 10) ** 1.35


def volcanic_biome_ht3d(h: float) -> float:
    """
    Height to 3D function for the volcanic biome.
    This function only necessary for 3D drawing in Terrain3D. 
    This function takes a height value (between 0 and 1) and returns another value, telling the code how much to stretch the pixel into 3d.
    """
    return ((1 - h) * 10) ** (1 + 0.5 * ((1 - h)**2))

def swamp_biome_ht3d(h: float) -> float:
    """
    Height to 3D function for the swamp biome.
    This function only necessary for 3D drawing in Terrain3D. 
    This function takes a height value (between 0 and 1) and returns another value, telling the code how much to stretch the pixel into 3d.
    """
    return (h * 10) ** 1.1

def ocean_biome_ht3d(h: float) -> float:
    """
    Height to 3D function for the ocean biome.
    This function only necessary for 3D drawing in Terrain3D. 
    This function takes a height value (between 0 and 1) and returns another value, telling the code how much to stretch the pixel into 3d.
    """
    return (h * 10) ** 1.1

def mars_biome_ht3d(h: float) -> float:
    """
    Height to 3D function for the mars biome.
    This function only necessary for 3D drawing in Terrain3D. 
    This function takes a height value (between 0 and 1) and returns another value, telling the code how much to stretch the pixel into 3d.
    """
    return (h * 10) ** 1.15
