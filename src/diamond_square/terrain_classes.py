from __future__ import annotations
from pgzero.rect import Rect
from pgzero.screen import Screen as PGZeroScreen
from PIL import Image
import pygame
from pygame.surface import Surface as PyGameSurface
from biomes import *
from .diamond import diamond_square
from biomes import _BIOMES as _BIOMES

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

class Terrain:
    """Class for pgzero and pygame terrains."""
    @overload
    def __init__(self, size, biome: str = "default", roughness = 0.6, scale: int = 4, pos = (0, 0)) -> None:
        """
        Creates the terrain.

        :param size: The size. Must be in the form 2 ** n + 1.
        :param biome: The biome name.
        :param roughness: Controls the amount of randomness is added to each pixel.
        :param scale: This determines how large the pixels are. Must be an integer greater than 1.
        :param pos: The topleft position of the terrain.
        """
    @overload
    def __init__(self, size, biome: Biome = DEFAULT_BIOME, roughness = 0.6, scale: int = 4, pos = (0, 0)) -> None:
        """
        Creates the terrain.

        :param size: The size. Must be in the form 2 ** n + 1.
        :param biome: The biome name.
        :param roughness: Controls the amount of randomness is added to each pixel.
        :param scale: This determines how large the pixels are. Must be an integer greater than 1.
        :param pos: The topleft position of the terrain.
        """

    def __init__(self, size, biome: Union[str, Biome], roughness = 0.6, scale: int = 4, pos = (0, 0)) -> None:
        if isinstance(biome, Biome):
            biome = biome.name
        if biome not in [b.name for b in _BIOMES]:
            raise TypeError(f"Biome name must be in {list(map(str, _BIOMES))}")

        height_map = diamond_square(size, roughness)

        self.heights = height_map
        """The heights in the height map."""

        self.biome = biome
        """The biome name of the terrain."""

        self.size = size
        """The size of the terrain. Size must be in the form 2 ** n + 1."""

        self.scale = scale
        """The scale of the terrain. This determines how large the pixels are. Must be an integer greater than 1."""

        self.pos = pos
        """The topleft position of the terrain."""

    def draw(self, screen_or_surface: Union[PGZeroScreen, PyGameSurface]):
        """
        Draws the terrain on pgzero or pygame determined by the screen_or_surface parameter.

        :param screen_or_surface: This is the screen in pgzero or a Surface in pygame.
        """
        ox, oy = self.pos
        is_pgzero = not isinstance(screen_or_surface, PyGameSurface)
        for y in range(self.size):
            for x in range(self.size):
                color = height_to_color(self.heights[y][x], self.biome)
                if is_pgzero:
                    screen_or_surface.draw.rect(Rect(ox + x * self.scale, oy + y * self.scale, self.scale, self.scale), color=color)
                else:
                    pygame.draw.rect(screen_or_surface, color, Rect(ox + x * self.scale, oy + y * self.scale, self.scale, self.scale))

    def save_as_img(self, save_path):
        img_width = self.size * self.scale
        img_height = self.size * self.scale
        img = Image.new("RGB", (img_width, img_height))
        pixels = img.load()

        for y in range(self.size):
            for x in range(self.size):
                color = height_to_color(self.heights[y][x], self.biome)

                color = tuple(max(0, min(255, int(c))) for c in color)

                for dy in range(self.scale):
                    for dx in range(self.scale):
                        pixels[x * self.scale + dx, y * self.scale + dy] = color

        img.save(save_path)
        print(f"Image saved as {save_path}")

