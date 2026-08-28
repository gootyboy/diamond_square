"""
This package implements the Diamond Square Algorithm to draw terrains in pgzero and pygame and 3D terrains in panda3D.
Interactive terrain generation also available in pgzero and pygame.
Uses C for fast rendering of the core Diamond Square algorithm.
"""

from .biome_funcs import *
from .biomes import *
from .core_algorithm import core_diamond_square
from .filter_funcs import *
from .interactive_terrain import *
from .terrain import *
from .terrain3d import Terrain3D, Panda3DBase
