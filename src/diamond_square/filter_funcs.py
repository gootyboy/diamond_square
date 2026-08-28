from .utils import *

def circle_filter(obj, pos):
    return (pos[0] ** 2 + pos[1] ** 2) <= (obj.world_size / 2) ** 2

def mandelbrot_set_filter(obj, pos):
    x = (pos[0] - obj.pos[0]) / (0.05 * obj.scale)
    y = (pos[1] - obj.pos[1]) / (0.05 * obj.scale)
    max_iterations = 1000
    percent_x = x / ((obj.size) - 1) if (obj.size) > 1 else 0.5
    percent_y = y / ((obj.size) - 1) if (obj.size) > 1 else 0.5
    coord_x = -2.0 + (percent_x * 3.0)
    coord_y = -1.5 + (percent_y * 3.0)

    c = complex(coord_x, coord_y)
    z = 0j
    is_in_set = True
    
    for i in range(max_iterations):
        if abs(z) > 2.0:
            is_in_set = False
            break

        z = z**2 + c

    return is_in_set
