import random
from pgzero.rect import Rect
from typing import overload

class Biome:
    def __init__(self, name, height_to_color_func):
        self.name = name
        self.height_to_color = height_to_color_func

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            other = Biome(other, None)

        return self.name == other.name and self.height_to_color == other.height_to_color

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return f"Biome({repr(self.name)}, {repr(self.height_to_color)})"

class _InteractiveMode:
    def __init__(self, draw_func, on_mouse_down_func, on_mouse_up_func, on_mouse_move_func) -> None:
        """
        Class for setting up an interactive mode of generating terrain. Not meant for user use. Use generate_interactive_terrain(...) to generate the terrain.

        :param draw_func: The function that should be called in the draw() function.
        :param on_mouse_down_func: The function that should be called in the on_mouse_down() function.
        :param on_mouse_up_func: The function that should be called in the on_mouse_up() function.
        :param on_mouse_move_func: The function that should be called in the on_mouse_move() function.
        """
        self.for_draw = draw_func
        self.for_on_mouse_down = on_mouse_down_func
        self.for_on_mouse_up = on_mouse_up_func
        self.for_on_mouse_move = on_mouse_move_func

class _Terrain:
    def __init__(self, height_map = None, biome = None, size = None, scale = None, height_to_color_func = None):
        self.heights = height_map
        self.biome = biome
        self.height_to_color = height_to_color_func
        self.size = size
        self.scale = scale

    def draw(self, screen):
        for y in range(self.size):
            for x in range(self.size):
                color = self.height_to_color(self.heights[y][x], self.biome)
                screen.draw.filled_rect(
                    Rect(x * self.scale, y * self.scale, self.scale, self.scale),
                    color
                )

_BIOMES = []

def _default_func(h):
    if h < 0.2:
        return (0, 0, int(100 + h * 80))
    if h < 0.3:
        return (0, 50, int(150 + h * 80))
    if h < 0.35:
        return (194, 178, 128)
    if h < 0.5:
        return (34, 139, 34)
    if h < 0.6:
        return (0, 100, 0)
    if h < 0.75:
        return (120, 110, 100)
    if h < 0.9:
        return (160, 160, 160)
    return (255, 255, 255)

def _desert_func(h):
    if h < 0.2:
        return (210, 180, 140)
    if h < 0.4:
        return (237, 201, 175)
    if h < 0.6:
        return (194, 178, 128)
    if h < 0.8:
        return (150, 140, 120)
    return (255, 255, 255)

def _tundra_func(h):
    if h < 0.05:
        return (0, 0, 120)
    if h < 0.1:
        return (0, 40, 140)
    if h < 0.3:
        return (150, 150, 150)
    if h < 0.4:
        return (180, 180, 180)
    return (255, 255, 255)

def _tropical_func(h):
    if h < 0.2:
        return (0, 30, 150)
    if h < 0.3:
        return (0, 80, 180)
    if h < 0.4:
        return (240, 220, 130)
    if h < 0.6:
        return (34, 180, 34)
    if h < 0.75:
        return (0, 120, 0)
    return (255, 255, 255) 

def _volcanic_func(h):
    if h < 0.2:
        return (20, 20, 20)
    if h < 0.4:
        return (40, 40, 40)
    if h < 0.6:
        return (80, 0, 0)
    if h < 0.8:
        return (200, 50, 0)
    return (255, 120, 50)

def _swamp_func(h):
    if h < 0.2:
        return (20, 40, 20)
    if h < 0.35:
        return (40, 60, 30)
    if h < 0.5:
        return (70, 90, 50)
    if h < 0.7:
        return (90, 120, 70)
    return (130, 160, 110)

def _ocean_func(h):
    if h < 0.2:
        return (0, 10, 40)
    if h < 0.4:
        return (0, 30, 80)
    if h < 0.6:
        return (0, 60, 120)
    if h < 0.8:
        return (0, 100, 160)
    if h < 0.9:
        return (200, 190, 140)
    return (240, 220, 180)

