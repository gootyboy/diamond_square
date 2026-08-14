from ctypes import *
import os

class Array2D(Structure):
    _fields_ = [
        ("rows", c_size_t),
        ("cols", c_size_t),
        ("data", POINTER(POINTER(c_double)))
    ]

_file = 'diamond_lib.so'
_path = os.path.join(*(os.path.split(__file__)[:-1] + (_file,)))
_mod = cdll.LoadLibrary(_path)

_mod.diamond_square.restype = Array2D
_mod.diamond_square.argtypes = [c_int, c_float]

def diamond_square(size, roughness):
    c_heights = _mod.diamond_square(size, roughness)

    heights = [
        [c_heights.data[y][x] for x in range(size)]
        for y in range(size)
    ]

    return heights
