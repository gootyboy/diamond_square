"""
This package implements the Diamond Square Algorithm to draw terrains in pgzero and pygame.
Interactive terrain generation also available in pgzero and pygame.
Uses C for fast rendering of the core Diamond Square algorithm.
"""

from .biome_funcs import *
from .biomes import *
from .core_algorithm import core_diamond_square


from .utils import *
from .biomes import *
from .biomes import ADDED_BIOMES as ADDED_BIOMES
from .terrain3d import Terrain3D, Panda3DBase
from .filter_funcs import *
from .terrain import *
