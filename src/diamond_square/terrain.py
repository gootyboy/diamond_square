from .utils import *
from .biomes import *
from .diamond import core_diamond_square

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

        self.heights = core_diamond_square(size, roughness)
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
                color = self.biome_obj.height_to_color(self.heights[y][x])
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
                color = self.biome_obj.height_to_color(self.heights[y][x])

                color = tuple(max(0, min(255, int(c))) for c in color)

                for dy in range(self.scale):
                    for dx in range(self.scale):
                        pixels[x * self.scale + dx, y * self.scale + dy] = color

        img.save(save_path)

        return Terrain

    def re_generate(self):
        self.heights = core_diamond_square(self.size, self.roughness)
