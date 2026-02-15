# Diamond Square

Implementation of the [Diamond Square Algorithm](https://en.wikipedia.org/wiki/Diamond-square_algorithm). This package can draw terrain on pgzero and pygame, also can set up interactive mode.

Interactive mode is only supported by pgzero. If you are using this package in pygame, you cannot use the interactive mode, but you can use the terrain generation.

# Sample generations

![Sample Default Terrain](https://gootyboy.github.io/project_details/diamond-square/default_terrain.png) ![Sample Desert Terrain](https://gootyboy.github.io/project_details/diamond-square/desert_terrain.png) ![Sample Tundra Terrain](https://gootyboy.github.io/project_details/diamond-square/tundra_terrain.png) ![Sample Tropical Terrain](https://gootyboy.github.io/project_details/diamond-square/tropical_terrain.png) ![Sample Volcanic Terrain](https://gootyboy.github.io/project_details/diamond-square/volcanic_terrain.png) ![Sample Swamp Terrain](https://gootyboy.github.io/project_details/diamond-square/swamp_terrain.png) ![Sample Ocean Terrain](https://gootyboy.github.io/project_details/diamond-square/ocean_terrain.png) ![Sample Mars Terrain](https://gootyboy.github.io/project_details/diamond-square/mars_terrain.png) ![Sample Extreme Mars Terrain](https://gootyboy.github.io/project_details/diamond-square/mars_crazy.png)

# Usage:

**Drawing Terrain:**

Use `terrain = generate_terrain(roughness=..., biome=..., scale=..., size=...)` to generate terrain. Once you generate terrain and store it in a variable, the terrain won't draw unless you call `terrain.draw(screen)`.

When you pass in the screen parameter for `terrain.draw(screen)`, this is expecting the pgzero screen or the pygame display surface. For pgzero, just enter `screen` for the screen parameter. This will have a yellow underline under it, but do not worry because this is what is supposed to happen.

**Drawing interactive Terrain:**

Use `terrain = generate_interactive_mode(size=..., start_biome=..., max_roughness=..., scale=..., start_roughness=...)` to generate an interactive scence which the user can interact and change the biome and roughness. Once you generate the interactive terrain and store it in a variable, the terrain won't draw unless you call `terrain.for_draw(screen)` in the draw function, `terrain.for_on_mouse_down(pos)` in the on_mouse_down function, `terrain.for_on_mouse_up()` in the on_mouse_up function, and `terrain.for_on_mouse_move(pos)` in the on_mouse_move function.

If you leave out any one of these, then it will create unexpected results or fail. As of latest version, drawing interactive terrains is not suppored by pygame. You can only use this in pgzero.

For the draw function, when you pass in the screen parameter for `terrain.draw(screen)`, this is expecting the pgzero screen or the pygame display surface. For pgzero, just enter `screen` for the screen parameter. This will have a yellow underline under it, but do not worry because this is what is supposed to happen.

# Versions:

Version 0.0.1: Main code for diamond-square added.

Version 0.0.2: Updated REAMDE file and added documentation.

Version 0.0.3: Fixed bugs and errors

Version 0.0.4: Added sample terrain.

(Latest) Version 0.0.5: Added sample terrains.

# Coming Soon:

Version 0.0.6: Added a function to add/remove biomes and added parameter pos to determine where to place the terrain.
