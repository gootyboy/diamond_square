from .utils import *
from .biomes import *
from .core_algorithm import core_diamond_square
from .terrain import *
from .terrain_saving import _TerrainSaving as _TerrainSaving

class PGZeroInteractive:
    """Class for pgzero interactive mode."""
    @overload
    def __init__(self, size: int, start_biome: str = "default", max_roughness: float = 1.0,  min_roughness: float = 0, start_roughness: float = 0, scale: int = 4, pos: tuple[int, int] = (0, 0)) -> None:
        """
        Creates a interactive mode for pgzero.

        Parameters
        ----------
        **size**: int
            The size. Must be in the form 2 ** n + 1.
        **start_biome**: str
            The biome name to start on.
        **max_roughness**: float
            The maximum roughness allowed on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
        **min_roughness**: float
            The maximum roughness allowed on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
        **start_roughness**: float
            The starting roughness on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
        **scale**: int
            This determines how large the pixels are. Must be an integer greater than 1.
        **pos**: tuple[float, float]
            The topleft position of the interactive terrain.
        """
    @overload
    def __init__(self, size: int, start_biome: Biome = DEFAULT_BIOME, max_roughness: float = 1.0, min_roughness: float = 0, start_roughness: float = 0, scale: int = 4, pos: tuple[int, int] = (0, 0)) -> None:
        """
        Creates a interactive mode for pgzero.

        Parameters
        ----------
        **size**: int
            The size. Must be in the form 2 ** n + 1.
        **start_biome**: Biome
            The Biome object to start on.
        **max_roughness**: float
            The maximum roughness allowed on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
        **min_roughness**: float
            The maximum roughness allowed on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
        **start_roughness**: float
            The starting roughness on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
        **scale**: int
            This determines how large the pixels are. Must be an integer greater than 1.
        **pos**: tuple[float, float]
            The topleft position of the interactive terrain.
        """

    def __init__(self, size: int, start_biome: Union[str, Biome], max_roughness: float = 1.0, min_roughness: float = 0, start_roughness: float = 0, scale: int = 4, pos: tuple[int, int] = (0, 0)) -> None:
        if isinstance(start_biome, str):
            start_biome_obj = ADDED_BIOMES.get(f"{start_biome}")
        if isinstance(start_biome, Biome):
            start_biome_obj = start_biome

        if start_biome_obj == None:
            raise TypeError(f"Biome name must be in {list(ADDED_BIOMES.items())}")

        start_biome_name = start_biome_obj.name

        self.state = {
            'roughness': max(min_roughness, min(start_roughness, max_roughness)),
            'biome': start_biome_name,
            'biome_obj': start_biome_obj,
            'drag': False,
            'height_map': [],
            'slider_circle_pos': (0, 0),
            'slider_circle_radius': 15
        }
        """The current state of the interactive terrain"""

        self.scale = scale
        """The scale (how big the pixels are) of the interactive terrain."""

        self._size = size
        """The size of the interactive terrain. Do not change the value of this variable. Use self.size instead of self._size."""

        self.width = self.size * self.scale
        """The width of the interactive terrain."""

        self.height = self.size * self.scale + 50
        """The height of the interactive terrain."""

        biomes: list[list[str, tuple[int, int, int], str]] = []

        for name, added_biome in ADDED_BIOMES.items():
            biome_color = added_biome.get_average_biome_color()

            r, g, b = biome_color

            luminance = (0.299 * r) + (0.587 * g) + (0.114 * b)

            if luminance < 128:
                matching_color = (255, 255, 255)
            else:
                matching_color = (0, 0, 0)
    
            biomes.append([name, biome_color, matching_color, added_biome])

        self.state['height_map'] = core_diamond_square(self.size, self.state['roughness'])
        
        biome_step = self.width // len(biomes)
        biome_rects = []
        for i, b in enumerate(biomes):
            r = Rect(i * biome_step + pos[0], self.height - 25 + pos[1] - 50, biome_step, 25)
            biome_rects.append({'rect': r, 'color': b[1], 'name': b[0], 'txt': b[2], "obj": b[3]})

        base_slider = Rect(pos[0], self.height - 50 + pos[1] - 50, self.width, 25)
        """The slider background rect."""
        
        def update_slider_pos() -> None:
            """
            Function to update the current position of the slider.
            """
            ratio = (self.state['roughness'] - min_roughness) / (max_roughness - min_roughness)
            x = base_slider.left + ratio * base_slider.width
            self.state['slider_circle_pos'] = (int(x), base_slider.centery)

        update_slider_pos()

        width_increase = 110
        button_increase = (width_increase - 100) / 2

        bg_rect = Rect(pos[0] - 10, pos[1] - 10, self.width + width_increase, self.height - 30)
        re_generate_button = Rect(pos[0] + self.width + button_increase, pos[1], 80 + button_increase, 50)

        def draw_func(screen) -> None:
            screen.draw.filled_rect(bg_rect, (100, 100, 100))
            pygame.draw.rect(screen.surface, "white", bg_rect, 5)

            screen.draw.filled_rect(re_generate_button, (20, 20, 20))
            screen.draw.textbox("Remake Terrain", re_generate_button, color="white")

            ox, oy = pos
            for y in range(self.size):
                for x in range(self.size):
                    color = self.state["biome_obj"].height_to_color(self.state['height_map'][y][x])
                    screen.draw.filled_rect(Rect(ox + x * self.scale, oy + y * self.scale, self.scale, self.scale), color)

            screen.draw.filled_rect(base_slider, "gray")
            circle_x, circle_y = self.state['slider_circle_pos']
            screen.draw.filled_circle((circle_x, circle_y), self.state['slider_circle_radius'], "red")

            active_width = (self.state['roughness'] - min_roughness) / (max_roughness - min_roughness) * base_slider.width
            active_rect = Rect(base_slider.topleft, (active_width, base_slider.height))

            screen.draw.filled_rect(active_rect, "red")
            screen.draw.filled_circle(self.state['slider_circle_pos'], self.state['slider_circle_radius'], "white")
            screen.draw.text(f"Roughness: {self.state['roughness']:.2f}", (10 + pos[0], self.height - 95 + pos[1]), color="white", shadow=(1, 1))
 
            for b in biome_rects:
                screen.draw.filled_rect(b['rect'], b['color'])
                screen.draw.text(b['name'], center=b['rect'].center, color=b['txt'], fontsize=20)
                if b['name'] == self.state['biome']:
                    screen.draw.rect(b['rect'], "yellow")

        def on_mouse_down_func(pos) -> None:
            for b in biome_rects:
                if b['rect'].collidepoint(pos):
                    self.state['biome'] = b['name']
                    self.state['biome_obj'] = b['obj']
                    self.state['height_map'] = core_diamond_square(self.size, self.state['roughness'])
                    return

            if re_generate_button.collidepoint(pos):
                self.state['height_map'] = core_diamond_square(self.size, self.state['roughness'])

            dx = pos[0] - self.state["slider_circle_pos"][0]
            dy = pos[1] - self.state["slider_circle_pos"][1]
            point_in_circle = dx ** 2 + dy ** 2 <= self.state["slider_circle_radius"] ** 2

            if point_in_circle:
                self.state['drag'] = True

        def on_mouse_move_func(pos) -> None:
            if self.state['drag']:
                val = max(base_slider.left, min(pos[0], base_slider.right))
                ratio = (val - base_slider.left) / base_slider.width
                self.state['roughness'] = min_roughness + ratio * (max_roughness - min_roughness)
                update_slider_pos()

                self.state['height_map'] = core_diamond_square(self.size, self.state['roughness'])

        def on_mouse_up_func() -> None:
            self.state['drag'] = False

        self.draw_func = draw_func
        """The draw function for the interactive mode. Must be called in your draw function in pgzero."""

        self.on_mouse_down_func = on_mouse_down_func
        """The on_mouse_down function for the interactive mode. Must be called in your on_mouse_down function in pgzero."""

        self.on_mouse_up_func = on_mouse_up_func
        """The on_mouse_up function for the interactive mode. Must be called in your on_mouse_up function in pgzero."""

        self.on_mouse_move_func = on_mouse_move_func
        """The on_mouse_move function for the interactive mode. Must be called in your on_mouse_move function in pgzero."""

    @property
    def size(self):
        """The size of the interactive terrain. Size must be in the form 2 ** n + 1."""
        return self._size

    @size.setter
    def size(self, value):
        """Sets the size of the interactive terrain. Size must be in the form 2 ** n + 1."""
        self._size = value
        self.re_generate_terrain()

    def re_generate_terrain(self):
        self.state["height_map"] = core_diamond_square(self.size, self.state['roughness'])

    def save_as_img(self, save_path: str):
        """
        Saves the interactive terrain as an image.

        Parameters
        ----------
        **save_path**: str
            The path to save the image to.
        """
        _TerrainSaving.save_as_img(self.size, self.scale, self.state["height_map"], self.state["biome_obj"], save_path)

