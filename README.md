# Diamond Square

Implementation of the [Diamond–Square Algorithm](https://en.wikipedia.org/wiki/Diamond-square_algorithm). This package can draw terrain on pgzero and pygame, and can also set up interactive mode.

Interactive mode is only supported by pgzero. If you are using this package in pygame, you cannot use the interactive mode, but you can still use terrain generation.

Visit the documentation page for more details:  
[Diamond Square Description](https://gootyboy.github.io/diamond_square.html)

---

## Sample Generations

![Sample Default Terrain](https://gootyboy.github.io/project_details/diamond-square/default_terrain.png)
![Sample Desert Terrain](https://gootyboy.github.io/project_details/diamond-square/desert_terrain.png)
![Sample Tundra Terrain](https://gootyboy.github.io/project_details/diamond-square/tundra_terrain.png)
![Sample Tropical Terrain](https://gootyboy.github.io/project_details/diamond-square/tropical_terrain.png)
![Sample Volcanic Terrain](https://gootyboy.github.io/project_details/diamond-square/volcanic_terrain.png)
![Sample Swamp Terrain](https://gootyboy.github.io/project_details/diamond-square/swamp_terrain.png)
![Sample Ocean Terrain](https://gootyboy.github.io/project_details/diamond-square/ocean_terrain.png)
![Sample Mars Terrain](https://gootyboy.github.io/project_details/diamond-square/mars_terrain.png)
![Sample Extreme Mars Terrain](https://gootyboy.github.io/project_details/diamond-square/mars_crazy.png)

---

> ### ⚠️ ***Interactive mode only works in pgzero***
> pygame cannot use interactive mode — only terrain generation.

> ### ⚠️ ***You MUST include all four interactive functions***
> Missing even one will cause failures or unpredictable behavior.

> ### ⚠️ ***You must pass the pgzero screen into draw functions***
> Use `terrain.draw(screen)` or `terrain.for_draw(screen)` — the yellow underline is expected.

---

## Table of Contents
- [Quick Start](#quick-start)
- [Why Use Diamond Square?](#why-use-diamond-square)
- [Usage](#usage)
- [Drawing Terrain](#drawing-terrain)
  - [pgzero Example](#pgzero-example)
  - [pygame Example](#pygame-example)
- [Important Requirements for Interactive Mode](#important-requirements-for-interactive-mode)
- [Interactive Mode](#interactive-mode)
- [Versions](#versions)
- [Coming Soon](#coming-soon)

---

## Quick Start

### Installation
```
pip install diamond-square
```

### Minimal Example
```python
from diamond_square import generate_terrain

terrain = generate_terrain(roughness=1.0, biome="default", scale=1, size=257)

def draw():
    terrain.draw(screen)
```

---

## Why Use Diamond Square?

This package provides a complete implementation of the Diamond–Square algorithm with:

- multiple built‑in biomes  
- adjustable roughness and scale  
- support for pgzero and pygame  
- optional interactive mode (pgzero only)  
- the ability to save generated terrain as an image  
- functions to add or remove biomes dynamically  

It is designed for both experimentation and game development, making terrain generation simple and customizable.

---

## Usage

### Drawing Terrain

Use:

```
terrain = generate_terrain(roughness=..., biome=..., scale=..., size=...)
```

Then draw it with:

```
terrain.draw(screen)
```

The `screen` parameter must be the pgzero screen or the pygame display surface. In pgzero, simply pass `screen`. Your editor may underline this, but it is correct.

---

## Drawing Terrain

### pgzero Example

```python
from diamond_square import generate_terrain

terrain = generate_terrain(
    roughness=1.0,
    biome="default",
    scale=1,
    size=257
)

def draw():
    terrain.draw(screen)

def update():
    pass
```

Run with:

```
pgzrun yourfile.py
```

---

### pygame Example

```python
import pygame
from diamond_square import generate_terrain

pygame.init()
screen = pygame.display.set_mode((800, 600))

terrain = generate_terrain(
    roughness=1.0,
    biome="default",
    scale=1,
    size=257
)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    terrain.draw(screen)
    pygame.display.flip()

pygame.quit()
```

---

## Important Requirements for Interactive Mode

Interactive mode **only works in pgzero**, and it requires **all four** of the following functions to be placed in their corresponding pgzero event handlers:

```
terrain.for_draw(screen)
terrain.for_on_mouse_down(pos)
terrain.for_on_mouse_up()
terrain.for_on_mouse_move(pos)
```

If **any one** of these is missing, the interactive mode will:

- fail to update correctly  
- behave unpredictably  
- or stop working entirely  

These must be placed in:

- `draw()` → `terrain.for_draw(screen)`  
- `on_mouse_down(pos)` → `terrain.for_on_mouse_down(pos)`  
- `on_mouse_up()` → `terrain.for_on_mouse_up()`  
- `on_mouse_move(pos)` → `terrain.for_on_mouse_move(pos)`  

---

## Interactive Mode

Use:

```
terrain = generate_interactive_mode(
    size=...,
    start_biome=...,
    max_roughness=...,
    scale=...,
    start_roughness=...
)
```

This creates an interactive scene where the user can change the biome and roughness in real time.

Interactive mode is **not supported in pygame** — only pgzero.

---

## Versions

Version 0.0.1: Main code for diamond-square added.  
Version 0.0.2: Updated README file and added documentation.  
Version 0.0.3: Fixed bugs and errors.  
Version 0.0.4: Added sample terrain.  
Version 0.0.5: Added sample terrains.  
Version 0.0.6: Added functions to add/remove biomes and added external documentation website.  
**(Latest) Version 0.0.7:** Added `pos` parameter to determine where to place the terrain and added function to save terrain as an image.

---

## Coming Soon

Version 0.0.8: Updates
