"""
C to Python wrapper for the core diamond square algorithm.
"""

from .utils import *

class Array2D(ctypes.Structure):
    """
    A Structure for a struct in the diamond.c file.

    Fields
    ------
    **rows**: c_size_t

        The amount of rows for the array.
    **cols**: c_size_t

        The amount of columns for the array.
    **data**: POINTER(POINTER(c_double))

        The data of the array.
    """
    _fields_ = [
        ("rows", ctypes.c_size_t),
        ("cols", ctypes.c_size_t),
        ("data", ctypes.POINTER(ctypes.POINTER(ctypes.c_double)))
    ]

_file = 'diamond_lib.so'
"""The file name of the .so file. Do not change the value of this variable."""
_path = os.path.join(*(os.path.split(__file__)[:-1] + (_file,)))
"""The path of the .so file. Do not change the value of this variable."""
_mod = ctypes.cdll.LoadLibrary(_path)
"""The loaded library of the .so file. Do not change the value of this variable."""

_mod.diamond_square.restype = Array2D
_mod.diamond_square.argtypes = [ctypes.c_int, ctypes.c_float]

def diamond_square(size: int, roughness: float) -> list[list[float]]:
    """
    Returns a height map using the Diamond Square Algorithm.
    
    Parameters
    ----------
    **size**: int
        The size of the height map. Must be in the form 2 ** n + 1.
    **roughness**: float
        Controls the amount of randomness that is added to each height value.

    Returns
    -------
    **Height Map**: list[list[float]]
        The height map generated using the Diamond Square Algorithm.
    """
    c_heights = _mod.diamond_square(size, roughness)

    heights = [
        [c_heights.data[y][x] for x in range(size)]
        for y in range(size)
    ]

    return heights
