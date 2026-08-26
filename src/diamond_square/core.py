"""
All functions and classes are accessible through this file.
"""

from .utils import *
from .biomes import *
from .diamond import diamond_square
from .biomes import ADDED_BIOMES as ADDED_BIOMES
from .terrain3d import Terrain3D, Panda3DBase

@overload
def get_average_biome_color(biome: Biome) -> tuple[int, int, int]: ...
@overload
def get_average_biome_color(biome: str) -> tuple[int, int, int]: ...

def get_average_biome_color(biome: Union[Biome, str]) -> tuple[int, int, int]:
    if isinstance(biome, str):
        for added_biome in ADDED_BIOMES:
            if added_biome.name == biome:
                biome = added_biome

    if isinstance(biome, str):
        raise TypeError(f"{biome} biome was not added to ADDED_BIOMES.")

    colors = []
    for i in np.arange(0, 1, 0.001):
       colors.append(biome.height_to_color(i))

    rgb = list(zip(*colors))
    red = sum(rgb[0]) / len(rgb[0])
    green = sum(rgb[1]) / len(rgb[1])
    blue = sum(rgb[2]) / len(rgb[2])

    return (int(red), int(green), int(blue))

def _get_matching_color(bg_color):
    """
    Takes an RGB background and returns a contrasting, matching color 
    tone without using external libraries.
    """
    r, g, b = bg_color

    luminance = (0.299 * r) + (0.587 * g) + (0.114 * b)

    if luminance < 128:
        return (255, 255, 255)
    else:
        return (0, 0, 0)

@overload
def height_to_color(h: float, biome: str = "default") -> tuple[int, int, int]:
    """
    Turns a height value from 0 to 1 into a color using a biome. You may also use biome.height_to_color(h).

    Parameters
    ----------
    **h**: float
        The height value. Must be from 0 to 1.
    **biome**: str
        The name of the biome.

    Returns
    -------
    **color**: tuple[int, int, int]
        The color based on the biome and the height value.
    """
@overload
def height_to_color(h: float, biome: Biome = DEFAULT_BIOME) -> tuple[int, int, int]:
    """
    Turns a height value from 0 to 1 into a color using a biome. You may also use biome.height_to_color(h).

    Parameters
    ----------
    **h**: float
        The height value. Must be from 0 to 1.
    **biome**: Biome
        The Biome object.

    Returns
    -------
    **color**: tuple[int, int, int]
        The color based on the biome and the height value.
    """

def height_to_color(h: float, biome: Union[str, Biome]) -> tuple[int, int, int]:
    if isinstance(biome, Biome):
        return biome.height_to_color(h)

    for b in ADDED_BIOMES:
        if biome == b.name:
            return b.height_to_color(h)

def _point_in_circle(pos: tuple[int, int], center: tuple[int, int], radius: float) -> bool:
    """
    Checks if a point is in a circle. Not meant for user use.

    Parameters
    ----------
    **pos**: tuple[int, int]
        The point to check if it is inside a circle.
    **center**: tuple[int, int]
        The center of the circle.
    **radius**: float
        The radius of the circle.

    Returns
    -------
    **is in circle**: bool
        Returns True if the point is inside or on the circle, and returns False if the point is outside the circle.
    """
    dx = pos[0] - center[0]
    dy = pos[1] - center[1]
    return dx ** 2 + dy ** 2 <= radius ** 2