class PGZeroInteractive:
    """Class for pgzero interactive mode."""
    @overload
    def __init__(self, size, start_biome: str = "default", max_roughness = 1.0,  min_roughness = 0, start_roughness = 0, scale = 4, pos = (0, 0)):
        """
        Creates a interactive mode for pgzero.

        :param size: The size. Must be in the form 2 ** n + 1.
        :param start_biome: The biome name to start on.
        :param max_roughness: The maximum roughness allowed on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
        :param min_roughness: The maximum roughness allowed on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
        :param start_roughness: The starting roughness on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
        :param scale: This determines how large the pixels are. Must be an integer greater than 1.
        :param pos: The topleft position of the interactive terrain.
        """

    @overload
    def __init__(self, size, start_biome: Biome = DEFAULT_BIOME, max_roughness = 1.0,  min_roughness = 0, start_roughness = 0, scale = 4, pos = (0, 0)):
        """
        Creates a interactive mode for pgzero.

        :param size: The size. Must be in the form 2 ** n + 1.
        :param start_biome: The Biome object to start on.
        :param max_roughness: The maximum roughness allowed on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
        :param min_roughness: The maximum roughness allowed on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
        :param start_roughness: The starting roughness on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
        :param scale: This determines how large the pixels are. Must be an integer greater than 1.
        :param pos: The topleft position of the interactive terrain.
        """

    def __init__(self, size, start_biome: Union[str, Biome], max_roughness = 1.0,  min_roughness = 0, start_roughness = 0, scale = 4, pos = (0, 0)):
        if isinstance(start_biome, Biome):
            start_biome = start_biome.name

        state = {
            'roughness': max(min_roughness, min(start_roughness, max_roughness)),
            'biome': start_biome,
            'drag': False,
            'height_map': [],
            'slider_circle_pos': (0, 0),
            'slider_circle_radius': 15
        }

        width = size * scale
        height = size * scale + 50
        
        biomes = [
            ["default", (50, 150, 50), "white"], 
            ["desert", (210, 180, 140), "black"], 
            ["tundra", (200, 200, 255), "black"], 
            ["tropical", (0, 150, 0), "white"], 
            ["volcanic", (60, 0, 0), "white"], 
            ["swamp", (40, 60, 30), "white"], 
            ["ocean", (0, 70, 140), "white"], 
            ["mars", (150, 60, 40), "white"]
        ]

        state['height_map'] = diamond_square(size, state['roughness'])
        
        biome_step = width // len(biomes)
        biome_rects = []
        for i, b in enumerate(biomes):
            r = Rect(i * biome_step, height - 25, biome_step, 25)
            biome_rects.append({'rect': r, 'color': b[1], 'name': b[0], 'txt': b[2]})

        base_slider = Rect(0, height - 50, width, 25)
        
        def update_slider_pos():
            ratio = (state['roughness'] - min_roughness) / (max_roughness - min_roughness)
            x = base_slider.left + ratio * base_slider.width
            state['slider_circle_pos'] = (int(x), base_slider.centery)

        update_slider_pos()

        def draw_func(screen):
            ox, oy = pos
            for y in range(size):
                for x in range(size):
                    color = height_to_color(state['height_map'][y][x], state['biome'])
                    screen.draw.filled_rect(Rect(ox + x * scale, oy + y * scale, scale, scale), color)
            screen.draw.filled_rect(base_slider, "gray")
            screen.draw.filled_circle(state['slider_circle_pos'], state['slider_circle_radius'], "red")
            active_width = (state['roughness'] - min_roughness) / (max_roughness - min_roughness) * base_slider.width
            active_rect = Rect(base_slider.topleft, (active_width, base_slider.height))
            screen.draw.filled_rect(active_rect, "red")
            screen.draw.filled_circle(state['slider_circle_pos'], state['slider_circle_radius'], "white")
            screen.draw.text(f"Roughness: {state['roughness']:.2f}", (10, height - 45), color="white", shadow=(1,1))
            for b in biome_rects:
                screen.draw.filled_rect(b['rect'], b['color'])
                screen.draw.text(b['name'], center=b['rect'].center, color=b['txt'], fontsize=20)
                if b['name'] == state['biome']:
                    screen.draw.rect(b['rect'], "yellow")

        def on_mouse_down_func(p):
            for b in biome_rects:
                if b['rect'].collidepoint(p):
                    state['biome'] = b['name']
                    state['height_map'] = diamond_square(size, state['roughness'])
                    return
            if _point_in_circle(p, state['slider_circle_pos'], state['slider_circle_radius']):
                state['drag'] = True

        def on_mouse_move_func(p):
            if state['drag']:
                val = max(base_slider.left, min(p[0], base_slider.right))
                ratio = (val - base_slider.left) / base_slider.width
                state['roughness'] = min_roughness + ratio * (max_roughness - min_roughness)
                update_slider_pos()
                state['height_map'] = diamond_square(size, state['roughness'])

        def on_mouse_up_func():
            state['drag'] = False

        self.draw_func = draw_func
        """The draw function for the interactive mode. Must be called in your draw function in pgzero."""

        self.on_mouse_down_func = on_mouse_down_func
        """The on_mouse_down function for the interactive mode. Must be called in your on_mouse_down function in pgzero."""

        self.on_mouse_up_func = on_mouse_up_func
        """The on_mouse_up function for the interactive mode. Must be called in your on_mouse_up function in pgzero."""

        self.on_mouse_move_func = on_mouse_move_func
        """The on_mouse_move function for the interactive mode. Must be called in your on_mouse_move function in pgzero."""

