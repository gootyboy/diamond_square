from terrain_classes import *
from biomes import _BIOMES as _BIOMES
from __future__ import annotations
from pgzero.rect import Rect
from pgzero.screen import Screen as PGZeroScreen
from PIL import Image
import pygame
from pygame.surface import Surface as PyGameSurface

@overload
def generate_terrain(size, biome: str = "default", roughness = 0.6, scale = 4) -> Terrain: ...
@overload
def generate_terrain(size, biome: Biome = DEFAULT_BIOME, roughness = 0.6, scale = 4) -> Terrain: ...

def generate_terrain(size, biome: Union[str, Biome], roughness = 0.6, scale = 4) -> Terrain:
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