class Terrain:
    """Class for pgzero and pygame terrains."""
    @overload
    def __init__(self, size: int, biome: str = "default", roughness: float = 0.6, scale: int = 4, pos: tuple[int, int] = (0, 0)) -> None:
        """
        Creates the terrain.

        Parameters
        ----------
        **size**: int
            The size. Must be in the form 2 ** n + 1.
        **biome**: str
            The biome name.
        **roughness**: float
            Controls the amount of randomness is added to each pixel.
        **scale**: int
            This determines how large the pixels are. Must be an integer greater than 1.
        **pos**: tuple[int, int]
            The topleft position of the terrain.

        Raises
        ------
        TypeError
            If the biome is not in the ADDED_BIOMES list.
        """
    @overload
    def __init__(self, size: int, biome: Biome = DEFAULT_BIOME, roughness: float = 0.6, scale: int = 4, pos: tuple[int, int] = (0, 0)) -> None:
        """
        Creates the terrain.

        Parameters
        ----------
        **size**: int
            The size. Must be in the form 2 ** n + 1.
        **biome**: Biome
            The Biome object.
        **roughness**: float
            Controls the amount of randomness is added to each pixel.
        **scale**: int
            This determines how large the pixels are. Must be an integer greater than 1.
        **pos**: tuple[int, int]
            The topleft position of the terrain.

        Raises
        ------
        TypeError
            If the biome is not in the ADDED_BIOMES list.
        """

    def __init__(self, size: int, biome: Union[str, Biome], roughness: float = 0.6, scale: int = 4, pos: tuple[int, int] = (0, 0)) -> None:
        if isinstance(biome, Biome):
            biome_name = biome.name
            """The biome name of the terrain."""
        elif isinstance(biome, str):
            biome_name = biome
            """The biome name of the terrain."""
            for added_biome in ADDED_BIOMES:
                if added_biome.name == biome_name:
                    biome = added_biome
                    """The Biome of the terrain."""
                    break

        if biome_name not in [b.name for b in ADDED_BIOMES]:
            raise TypeError(f"Biome name must be in {list(map(str, ADDED_BIOMES))}")

        self.heights = diamond_square(size, roughness)
        """The heights in the height map."""

        self.biome: str = biome_name
        """The biome name of the terrain."""

        self.biome_obj: Biome = biome
        """The Biome of the terrain."""

        self.size = size
        """The size of the terrain. Size must be in the form 2 ** n + 1."""

        self.scale = scale
        """The scale of the terrain. This determines how large the pixels are. Must be an integer greater than 1."""

        self.pos = pos
        """The topleft position of the terrain."""

        self.roughness = roughness
        """The roughness of the terrain."""

    def draw(self, screen_or_surface) -> None:
        """
        Draws the terrain on pgzero or pygame determined by the screen_or_surface parameter.

        Parameters
        ----------
        **screen_or_surface**: Screen | Surface
            This is the screen in pgzero or a Surface in pygame.
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

    def save_as_img(self, save_path: str):
        """
        Saves the terrain as an image.

        Parameters
        ----------
        **save_path**: str
            The path to save the image to.

        Returns
        -------
        terrain: Terrain
            The terrain that was saved.
        """
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

        return Terrain

    def re_generate(self):
        self.heights = diamond_square(self.size, self.roughness)

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
        if isinstance(start_biome, Biome):
            start_biome = start_biome.name

        self.state = {
            'roughness': max(min_roughness, min(start_roughness, max_roughness)),
            'biome': start_biome,
            'drag': False,
            'height_map': [],
            'slider_circle_pos': (0, 0),
            'slider_circle_radius': 15
        }
        """The current state of the interactive terrain"""

        shift = -50

        self.width = size * scale
        """The width of the interactive terrain."""

        self.height = size * scale + 50
        """The height of the interactive terrain."""

        biomes: list[list[str, tuple[int, int, int], str]] = []
        """The list of biomes to be drawn."""

        for added_biome in ADDED_BIOMES:
            biome_color = get_average_biome_color(added_biome)
            biomes.append([added_biome.name, biome_color, _get_matching_color(biome_color)])

        self.state['height_map'] = diamond_square(size, self.state['roughness'])
        
        biome_step = self.width // len(biomes)
        """The distance btween the biomes rectangles."""
        biome_rects = []
        for i, b in enumerate(biomes):
            r = Rect(i * biome_step + pos[0], self.height - 25 + pos[1] + shift, biome_step, 25)
            biome_rects.append({'rect': r, 'color': b[1], 'name': b[0], 'txt': b[2]})

        base_slider = Rect(pos[0], self.height - 50 + pos[1] + shift, self.width, 25)
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
            for y in range(size):
                for x in range(size):
                    color = height_to_color(self.state['height_map'][y][x], self.state['biome'])
                    screen.draw.filled_rect(Rect(ox + x * scale, oy + y * scale, scale, scale), color)

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
                    self.state['height_map'] = diamond_square(size, self.state['roughness'])
                    return

            if re_generate_button.collidepoint(pos):
                self.state['height_map'] = diamond_square(size, self.state['roughness'])

            if _point_in_circle(pos, self.state['slider_circle_pos'], self.state['slider_circle_radius']):
                self.state['drag'] = True

        def on_mouse_move_func(pos) -> None:
            if self.state['drag']:
                val = max(base_slider.left, min(pos[0], base_slider.right))
                ratio = (val - base_slider.left) / base_slider.width
                self.state['roughness'] = min_roughness + ratio * (max_roughness - min_roughness)
                update_slider_pos()

                self.state['height_map'] = diamond_square(size, self.state['roughness'])

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

        self.width = size * scale
        self.height = size * scale + 50
        
        biomes: list[list[str, tuple[int, int, int], str]] = []
        """The list of biomes to be drawn."""

        for added_biome in ADDED_BIOMES:
            biome_color = get_average_biome_color(added_biome)
            biomes.append([added_biome.name, biome_color, _get_matching_color(biome_color)])

        state['height_map'] = diamond_square(size, state['roughness'])

        biome_step = self.width // len(biomes)
        biome_rects = []
        for i, b in enumerate(biomes):
            r = Rect(i * biome_step + pos[0], self.height + pos[1] - 25, biome_step, 25)
            biome_rects.append({'rect': r, 'color': b[1], 'name': b[0], 'txt': b[2]})

        base_slider = Rect(pos[0], self.height + pos[1] - 50, self.width, 25)

        def update_slider_pos():
            ratio = (state['roughness'] - min_roughness) / (max_roughness - min_roughness)
            x = base_slider.left + ratio * base_slider.width
            state['slider_circle_pos'] = (int(x), base_slider.centery)

        update_slider_pos()

        width_increase = 110
        button_increase = (width_increase - 100) / 2

        bg_rect = Rect(pos[0] - 10, pos[1] - 10, self.width + width_increase - 5, self.height + 20)
        re_generate_button = Rect(pos[0] + self.width + button_increase, pos[1], 80 + button_increase, 50)

        def main_function(surface: PyGameSurface, events: list[PyGameEvent]):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for b in biome_rects:
                        if b['rect'].collidepoint(event.pos):
                            state['biome'] = b['name']
                            state['height_map'] = diamond_square(size, state['roughness'])

                    if _point_in_circle(event.pos, state['slider_circle_pos'], state['slider_circle_radius']):
                        state['drag'] = True

                    if re_generate_button.collidepoint(event.pos):
                        state['height_map'] = diamond_square(size, state['roughness'])

                if event.type == pygame.MOUSEMOTION:
                    if state['drag']:
                        val = max(base_slider.left, min(event.pos[0], base_slider.right))
                        ratio = (val - base_slider.left) / base_slider.width
                        state['roughness'] = min_roughness + ratio * (max_roughness - min_roughness)
                        update_slider_pos()
                        state['height_map'] = diamond_square(size, state['roughness'])

                if event.type == pygame.MOUSEBUTTONUP:
                    state['drag'] = False

            pygame.draw.rect(surface, (100, 100, 100), bg_rect)
            pygame.draw.rect(surface, (20, 20, 20), re_generate_button)

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

            remake_text = font24.render("Remake", True, "white")
            terrain_text = font24.render("Terrain", True, "white")

            pygame.draw.rect(surface, "gray", base_slider, width = 0)
            pygame.draw.circle(surface, "red", state['slider_circle_pos'], state['slider_circle_radius'])
            active_width = (state['roughness'] - min_roughness) / (max_roughness - min_roughness) * base_slider.width
            active_rect = Rect(base_slider.topleft, (active_width, base_slider.height))
            pygame.draw.rect(surface, "red", active_rect, width = 0)
            pygame.draw.circle(surface, "white", state['slider_circle_pos'], state['slider_circle_radius'])
            surface.blit(roughness_text, (10 + pos[0], self.height + pos[1] - 45))
            surface.blit(shadow, (11 + pos[0], self.height + pos[1] - 44))

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
                if b['name'] == state['biome']:
                    pygame.draw.rect(surface, "yellow", b["rect"], width = 1)

        self.draw: Callable[[PyGameSurface, list[PyGameEvent]], None] = main_function
        """Draws the interactive mode in pygame. Must be called in the main loop."""
