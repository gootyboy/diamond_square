# diamond_square

Implementation of the diamond-square. Can draw terrain on pgzero and pygame. Also can set up interactive mode.

Drawing Terrain:

Use `terrain = generate_terrain(roughness=..., biome=..., scale=..., size=...)` to generate terrain. Once you generate terrain and store it in a variable, the terrain won't draw unless you call `terrain.draw(screen)`.

When you pass in the screen parameter for `terrain.draw(screen)`, this is expecting the pgzero screen or the pygame display surface. For pgzero, just enter `screen` for the screen parameter. This will have a yellow underline under it, but do not worry because this is what is supposed to happen.

Drawing interactive Terrain:

Use `terrain = generate_interactive_mode(size=..., start_biome=..., max_roughness=..., scale=..., start_roughness=...)` to generate an interactive scence which the user can interact and change the biome and roughness. Once you generate the interactive terrain and store it in a variable, the terrain won't draw unless you call `terrain.for_draw(screen)` in the draw function, `terrain.for_on_mouse_down(pos)` in the on_mouse_down function, `terrain.for_on_mouse_up()` in the on_mouse_up function, and `terrain.for_on_mouse_move(pos)` in the on_mouse_move function.

If you leave out any one of these, then it will create unexpected results or fail.

For the draw function, when you pass in the screen parameter for `terrain.draw(screen)`, this is expecting the pgzero screen or the pygame display surface. For pgzero, just enter `screen` for the screen parameter. This will have a yellow underline under it, but do not worry because this is what is supposed to happen.

Versions:

Version 0.0.1: Main code for diamond-square added.
(Latest) Version 0.0.2: Updated REAMDE file and added documentation.
Version 0.0.3: Added a function to add/remove biomes and added parameter pos to determine where to place the terrain.