class PyGameInteractive:
    """Class for pygame interactive mode."""
    @overload
    def __init__(self, size: int, start_biome: str = "default", max_roughness: float = 1.0,  min_roughness: float = 0, start_roughness: float = 0, scale: int = 4, pos: tuple[int, int] = (0, 0)) -> None:
        """
        Creates a interactive mode for pygame.

        Parameters
        ----------
        **size**: int
            The size. Must be in the form 2 ** n + 1.
        **start_biome**: str
            The biome name to start on.
        **max_roughness**: float
            The maximum roughness allowed on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
        **min_roughness**: float
            The maximum roughness allowed on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
        **start_roughness**: float
            The starting roughness on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
        **scale**: int
            This determines how large the pixels are. Must be an integer greater than 1.
        **pos**: tuple[int, int]
            The topleft position of the interactive terrain.
        """
    @overload
    def __init__(self, size: int, start_biome: Biome = DEFAULT_BIOME, max_roughness: float = 1.0,  min_roughness: float = 0, start_roughness: float = 0, scale: int = 4, pos: tuple[int, int] = (0, 0)) -> None:
        """
        Creates a interactive mode for pygame.

        Parameters
        ----------
        **size**: int
            The size. Must be in the form 2 ** n + 1.
        **start_biome**: Biome
            The biome object to start on.
        **max_roughness**: float
            The maximum roughness allowed on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
        **min_roughness**: float
            The maximum roughness allowed on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
        **start_roughness**: float
            The starting roughness on the roughness slider. Roughness controls the amount of randomness is added to each pixel.
        **scale**: int
            This determines how large the pixels are. Must be an integer greater than 1.
        **pos**: tuple[int, int]
            The topleft position of the interactive terrain.
        """

    def __init__(self, size: int, start_biome: Union[str, Biome], max_roughness: float = 1.0,  min_roughness: float = 0, start_roughness: float = 0, scale: int = 4, pos: tuple[int, int] = (0, 0)) -> None:
        if isinstance(start_biome, str):
            start_biome_obj = ADDED_BIOMES.get(f"{start_biome}")
        if isinstance(start_biome, Biome):
            start_biome_obj = start_biome

        if start_biome_obj == None:
            raise TypeError(f"Biome name must be in {list(ADDED_BIOMES.items())}")

        start_biome_name = start_biome_obj.name

        self.pos = pos

        pygame.init()
        pygame.font.init()

        self.state = {
            'roughness': max(min_roughness, min(start_roughness, max_roughness)),
            'biome': start_biome_name,
            'biome_obj': start_biome_obj,
            'drag': False,
            'height_map': [],
            'slider_circle_pos': (0, 0),
            'slider_circle_radius': 15
        }

        self.scale = scale
        """The scale (how big the pixels are) of the interactive terrain."""

        self._size = size
        """The size of the interactive terrain. Do not change the value of this variable. Use self.size instead of self._size."""

        self.width = self.size * self.scale
        """The width of the interactive terrain."""
        self.height = self.size * self.scale + 50
        """The height of the interactive terrain."""
        
        biomes: list[list[str, tuple[int, int, int], str]] = []
        """The list of biomes to be drawn."""

        for name, added_biome in ADDED_BIOMES.items():
            biome_color = added_biome.get_average_biome_color()

            r, g, b = biome_color

            luminance = (0.299 * r) + (0.587 * g) + (0.114 * b)

            if luminance < 128:
                matching_color = (255, 255, 255)
            else:
                matching_color = (0, 0, 0)

            biomes.append([name, biome_color, matching_color, added_biome])

        self.state['height_map'] = core_diamond_square(self.size, self.state['roughness'])

        biome_step = self.width // len(biomes)
        biome_rects = []
        for i, b in enumerate(biomes):
            r = Rect(i * biome_step + self.pos[0], self.height + self.pos[1] - 25, biome_step, 25)
            biome_rects.append({'rect': r, 'color': b[1], 'name': b[0], 'txt': b[2], "obj": b[3]})

        base_slider = Rect(self.pos[0], self.height + self.pos[1] - 50, self.width, 25)

        def update_slider_pos():
            ratio = (self.state['roughness'] - min_roughness) / (max_roughness - min_roughness)
            x = base_slider.left + ratio * base_slider.width
            self.state['slider_circle_pos'] = (int(x), base_slider.centery)

        update_slider_pos()

        width_increase = 110
        button_increase = (width_increase - 100) / 2

        bg_rect = Rect(self.pos[0] - 10, self.pos[1] - 10, self.width + width_increase - 5, self.height + 20)
        re_generate_button = Rect(self.pos[0] + self.width + button_increase, self.pos[1], 80 + button_increase, 50)

        def main_function(surface: PyGameSurface, events: list[PyGameEvent]):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for b in biome_rects:
                        if b['rect'].collidepoint(event.pos):
                            self.state['biome'] = b['name']
                            self.state["biome_obj"] = b["obj"]
                            self.state['height_map'] = core_diamond_square(self.size, self.state['roughness'])

                    dx = event.pos[0] - self.state["slider_circle_pos"][0]
                    dy = event.pos[1] - self.state["slider_circle_pos"][1]
                    point_in_circle = dx ** 2 + dy ** 2 <= self.state["slider_circle_radius"] ** 2

                    if point_in_circle:
                        self.state['drag'] = True

                    if re_generate_button.collidepoint(event.pos):
                        self.state['height_map'] = core_diamond_square(self.size, self.state['roughness'])

                if event.type == pygame.MOUSEMOTION:
                    if self.state['drag']:
                        val = max(base_slider.left, min(event.pos[0], base_slider.right))
                        ratio = (val - base_slider.left) / base_slider.width
                        self.state['roughness'] = min_roughness + ratio * (max_roughness - min_roughness)
                        update_slider_pos()
                        self.state['height_map'] = core_diamond_square(self.size, self.state['roughness'])

                if event.type == pygame.MOUSEBUTTONUP:
                    self.state['drag'] = False

            pygame.draw.rect(surface, (100, 100, 100), bg_rect)
            pygame.draw.rect(surface, (20, 20, 20), re_generate_button)

            ox, oy = self.pos
            for y in range(self.size):
                for x in range(self.size):
                    color = self.state["biome_obj"].height_to_color(self.state['height_map'][y][x])
                    pygame.draw.rect(surface, color, Rect(ox + x * self.scale, oy + y * self.scale, self.scale, self.scale), width = 0)

            font24 = pygame.font.SysFont(None, 24)
            font20 = pygame.font.SysFont(None, 20)
            text = f"Roughness: {self.state['roughness']:.2f}"
            roughness_text = font24.render(text, True, "white")
            shadow = font24.render(text, True, "black")

            remake_text = font24.render("Remake", True, "white")
            terrain_text = font24.render("Terrain", True, "white")

            pygame.draw.rect(surface, "gray", base_slider, width = 0)
            pygame.draw.circle(surface, "red", self.state['slider_circle_pos'], self.state['slider_circle_radius'])
            active_width = (self.state['roughness'] - min_roughness) / (max_roughness - min_roughness) * base_slider.width
            active_rect = Rect(base_slider.topleft, (active_width, base_slider.height))
            pygame.draw.rect(surface, "red", active_rect, width = 0)
            pygame.draw.circle(surface, "white", self.state['slider_circle_pos'], self.state['slider_circle_radius'])
            surface.blit(roughness_text, (10 + self.pos[0], self.height + self.pos[1] - 45))
            surface.blit(shadow, (11 + self.pos[0], self.height + self.pos[1] - 44))

            remake_text_rect = remake_text.get_rect()
            remake_text_rect.midtop = (re_generate_button.midtop[0], re_generate_button.midtop[1] + 5)
            terrain_text_rect = terrain_text.get_rect()
            terrain_text_rect.midbottom = (re_generate_button.midbottom[0], re_generate_button.midbottom[1] - 5)

            surface.blit(remake_text, remake_text_rect)
            surface.blit(terrain_text, terrain_text_rect)

            for b in biome_rects:
                biome_text = font20.render(b['name'], True, b['txt'])
                rect = biome_text.get_rect(center = b['rect'].center)
                pygame.draw.rect(surface, b["color"], b["rect"], width = 0)
                surface.blit(biome_text, rect)
                if b['name'] == self.state['biome']:
                    pygame.draw.rect(surface, "yellow", b["rect"], width = 1)

        self.draw: Callable[[PyGameSurface, list[PyGameEvent]], None] = main_function
        """Draws the interactive mode in pygame. Must be called in the main loop."""

    @property
    def size(self):
        """The size of the interactive terrain. Size must be in the form 2 ** n + 1."""
        return self._size

    @size.setter
    def size(self, value):
        """Sets the size of the interactive terrain. Size must be in the form 2 ** n + 1."""
        self._size = value
        self.re_generate_terrain()

    def re_generate_terrain(self):
        self.state["height_map"] = core_diamond_square(self.size, self.state['roughness'])

    def save_as_img(self, save_path: str):
        """
        Saves the interactive terrain as an image.

        Parameters
        ----------
        **save_path**: str
            The path to save the image to.
        """
        _TerrainSaving.save_as_img(self.size, self.scale, self.state["height_map"], self.state["biome_obj"], save_path)
