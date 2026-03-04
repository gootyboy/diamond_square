import ctypes
import os

class Array2D(ctypes.Structure):
    _fields_ = [
        ("rows", ctypes.c_size_t),
        ("cols", ctypes.c_size_t),
        ("data", ctypes.POINTER(ctypes.POINTER(ctypes.c_double)))
    ]

_file = 'diamond.so'
_path = os.path.join(*(os.path.split(__file__)[:-1] + (_file, )))
_mod = ctypes.cdll.LoadLibrary(_path)

_mod._diamond_square.restype = Array2D
_mod._diamond_square.argtypes = [ctypes.c_int, ctypes.c_float]

h_map = _mod._diamond_square(2 ** 5 + 1, 0.6)
data = h_map.data