class PyGameInteractive:
    """Class for pygame interactive mode."""
    @overload
    def __init__(self, size, start_biome: str = "default", max_roughness = 1.0,  min_roughness = 0, start_roughness = 0, scale = 4, pos = (0, 0)):
        """
        Creates a interactive mode for pygame.

        :param size: The size. Must be in the form 2 ** n + 1.
        :param start_biome: The Biome object to start on.
        :param max_roughness: The maximum roughness allowed on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
        :param min_roughness: The maximum roughness allowed on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
        :param start_roughness: The starting roughness on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
        :param scale: This determines how large the pixels are. Must be an integer greater than 1.
        :param pos: The topleft position of the interactive terrain.
        """
    @overload
    def __init__(self, size, start_biome: Biome = DEFAULT_BIOME, max_roughness = 1.0,  min_roughness = 0, start_roughness = 0, scale = 4, pos = (0, 0)):
        """
        Creates a interactive mode for pygame.

        :param size: The size. Must be in the form 2 ** n + 1.
        :param start_biome: The Biome object to start on.
        :param max_roughness: The maximum roughness allowed on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
        :param min_roughness: The maximum roughness allowed on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
        :param start_roughness: The starting roughness on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
        :param scale: This determines how large the pixels are. Must be an integer greater than 1.
        :param pos: The topleft position of the interactive terrain.
        """

    def __init__(self, size, start_biome: Union[str, Biome], max_roughness = 1.0,  min_roughness = 0, start_roughness = 0, scale = 4, pos = (0, 0)):
        if isinstance(start_biome, Biome):
            start_biome = start_biome.name
        pygame.init()
        pygame.font.init()
        state = {
            'roughness': max(min_roughness, min(start_roughness, max_roughness)),
            'biome': start_biome,
            'drag': False,
            'height_map': [],
            'slider_circle_pos': (0, 0),
            'slider_circle_radius': 15
        }

        width = size * scale
        height = size * scale + 50
        
        biomes = [
            ["default", (50, 150, 50), "white"], 
            ["desert", (210, 180, 140), "black"], 
            ["tundra", (200, 200, 255), "black"], 
            ["tropical", (0, 150, 0), "white"], 
            ["volcanic", (60, 0, 0), "white"], 
            ["swamp", (40, 60, 30), "white"], 
            ["ocean", (0, 70, 140), "white"], 
            ["mars", (150, 60, 40), "white"]
        ]

        state['height_map'] = diamond_square(size, state['roughness'])
        
        biome_step = width // len(biomes)
        biome_rects = []
        for i, b in enumerate(biomes):
            r = Rect(i * biome_step, height - 25, biome_step, 25)
            biome_rects.append({'rect': r, 'color': b[1], 'name': b[0], 'txt': b[2]})

        base_slider = Rect(0, height - 50, width, 25)
        
        def update_slider_pos():
            ratio = (state['roughness'] - min_roughness) / (max_roughness - min_roughness)
            x = base_slider.left + ratio * base_slider.width
            state['slider_circle_pos'] = (int(x), base_slider.centery)

        update_slider_pos()

        def main_function(surface, events):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for b in biome_rects:
                        if b['rect'].collidepoint(event.pos):
                            state['biome'] = b['name']
                            state['height_map'] = diamond_square(size, state['roughness'])
                            return
                    if _point_in_circle(event.pos, state['slider_circle_pos'], state['slider_circle_radius']):
                        state['drag'] = True

                if event.type == pygame.MOUSEMOTION:
                    if state['drag']:
                        val = max(base_slider.left, min(event.pos[0], base_slider.right))
                        ratio = (val - base_slider.left) / base_slider.width
                        state['roughness'] = min_roughness + ratio * (max_roughness - min_roughness)
                        update_slider_pos()
                        state['height_map'] = diamond_square(size, state['roughness'])

                if event.type == pygame.MOUSEBUTTONUP:
                    state['drag'] = False

            ox, oy = pos
            for y in range(size):
                for x in range(size):
                    color = height_to_color(state['height_map'][y][x], state['biome'])
                    pygame.draw.rect(surface, color, Rect(ox + x * scale, oy + y * scale, scale, scale), width = 0)

            font24 = pygame.font.SysFont(None, 24)
            font20 = pygame.font.SysFont(None, 20)
            text = f"Roughness: {state['roughness']:.2f}"
            roughness_text = font24.render(text, True, "white")
            shadow = font24.render(text, True, "black")

            pygame.draw.rect(surface, "gray", base_slider, width = 0)
            pygame.draw.circle(surface, "red", state['slider_circle_pos'], state['slider_circle_radius'])
            active_width = (state['roughness'] - min_roughness) / (max_roughness - min_roughness) * base_slider.width
            active_rect = Rect(base_slider.topleft, (active_width, base_slider.height))
            pygame.draw.rect(surface, "red", active_rect, width = 0)
            pygame.draw.circle(surface, "white", state['slider_circle_pos'], state['slider_circle_radius'])
            surface.blit(roughness_text, (10, height - 45))
            surface.blit(shadow, (11, height - 44))

            for b in biome_rects:
                biome_text = font20.render(b['name'], True, b['txt'])
                rect = biome_text.get_rect(center = b['rect'].center)
                pygame.draw.rect(surface, b["color"], b["rect"], width = 0)
                surface.blit(biome_text, rect)
                if b['name'] == state['biome']:
                    pygame.draw.rect(surface, "yellow", b["rect"], width = 1)

        self.draw = main_function
        """Draws the interactive mode in pygame. Must be called in the main loop."""
