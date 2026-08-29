from .biomes import *
from PIL import Image
import os

class _TerrainSaving:
    """Functions to save 2D terrain as images, and 3D terrain as .stl and .obj. Not meant for user use."""
    @staticmethod
    def save_as_img(size, scale, heights, biome_obj, save_path, filter_func = None, obj = None):
        img_width = size * scale
        img_height = size * scale
        img = Image.new("RGB", (img_width, img_height))
        pixels = img.load()

        if filter_func != None:
            for y in range(size):
                for x in range(size):
                    if filter_func(obj, (x, y)):
                        color = biome_obj.height_to_color(heights[y][x])

                        color = tuple(max(0, min(255, int(c))) for c in color)

                        for dy in range(scale):
                            for dx in range(scale):
                                pixels[x * scale + dx, y * scale + dy] = color
        else:
            for y in range(size):
                for x in range(size):
                    color = biome_obj.height_to_color(heights[y][x])

                    color = tuple(max(0, min(255, int(c))) for c in color)

                    for dy in range(scale):
                        for dx in range(scale):
                            pixels[x * scale + dx, y * scale + dy] = color

        img.save(save_path)

    @staticmethod
    def save_as_stl(obj, filename, filter_func = None):
        cube_facets = [
            ((0, 0, 1), (0, 0, 1), (1, 0, 1), (1, 1, 1)),
            ((0, 0, 1), (0, 0, 1), (1, 1, 1), (0, 1, 1)),
            ((0, 0, -1), (0, 0, 0), (0, 1, 0), (1, 1, 0)),
            ((0, 0, -1), (0, 0, 0), (1, 1, 0), (1, 0, 0)),
            ((0, -1, 0), (0, 0, 0), (1, 0, 0), (1, 0, 1)),
            ((0, -1, 0), (0, 0, 0), (1, 0, 1), (0, 0, 1)),
            ((0, 1, 0), (1, 1, 0), (0, 1, 0), (0, 1, 1)),
            ((0, 1, 0), (1, 1, 0), (0, 1, 1), (1, 1, 1)),
            ((-1, 0, 0), (0, 0, 0), (0, 0, 1), (0, 1, 1)),
            ((-1, 0, 0), (0, 0, 0), (0, 1, 1), (0, 1, 0)),
            ((1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1)),
            ((1, 0, 0), (1, 1, 0), (1, 0, 1), (1, 0, 0))
        ]

        box_width = 0.1 * obj.scale
        box_depth = 0.1 * obj.scale

        with open(filename, 'w') as f:
            f.write("solid terrain\n")

            for y, row in enumerate(obj.height_map):
                for x, h in enumerate(row):
                    world_x = x * obj.scale * 0.05 + obj.pos[0]
                    world_y = y * obj.scale * 0.05 + obj.pos[1]

                    if filter_func and not filter_func(obj, (world_x, world_y)):
                        continue

                    height = obj.biome.height_to_3d(h)
                    x_start = world_x - box_width / 2
                    y_start = world_y - box_depth / 2
                    z_start = obj.pos[2]

                    for normal, v1, v2, v3 in cube_facets:
                        f.write(f"  facet normal {normal[0]} {normal[1]} {normal[2]}\n")
                        f.write("    outer loop\n")
                        for v in (v1, v2, v3):
                            vx = x_start + (v[0] * box_width)
                            vy = y_start + (v[1] * box_depth)
                            vz = z_start + (v[2] * height)
                            f.write(f"      vertex {vx:.6f} {vy:.6f} {vz:.6f}\n")
                        f.write("    endloop\n")
                        f.write("  endfacet\n")

            f.write("endsolid terrain\n")

    @staticmethod
    def save_as_obj(obj, filename: str, filter_func: Callable[[object, tuple[int, int]], bool] | None = None):
        base_name = os.path.splitext(filename)[0]
        obj_path = base_name + ".obj"
        mtl_path = base_name + ".mtl"
        mtl_filename = os.path.basename(mtl_path)

        box_width = 0.1 * obj.scale
        box_depth = 0.1 * obj.scale

        used_colors = {}
        vertices = []
        faces = []

        local_cube_verts = [
            (0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0),
            (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)
        ]

        local_quad_faces = [
            (1, 4, 3, 2),
            (5, 6, 7, 8),
            (1, 2, 6, 5),
            (2, 3, 7, 6),
            (3, 4, 8, 7),
            (4, 1, 5, 8)
        ]

        v_index_counter = 1

        for y, row in enumerate(obj.height_map):
            for x, h in enumerate(row):
                world_x = x * obj.scale * 0.05 + obj.pos[0]
                world_y = y * obj.scale * 0.05 + obj.pos[1]

                if filter_func and not filter_func(obj, (world_x, world_y)):
                    continue

                color = obj.biome.height_to_color(h)  
                height = obj.biome.height_to_3d(h)

                if any(val > 1.0 for val in color[:3]):
                    color = tuple(val / 255.0 for val in color[:3])
                else:
                    color = tuple(color[:3])

                color_key = f"mat_{int(color[0]*255)}_{int(color[1]*255)}_{int(color[2]*255)}"
                if color_key not in used_colors:
                    used_colors[color_key] = color

                x_start = world_x - box_width / 2
                y_start = world_y - box_depth / 2
                z_start = obj.pos[2]

                for vx, vy, vz in local_cube_verts:
                    px = x_start + (vx * box_width)
                    py = y_start + (vy * box_depth)
                    pz = z_start + (vz * height)
                    vertices.append((px, py, pz))

                for quad in local_quad_faces:
                    global_quad = tuple(idx + v_index_counter - 1 for idx in quad)
                    faces.append((color_key, global_quad))

                v_index_counter += 8

        with open(mtl_path, 'w') as mtl_f:
            mtl_f.write("# Terrain Biome Materials\n\n")
            for mat_name, rgb in used_colors.items():
                mtl_f.write(f"newmtl {mat_name}\n")
                mtl_f.write(f"Kd {rgb[0]:.4f} {rgb[1]:.4f} {rgb[2]:.4f}\n")
                mtl_f.write(f"Ka {rgb[0]*0.2:.4f} {rgb[1]*0.2:.4f} {rgb[2]*0.2:.4f}\n")
                mtl_f.write("Illum 2\n\n")

        with open(obj_path, 'w') as obj_f:
            obj_f.write("# Terrain 3D Mesh Export\n")
            obj_f.write(f"mtllib {mtl_filename}\n\n")

            for v in vertices:
                obj_f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")

            current_mat = None
            for mat_name, quad in faces:
                if mat_name != current_mat:
                    obj_f.write(f"\nusemtl {mat_name}\n")
                    current_mat = mat_name
                obj_f.write(f"f {quad[0]} {quad[1]} {quad[2]} {quad[3]}\n")
