from .utils import *
from .core_algorithm import core_diamond_square
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, MouseButton
from .biomes import *
from .filter_funcs import *

def _panda3d_box(obj, width, height, depth, pos, color):
    rectangle = obj.loader.loadModel("models/box")
    rectangle.reparentTo(obj.render)

    rectangle.setScale(width / 2, depth / 2, height / 2)

    rectangle.setTextureOff(1)

    r, g, b = color
    rectangle.setColor(r / 255, g / 255, b / 255, 1)
    rectangle.setPos(*pos)

    return rectangle

class Panda3DBase(ShowBase):
    """
    Panda3D base class which includes
    
    - zoom in/out
    - rotate
    - move
    """
    def __init__(self):
        super().__init__()
        self.disableMouse()
        
        self.target = Vec3(0, 0, 0)
        self.yaw = 0
        self.pitch = 0
        self.distance = 10
        self.mouse_sensitivity = 100
        self.pan_sensitivity = 100
        
        self.last_mouse = None
        self.draw()
        self.update_camera()
        
        self.accept("wheel_up", self.zoom_in)
        self.accept("wheel_down", self.zoom_out)
        self.taskMgr.add(self.update_mouse, "update_mouse")

    def draw(self):
        pass

    def box(self, width, height, depth, pos, color):
        rectangle = self.loader.loadModel("models/box")
        rectangle.reparentTo(self.render)
        rectangle.setScale(width / 2, depth / 2, height / 2)
        rectangle.setTextureOff(1)
        rectangle.setLightOff()
        r, g, b = color
        rectangle.setColor(r / 255, g / 255, b / 255, 1)
        rectangle.setPos(*pos)
        return rectangle

    def update_mouse(self, task):
        if self.mouseWatcherNode.hasMouse():
            mouse = self.mouseWatcherNode.getMouse()

            if self.mouseWatcherNode.isButtonDown(MouseButton.one()):
                if self.last_mouse is None:
                    self.last_mouse = Vec3(mouse.x, mouse.y, 0)
                else:
                    dx = mouse.x - self.last_mouse.x
                    dy = mouse.y - self.last_mouse.y
                    
                    self.yaw -= dx * self.mouse_sensitivity
                    self.pitch += dy * self.mouse_sensitivity
                    self.pitch = max(-89, min(89, self.pitch))
                    
                    self.update_camera()
                    self.last_mouse = Vec3(mouse.x, mouse.y, 0)

            elif self.mouseWatcherNode.isButtonDown(MouseButton.three()):
                if self.last_mouse is None:
                    self.last_mouse = Vec3(mouse.x, mouse.y, 0)
                else:
                    dx = mouse.x - self.last_mouse.x
                    dy = mouse.y - self.last_mouse.y

                    cam_right = self.render.getRelativeVector(self.camera, Vec3.right())
                    cam_up = self.render.getRelativeVector(self.camera, Vec3.up())

                    pan_speed = self.distance * self.pan_sensitivity * 0.01

                    self.target -= cam_right * dx * pan_speed
                    self.target -= cam_up * dy * pan_speed
                    
                    self.update_camera()
                    self.last_mouse = Vec3(mouse.x, mouse.y, 0)
            else:
                self.last_mouse = None
        else:
            self.last_mouse = None
            
        return task.cont

    def update_camera(self):
        yaw = math.radians(self.yaw)
        pitch = math.radians(self.pitch)
        
        x = math.sin(yaw) * math.cos(pitch)
        y = -math.cos(yaw) * math.cos(pitch)
        z = math.sin(pitch)
        
        position = self.target + Vec3(x, y, z) * self.distance
        self.camera.setPos(position)
        self.camera.lookAt(self.target)

    def zoom_in(self):
        self.distance = max(2, self.distance - 1)
        self.update_camera()

    def zoom_out(self):
        self.distance += 1
        self.update_camera()

