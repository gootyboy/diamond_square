from terrain_classes import *
from biomes import _BIOMES as _BIOMES
from __future__ import annotations
from pgzero.rect import Rect
from pgzero.screen import Screen as PGZeroScreen
from PIL import Image
import pygame
from pygame.surface import Surface as PyGameSurface

@overload
def height_to_color(h, biome: str = "default"): ...
@overload
def height_to_color(h, biome: Biome = DEFAULT_BIOME): ...

def height_to_color(h, biome: Union[str, Biome]):
    if isinstance(biome, Biome):
        biome = biome.name
    for b in _BIOMES:
        if biome == b.name:
            return b.height_to_color(h)

def _point_in_circle(pos, center, radius):
    dx = pos[0] - center[0]
    dy = pos[1] - center[1]
    return dx ** 2 + dy ** 2 < radius ** 2

@overload
def generate_terrain(size, biome: str = "default", roughness = 0.6, scale = 4): ...
@overload
def generate_terrain(size, biome: Biome = DEFAULT_BIOME, roughness = 0.6, scale = 4): ...

def generate_terrain(size, biome: Union[str, Biome], roughness = 0.6, scale = 4):
    return Terrain(size, biome, roughness, scale)

@overload
def generate_pgzero_interactive(size, start_biome: str = "default", max_roughness = 1.0,  min_roughness = 0, start_roughness = 0, scale = 4, pos = (0, 0)): ...
@overload
def generate_pgzero_interactive(size, start_biome: Biome = DEFAULT_BIOME, max_roughness = 1.0,  min_roughness = 0, start_roughness = 0, scale = 4, pos = (0, 0)): ...

def generate_pgzero_interactive(size, start_biome: Union[str, Biome], max_roughness = 1.0,  min_roughness = 0, start_roughness = 0, scale = 4, pos = (0, 0)):
    return PGZeroInteractive(size, start_biome, max_roughness, min_roughness, start_roughness, scale, pos)

@overload
def generate_pygame_interactive(size, start_biome: str = "default", max_roughness = 1.0,  min_roughness = 0, start_roughness = 0, scale = 4, pos = (0, 0)): ...
@overload
def generate_pygame_interactive(size, start_biome: Biome = DEFAULT_BIOME, max_roughness = 1.0,  min_roughness = 0, start_roughness = 0, scale = 4, pos = (0, 0)): ...

def generate_pygame_interactive(size, start_biome: Union[str, Biome], max_roughness = 1.0,  min_roughness = 0, start_roughness = 0, scale = 4, pos = (0, 0)):
    return PyGameInteractive(size, start_biome, max_roughness, min_roughness, start_roughness, scale, pos)