def _mars_func(h):
    if h < 0.2:
        return (60, 30, 20)
    if h < 0.35:
        return (110, 50, 30)
    if h < 0.55:
        return (160, 70, 40)
    if h < 0.7:
        return (200, 120, 80)
    if h < 0.85:
        return (230, 200, 170)
    return (240, 240, 240)

_BIOMES.append(Biome("default", _default_func))
_BIOMES.append(Biome("desert", _desert_func))
_BIOMES.append(Biome("tundra", _tundra_func))
_BIOMES.append(Biome("tropical", _tropical_func))
_BIOMES.append(Biome("volcanic", _volcanic_func))
_BIOMES.append(Biome("swamp", _swamp_func))
_BIOMES.append(Biome("ocean", _ocean_func))
_BIOMES.append(Biome("mars", _mars_func))

def add_biome(biome: Biome):
    if biome.name in [b.name for b in _BIOMES]:
        raise TypeError(f"\"{biome}\" biome is already in the added biomes list: {list(map(str, _BIOMES))}.")

    _BIOMES.append(biome)

@overload
def remove_biome(biome_name: str):
    ...

@overload
def remove_biome(biome: Biome):
    ...

def remove_biome(arg):
    name = arg if isinstance(arg, str) else arg.name
    for b in _BIOMES:
        if b.name == name:
            _BIOMES.remove(b)
            return
    raise TypeError(f'"{name}" biome is not in the list.')

def _point_in_circle(pos, center, radius):
    dx = pos[0] - center[0]
    dy = pos[1] - center[1]
    return dx ** 2 + dy ** 2 < radius ** 2

def _height_to_color(h, biome="default"):
    for b in _BIOMES:
        if biome == b.name:
            return b.height_to_color(h)

def generate_terrain(roughness, biome, scale, size):
    terrain = _Terrain(biome=biome, size=size, scale=scale)
    if biome not in [b.name for b in _BIOMES]:
        raise TypeError(f"Biome must be in {list(map(str, _BIOMES))}")

    height_map = [[0.0 for i in range(size)] for i in range(size)]
    height_map[0][0] = random.uniform(0, 1)
    height_map[0][size - 1] = random.uniform(0, 1)
    height_map[size - 1][0] = random.uniform(0, 1)
    height_map[size - 1][size - 1] = random.uniform(0, 1)
    step_size = size - 1
    scale = roughness
    while step_size > 1:
        half_step = step_size // 2
        for y in range(half_step, size - 1, step_size):
            for x in range(half_step, size - 1, step_size):
                avg = (
                    height_map[y - half_step][x - half_step] +
                    height_map[y - half_step][x + half_step] +
                    height_map[y + half_step][x - half_step] +
                    height_map[y + half_step][x + half_step]
                ) / 4
                height_map[y][x] = avg + random.uniform(-scale, scale)
        for y in range(0, size, half_step):
            for x in range((y + half_step) % step_size, size, step_size):
                total = 0
                count = 0
                if y - half_step >= 0:
                    total += height_map[y - half_step][x]
                    count += 1
                if y + half_step < size:
                    total += height_map[y + half_step][x]
                    count += 1
                if x - half_step >= 0:
                    total += height_map[y][x - half_step]
                    count += 1
                if x + half_step < size:
                    total += height_map[y][x + half_step]
                    count += 1
                avg = total / count
                height_map[y][x] = avg + random.uniform(-scale, scale)
        step_size //= 2
        scale *= roughness

    min_val = min(min(row) for row in height_map)
    max_val = max(max(row) for row in height_map)
    for y in range(size):
        for x in range(size):
            height_map[y][x] = (height_map[y][x] - min_val) / (max_val - min_val)

    terrain.heights = height_map

    terrain.height_to_color = _height_to_color

    return terrain