class Terrain3D:
    def __init__(self, size, biome: Biome, roughness, scale, pos=(0, 0, 0)):
        """The scale parameter does not have to be a integer ≥ 1. It can be any number > 0."""
        self.size = size
        self.biome = biome
        self.roughness = roughness
        self.scale = scale
        self.spacing = 0.05 * scale
        self.world_size = self.size * self.spacing
        center = -(self.size * self.spacing) / 2
        z_pos = pos[2] if len(pos) > 2 else 0
        self.pos = (center + pos[0], center + pos[1], z_pos)
        self.height_map = core_diamond_square(self.size, self.roughness)

    def draw_panda3d(self, obj):
        """obj is the panda3d class. When using this function inside a panda3d class, pass the panda3d class `self` into obj."""
        for y, row in enumerate(self.height_map):
            for x, h in enumerate(row):
                color = self.biome.height_to_color(h)
                height = self.biome.height_to_3d(h)
                _panda3d_box(obj, 0.1 * self.scale, height, 0.1 * self.scale, (x * self.scale * 0.05 + self.pos[0], y * self.scale * 0.05 + self.pos[1], self.pos[2]), color)

    def draw_filtered_panda3d(self, obj, filter_func):
        """
        Filters the rectangular prisms drawn, so that the output range can be other shapes instead of just a square.

        ***Only works when self.pos = (0, 0, z)***

        Parameters
        ----------
        **obj**: ShowBase
            obj is the panda3d class. When using this function inside a panda3d class, pass the panda3d class `self` into obj.
        **filter_func**: (( obj, pos)) -> bool
            The filter function should have 2 parameters: obj, pos. obj is the Terrain3D self. From obj, you have access to all of the variables in the Terrain3D self.
            pos is the current position of the pixel that it is checking.
    
            Example::

                def circle_filter(obj, pos):
                    return (pos[0] ** 2 + pos[1] ** 2) <= (obj.world_size / 2) ** 2
                    # You have to use world_size instead of size because size is just the dimensions of the height map.
                    # world_size is the dimensions of the Terrain3D.
        """
        for y, row in enumerate(self.height_map):
            for x, h in enumerate(row):
                world_x = x * self.scale * 0.05 + self.pos[0]
                world_y = y * self.scale * 0.05 + self.pos[0]
                if filter_func(self, (world_x, world_y)):
                    color = self.biome.height_to_color(h)
                    height = self.biome.height_to_3d(h)
                    _panda3d_box(obj, 0.1 * self.scale, height, 0.1 * self.scale, (world_x, world_y, self.pos[2]), color)

    def re_generate(self):
        self.height_map = core_diamond_square(self.size, self.roughness)


    def save_as_stl(self, filename: str, filter_func=None):
        """
        Exports the terrain data into an ASCII STL file.
        Generates individual solid 3D blocks mirroring the `_panda3d_box` logic.
        
        Parameters
        ----------
        filename : str
            The target file path (e.g., 'terrain.stl').
        filter_func : function, optional
            A filtering function mirroring `draw_filtered_panda3d`.
        """
        # Define the 12 triangles that make up a standard 3D bounding box
        # Each tuple represents: (normal_vector, vertex1, vertex2, vertex3)
        cube_facets = [
            # Top Face (Z+)
            ((0, 0, 1), (0, 0, 1), (1, 0, 1), (1, 1, 1)),
            ((0, 0, 1), (0, 0, 1), (1, 1, 1), (0, 1, 1)),
            # Bottom Face (Z-)
            ((0, 0, -1), (0, 0, 0), (0, 1, 0), (1, 1, 0)),
            ((0, 0, -1), (0, 0, 0), (1, 1, 0), (1, 0, 0)),
            # Front Face (Y-)
            ((0, -1, 0), (0, 0, 0), (1, 0, 0), (1, 0, 1)),
            ((0, -1, 0), (0, 0, 0), (1, 0, 1), (0, 0, 1)),
            # Back Face (Y+)
            ((0, 1, 0), (1, 1, 0), (0, 1, 0), (0, 1, 1)),
            ((0, 1, 0), (1, 1, 0), (0, 1, 1), (1, 1, 1)),
            # Left Face (X-)
            ((-1, 0, 0), (0, 0, 0), (0, 0, 1), (0, 1, 1)),
            ((-1, 0, 0), (0, 0, 0), (0, 1, 1), (0, 1, 0)),
            # Right Face (X+)
            ((1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1)),
            ((1, 0, 0), (1, 1, 0), (1, 0, 1), (1, 0, 0))
        ]

        box_width = 0.1 * self.scale
        box_depth = 0.1 * self.scale

        with open(filename, 'w') as f:
            f.write("solid terrain\n")

            for y, row in enumerate(self.height_map):
                for x, h in enumerate(row):
                    # Calculate position identical to the draw loops
                    world_x = x * self.scale * 0.05 + self.pos[0]
                    world_y = y * self.scale * 0.05 + self.pos[1] # Fixed typo from original code

                    # Apply geometry filter if provided
                    if filter_func and not filter_func(self, (world_x, world_y)):
                        continue

                    # Calculate precise block boundary variables
                    height = self.biome.height_to_3d(h)
                    
                    # Aligning coordinates with how _panda3d_box typically spaces axes
                    x_start = world_x - box_width / 2
                    y_start = world_y - box_depth / 2
                    z_start = self.pos[2]

                    # Loop through all 12 triangles of the voxel column block
                    for normal, v1, v2, v3 in cube_facets:
                        f.write(f"  facet normal {normal[0]} {normal[1]} {normal[2]}\n")
                        f.write("    outer loop\n")
                        for v in (v1, v2, v3):
                            # Scale the unit vertices to the calculated box sizes
                            vx = x_start + (v[0] * box_width)
                            vy = y_start + (v[1] * box_depth)
                            vz = z_start + (v[2] * height)
                            f.write(f"      vertex {vx:.6f} {vy:.6f} {vz:.6f}\n")
                        f.write("    endloop\n")
                        f.write("  endfacet\n")

            f.write("endsolid terrain\n")

    def save_as_obj(self, filename: str, filter_func=None):
        """
        Exports the terrain data into a colored Wavefront OBJ file 
        with an accompanying MTL file for material/biome colors.
        
        Parameters
        ----------
        filename : str
            The target file path (e.g., 'terrain.obj').
        filter_func : function, optional
            A filtering function mirroring `draw_filtered_panda3d`.
        """
        
        # Split extension to generate paths for both files
        base_name = os.path.splitext(filename)[0]
        obj_path = base_name + ".obj"
        mtl_path = base_name + ".mtl"
        mtl_filename = os.path.basename(mtl_path)

        box_width = 0.1 * self.scale
        box_depth = 0.1 * self.scale

        used_colors = {}  # Tracks unique colors to map them to materials
        vertices = []
        faces = []        # List of tuples: (material_name, (v1, v2, v3, v4))

        # Define 8 local corners of a 3D block unit
        local_cube_verts = [
            (0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0),  # Bottom face vertices
            (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)   # Top face vertices
        ]
        
        # Local vertex index groups for the 6 faces (counter-clockwise orientation)
        local_quad_faces = [
            (1, 4, 3, 2),  # Bottom (Z-)
            (5, 6, 7, 8),  # Top (Z+)
            (1, 2, 6, 5),  # Front (Y-)
            (2, 3, 7, 6),  # Right (X+)
            (3, 4, 8, 7),  # Back (Y+)
            (4, 1, 5, 8)   # Left (X-)
        ]

        v_index_counter = 1

        # Process the heightmap matrix
        for y, row in enumerate(self.height_map):
            for x, h in enumerate(row):
                world_x = x * self.scale * 0.05 + self.pos[0]
                world_y = y * self.scale * 0.05 + self.pos[1]

                # Run custom geometry filters (like your circular terrain filter)
                if filter_func and not filter_func(self, (world_x, world_y)):
                    continue

                # Fetch biome graphics parameters
                color = self.biome.height_to_color(h)  
                height = self.biome.height_to_3d(h)

                # Ensure RGB color values are normalized strictly from 0.0 to 1.0
                if any(val > 1.0 for val in color[:3]):
                    color = tuple(val / 255.0 for val in color[:3])
                else:
                    color = tuple(color[:3])

                # Create a unique material name based on the RGB profile
                color_key = f"mat_{int(color[0]*255)}_{int(color[1]*255)}_{int(color[2]*255)}"
                if color_key not in used_colors:
                    used_colors[color_key] = color

                # Set up local transformations matching your Panda3D bounding box dimensions
                x_start = world_x - box_width / 2
                y_start = world_y - box_depth / 2
                z_start = self.pos[2]

                # Convert the local bounding box to absolute world space
                for vx, vy, vz in local_cube_verts:
                    px = x_start + (vx * box_width)
                    py = y_start + (vy * box_depth)
                    pz = z_start + (vz * height)
                    vertices.append((px, py, pz))

                # Step through faces and append them tracking global indices
                for quad in local_quad_faces:
                    global_quad = tuple(idx + v_index_counter - 1 for idx in quad)
                    faces.append((color_key, global_quad))

                # Increment vertex index stack (8 points per voxel column)
                v_index_counter += 8

        # 1. Write out the Accompanying Material (.mtl) File
        with open(mtl_path, 'w') as mtl_f:
            mtl_f.write("# Terrain Biome Materials\n\n")
            for mat_name, rgb in used_colors.items():
                mtl_f.write(f"newmtl {mat_name}\n")
                mtl_f.write(f"Kd {rgb[0]:.4f} {rgb[1]:.4f} {rgb[2]:.4f}\n")  # Diffuse color
                mtl_f.write(f"Ka {rgb[0]*0.2:.4f} {rgb[1]*0.2:.4f} {rgb[2]*0.2:.4f}\n")  # Ambient reflection
                mtl_f.write("Illum 2\n\n")

        # 2. Write out the Structural Mesh (.obj) File
        with open(obj_path, 'w') as obj_f:
            obj_f.write("# Terrain 3D Mesh Export\n")
            obj_f.write(f"mtllib {mtl_filename}\n\n")
            
            # Print global coordinate points array
            for v in vertices:
                obj_f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
            
            # Group geometry assignments by material to reduce file clutter overhead
            current_mat = None
            for mat_name, quad in faces:
                if mat_name != current_mat:
                    obj_f.write(f"\nusemtl {mat_name}\n")
                    current_mat = mat_name
                obj_f.write(f"f {quad[0]} {quad[1]} {quad[2]} {quad[3]}\n")

