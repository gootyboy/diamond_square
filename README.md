# Diamond Square

Implementation of the [Diamond–Square Algorithm](https://en.wikipedia.org/wiki/Diamond-square_algorithm). This package can draw terrain on pgzero and pygame, and can also set up interactive mode.

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
![Sample Crazy Mars Terrain](https://gootyboy.github.io/project_details/diamond-square/mars_crazy.png)

---

> ### ⚠️ ***You MUST include all four interactive functions for pgzero interactive***
> Missing even one will cause failures or unpredictable behavior.

> ### ⚠️ ***You must pass the pgzero screen into draw functions***
> Use `terrain.draw(screen)` or `terrain.for_draw(screen)` — the yellow underline is expected.

---

## Table of Contents
- Quick Start
  - Installation
- Why Use Diamond Square?
- Usage
  - Drawing Terrain
    - Pgzero Example
    - Pygame Example
  - Interactive Mode
    - Pgzero Example
    - Pygame Example
- Requirements for Pgzero Interactive
- Versions
- Coming Soon

---

## Quick Start

### Installation
```
pip install diamond-square
```

---

## Why Use diamond-square?

This package provides a complete implementation of the Diamond–Square algorithm with:

- Fast rendering of the Diamond-Square algorithm written in C
- Multiple built‑in biomes  
- Adjustable roughness and scale  
- Support for pgzero and pygame  
- Optional interactive mode (pgzero only)  
- The ability to save generated terrain as an image  
- Functions to add or remove biomes dynamically  

It is designed for both experimentation and game development, making terrain generation simple and customizable.

---

## Usage

### Drawing Terrain

#### Pgzero Example

Look at sample_code_pgzero_drawing_terrain.py for pgzero examples.

---

#### Pygame Example

Look at sample_code_pygame_drawing_terrain.py for pygame examples.

The `screen` parameter must be the pygame display surface.

### Interactive Mode

This creates an interactive scene where the user can change the biome and roughness in real time.

#### Pgzero example

Look at sample_code_pgzero_drawing_terrain.py for pgzero examples.

#### Pygame example

Look at sample_code_pygame_drawing_terrain.py for pygame examples.

---

## Requirements for Pgzero Interactive

For Pgzero Interative Mode, it requires **all four** of the following functions to be placed in their corresponding pgzero event handlers:

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

## Versions

Version 0.0.1: Main code for diamond-square added.  
Version 0.0.2: Updated README file and added documentation.  
Version 0.0.3: Fixed bugs and errors.  
Version 0.0.4: Added sample terrain.  
Version 0.0.5: Added sample terrains.  
Version 0.0.6: Added functions to add/remove biomes and added external documentation website.  
Version 0.0.7: Added `pos` parameter to determine where to place the terrain and added function to save terrain as an image. Also made interative mode avaliable to pgzero.
Version 0.0.8:  Added C file for fast rendering of the [Diamond–Square Algorithm](https://en.wikipedia.org/wiki/Diamond-square_algorithm)
**(Latest) Version 0.0.9:** Made pgzero and pygame interactive mode into one function and added documentation

---

## Coming Soon

Version 0.1.0: Complete documentation