def generate_interactive_mode(size, start_biome="default", max_roughness=1.0, scale=4, start_roughness=0):
    state = {
        'roughness': start_roughness,
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

    def diamond_square(sz, rough):
        h_map = [[0.0 for _ in range(sz)] for _ in range(sz)]
        h_map[0][0] = h_map[0][sz-1] = h_map[sz-1][0] = h_map[sz-1][sz-1] = random.random()
        
        step = sz - 1
        s = rough
        while step > 1:
            half = step // 2
            for y in range(half, sz - 1, step):
                for x in range(half, sz - 1, step):
                    avg = (h_map[y-half][x-half] + h_map[y-half][x+half] + 
                           h_map[y+half][x-half] + h_map[y+half][x+half]) / 4
                    h_map[y][x] = avg + random.uniform(-s, s)
            for y in range(0, sz, half):
                for x in range((y + half) % step, sz, step):
                    total, count = 0, 0
                    for dy, dx in [(-half, 0), (half, 0), (0, -half), (0, half)]:
                        if 0 <= y+dy < sz and 0 <= x+dx < sz:
                            total += h_map[y+dy][x+dx]
                            count += 1
                    h_map[y][x] = (total / count) + random.uniform(-s, s)
            step //= 2
            s *= rough

        flat = [item for sublist in h_map for item in sublist]
        mi, ma = min(flat), max(flat)
        return [[(h_map[y][x] - mi) / (ma - mi + 0.0001) for x in range(sz)] for y in range(sz)]

    state['height_map'] = diamond_square(size, state['roughness'])
    
    biome_step = width // len(biomes)
    biome_rects = []
    for i, b in enumerate(biomes):
        r = Rect(i * biome_step, height - 25, biome_step, 25)
        biome_rects.append({'rect': r, 'color': b[1], 'name': b[0], 'txt': b[2]})

    base_slider = Rect(0, height - 50, width, 25)
    
    def update_slider_pos():
        x = base_slider.left + (state['roughness'] / max_roughness) * base_slider.width
        state['slider_circle_pos'] = (int(x), base_slider.centery)

    update_slider_pos()

    def draw_func(screen):
        for y in range(size):
            for x in range(size):
                color = _height_to_color(state['height_map'][y][x], state['biome'])
                screen.draw.filled_rect(Rect(x * scale, y * scale, scale, scale), color)
        
        screen.draw.filled_rect(base_slider, "gray")
        screen.draw.filled_circle(state['slider_circle_pos'], state['slider_circle_radius'], "red")

        active_width = (state['roughness'] / max_roughness) * base_slider.width
        active_rect = Rect(base_slider.topleft, (active_width, base_slider.height))
        screen.draw.filled_rect(active_rect, "red")
        
        screen.draw.filled_circle(state['slider_circle_pos'], state['slider_circle_radius'], "white")
        screen.draw.text(f"Roughness: {state['roughness']:.2f}", (10, height - 45), color="white", shadow=(1,1))
        
        for b in biome_rects:
            screen.draw.filled_rect(b['rect'], b['color'])
            screen.draw.text(b['name'], center=b['rect'].center, color=b['txt'], fontsize=20)
            if b['name'] == state['biome']:
                screen.draw.rect(b['rect'], "yellow")

    def on_mouse_down_func(pos):
        for b in biome_rects:
            if b['rect'].collidepoint(pos):
                state['biome'] = b['name']
                state['height_map'] = diamond_square(size, state['roughness'])
                return

        if _point_in_circle(pos, state['slider_circle_pos'], state['slider_circle_radius']):
            state['drag'] = True

    def on_mouse_move_func(pos):
        if state['drag']:
            val = max(base_slider.left, min(pos[0], base_slider.right))
            state['roughness'] = ((val - base_slider.left) / base_slider.width) * max_roughness
            update_slider_pos()
            state['height_map'] = diamond_square(size, state['roughness'])

    def on_mouse_up_func():
        state['drag'] = False

    return _InteractiveMode(draw_func, on_mouse_down_func, on_mouse_up_func, on_mouse_move_func)
