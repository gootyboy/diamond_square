# Diamond Square

245-278
Implementation of the [Diamond–Square Algorithm](https://en.wikipedia.org/wiki/Diamond-square_algorithm). This package can draw terrains and interactive terrains in pgzero and pygame. Also can draw 3D terrains in panda3d.

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
>
> Missing even one will cause failures or unpredictable behavior.

---

## Table of Contents

- Why Use Diamond Square?
- Usage
  - Terrain Examples
    - Pgzero Terrain Example
    - Pygame Terrain Example
    - Panda3d 3D Terrain Example
  - Interactive Terrain Examples
    - Pgzero Interactive Terrain Example
    - Pygame Interactive Terrain Example
  - Other Examples
    - Custom Biome Examples
    - Image Saving Examples
- Requirements for Pgzero Interactive
- Versions
- Coming Soon

---

## Why Use diamond-square?

This package provides a complete implementation of the Diamond–Square algorithm with:

- Fast rendering of the Diamond-Square algorithm written in C.

- Multiple built‑in biomes.

- Adjustable roughness, scale, and size.

- Support for pgzero and pygame.

- 3d terrain drawing in panda3d.

- Interactive mode.

- Change the border shape of the terrain (it is normally a square) using a function.

- The ability to save generated terrain as an image.

- Functions to add or remove biomes dynamically.

It is designed for both experimentation and game development, making 2d/3d terrain generation simple and customizable.

---

## Usage

### Terrain Examples

#### Pgzero Terrain Example

Go to [/sample_codes/pgzero_terrain.py](https://github.com/gootyboy/diamond_square/blob/main/sample_codes/pgzero_terrain.py)

#### Pygame Terrain Example

Go to [/sample_codes/pygame_terrain.py](https://github.com/gootyboy/diamond_square/blob/main/sample_codes/pygame_terrain.py)

#### Panda3d 3D Terrain Example

Go to [/sample_code/custom_biome.py](https://github.com/gootyboy/diamond_square/blob/main/sample_codes/panda3d_terrain3d.py)

---

### Interactive Terrain Examples

#### Pgzero Interactive Terrain Example

Go to [/sample_codes/pgzero_interactive_terrain.py](https://github.com/gootyboy/diamond_square/blob/main/sample_codes/pgzero_interactive_terrain.py)

#### Pygame Interactive Terrain Example

Go to [/sample_codes/pygame_interactive_terrain.py](https://github.com/gootyboy/diamond_square/blob/main/sample_codes/pygame_interactive_terrain.py)

---

### Other Examples

### Image Saving Examples

Go to [/sample_codes/save_terrain.py](https://github.com/gootyboy/diamond_square/blob/main/sample_codes/save_terrain.py)

### Custom Biome Examples

Go to [/sample_code/custom_biome.py](https://github.com/gootyboy/diamond_square/blob/main/sample_codes/custom_biome.py)

---

## Requirements for Pgzero Interactive

For Pgzero Interative Mode, it requires **all four** of the following functions to be placed in their corresponding pgzero event handlers:

```python
terrain.draw_func(screen)
terrain.on_mouse_down_func(pos)
terrain.on_mouse_up_func()
terrain.on_mouse_move_func(pos)
```

If **any one** of these is missing, the interactive mode will:

- fail to update correctly

- behave unpredictably

- or stop working entirely

These must be placed in these functions in pgzero:

- `def draw():` → `terrain.draw_func(screen)`

- `on_mouse_down(pos):` → `terrain.on_mouse_down_func(pos)`

- `on_mouse_up():` → `terrain.on_mouse_up_func()`

- `on_mouse_move(pos):` → `terrain.on_mouse_move_func(pos)`

---

## Versions

**(LATEST) Version 1.0.0**: Added 3D Terrain Generation in panda3d.

Version 0.2.0: Add re-generate button for interactive mode in pygame.

Version 0.1.9: Improve speed in C file and fix bugs.

*To view previous versions, go to [versions.txt](https://github.com/gootyboy/diamond_square/blob/main/versions.txt)*

---

## Coming Soon

Version 1.1.0: Add filter functions for 2D terrains.
