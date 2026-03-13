from ctypes import *
import os

_file = 'diamond_lib.so'
_path = os.path.join(*(os.path.split(__file__)[:-1] + (_file,)))
_mod = cdll.LoadLibrary(_path)

_mod.diamond_square.restype = POINTER(POINTER(c_double))
_mod.diamond_square.argtypes = [c_int, c_float]

def diamond_square(size, roughness):
    return _mod.diamond_square(size, roughness)
