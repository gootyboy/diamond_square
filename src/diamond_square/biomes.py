"""
This file has the Biome class, add_biome and remove_biome function, and 8 in-built biomes
"""

from .utils import *
from .biome_htc_funcs import *

ADDED_BIOMES: list[Biome] = []
"""This is the list of the biome names. Do not update or change this list."""

class Biome:
    """Class to create new biomes."""
    def __init__(self, name: str, htc_func: Callable[[float], tuple[int, int, int]]) -> None:
        """
        Creates a new biome.

        Parameters
        ----------
        **name**: str
            The name of the biome.

        htc_func (( float)) -> tuple[int, int, int]
            A function that maps a height value to a color. The function must have
            the following form::

                def height_to_color(h: float) -> float[int, int, int]:
                    if h < ...: # float between 0 and 1
                        return ... # RGB tuple
                    elif h < ...: # float between 0 and 1
                        return ... # RGB tuple
                    ...
                    else:
                        return ... # RGB tuple
                # The function should return a RGB Tuple. Strings or Hex codes will not work.
        """

        self.name = name
        """The name of the Biome."""

        self.height_to_color = htc_func
        """The height to color function."""

    def __str__(self) -> str:
        """
        String representation of the Biome. Returns the name of the Biome.

        Returns
        -------
        **Name**: str
            The name of the biome.
        """
        return self.name

    def __repr__(self) -> str:
        """
        Returns the representation of the Biome.

        Returns
        -------
        **Representation**: str
            The representation of the Biome.

        """
        return f"Biome({repr(self.name)}, {repr(self.height_to_color)})"

    def add_to_biomes(self) -> Biome:
        """
        Adds a Biome to the list of biomes so that it can be used in a terrain.

        Returns
        ------
        biome: Biome
            The biome that was added.

        Raises
        ------
        **TypeError**
            If there already exists another biome with the same name as the biome parameter.
        """
        return add_biome(self)

    def remove_from_biomes(self) -> Biome:
        """
        Removes a Biome to the list of biomes.

        Returns
        ------
        biome: Biome
            The biome that was added.

        Raises
        ------
        **TypeError**
            If the biome is not already added.
        """
        return remove_biome(self)

@overload
def add_biome(biome: Biome) -> Biome:
    """
    Adds a Biome to the list of biomes so that it can be used in a terrain.

    Parameters
    ---------
    **biome**: Biome
        The biome to add.

    Returns
    ------
    biome: Biome
        The biome that was added.

    Raises
    ------
    **TypeError**:
        If there already exists another biome with the same name as the biome parameter.
    """
@overload
def add_biome(biome_name: str, htc_func: Callable[[float], tuple[int, int, int]]) -> Biome:
    """
    Adds a Biome to the list of biomes so that it can be used in a terrain.

    Parameters
    ---------
    **biome_name**: str
        The name of the biome to add.
    **htc_func** (( float)) -> tuple[int, int, int]
        The height to color function.

    Returns
    ------
    biome: Biome
        The biome that was added.

    Raises
    ------
    **TypeError**:
        If there already exists another biome with the same name as the biome_name parameter.
    """

def add_biome(*args: Union[Biome, str, Callable[[float], tuple[int, int, int]]]) -> Biome:
    if len(args) == 1:
        biome = args[0]
    elif len(args) == 2:
        name, htc = args
        biome = Biome(name, htc)

    if biome.name in [b.name for b in ADDED_BIOMES]:
        raise TypeError(f"You cannot add a biome with the same name as another biome in the added biomes list: {list(map(str, ADDED_BIOMES))}.")

    ADDED_BIOMES.append(biome)
    return biome

DEFAULT_BIOME = Biome("default", default_biome_htc)
"""The default Biome."""

DESERT_BIOME = Biome("desert", desert_biome_htc)
"""The desert Biome."""

TUNDRA_BIOME = Biome("tundra", tundra_biome_htc)
"""The tundra Biome."""

TROPICAL_BIOME = Biome("tropical", tropical_biome_htc)
"""The tropical Biome."""

VOLCANIC_BIOME = Biome("volcanic", volcanic_biome_htc)
"""The volcanic Biome."""

SWAMP_BIOME = Biome("swamp", swamp_biome_htc)
"""The swamp Biome."""

OCEAN_BIOME = Biome("ocean", ocean_biome_htc)
"""The ocean Biome."""

MARS_BIOME = Biome("mars", mars_biome_htc)
"""The mars Biome."""

DEFAULT_BIOME.add_to_biomes()
DESERT_BIOME.add_to_biomes()
TUNDRA_BIOME.add_to_biomes()
TROPICAL_BIOME.add_to_biomes()
VOLCANIC_BIOME.add_to_biomes()
SWAMP_BIOME.add_to_biomes()
OCEAN_BIOME.add_to_biomes()
MARS_BIOME.add_to_biomes()

@overload
def remove_biome(biome: str) -> Biome:
    """
    Removes a biome from the list of biomes so that it cannot be used in any terrains.

    Parameters
    ----------
    **biome**: str
        The name of the biome to remove.

    Returns
    ------
    biome: Biome
        The biome that was removed.

    Raises
    ------
    TypeError
        If the biome was not already added.
    """
@overload
def remove_biome(biome: Biome) -> Biome:
    """
    Removes a biome from the list of biomes so that it cannot be used in any terrains.

    Parameters
    ----------
    **biome**: str
        The Biome object to remove.

    Returns
    ------
    biome: Biome
        The biome that was removed.

    Raises
    ------
    TypeError
        If the biome was not already added.
    """

def remove_biome(biome: Union[str, Biome]) -> Biome:
    if isinstance(biome, Biome):
        biome = biome.name
    for b in ADDED_BIOMES:
        if b.name == biome:
            ADDED_BIOMES.remove(b)
            return b

    raise TypeError(f'"{biome}" biome is not in the list. Biomes must be added before they can be removed.')
