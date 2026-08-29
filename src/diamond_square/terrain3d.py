from .core_algorithm import core_diamond_square
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, MouseButton
from .biomes import *
from .filter_funcs import *
from .terrain_saving import _TerrainSaving as _TerrainSaving
import math

def draw_panda3d_box(obj, width, height, depth, pos, color):
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
        self._roughness = roughness
        self.scale = scale
        self.spacing = 0.05 * scale
        self.world_size = self.size * self.spacing
        center = -(self.size * self.spacing) / 2
        z_pos = pos[2] if len(pos) > 2 else 0
        self.pos = (center + pos[0], center + pos[1], z_pos)
        self.height_map = core_diamond_square(self.size, self.roughness)

    @property
    def roughness(self):
        return self._roughness

    @roughness.setter
    def roughness(self, value):
        self._roughness = value
        self.re_generate()

    def draw_panda3d(self, obj, filter_func: Callable[[object, tuple[int, int]], bool] | None = None):
        """
        Draws the 3D terrain in panda3d.

        Parameters
        ----------
        obj
            obj is the panda3d class. When using this function inside a panda3d class, pass the panda3d class `self` into obj.
        filter_func
            Filters the rectangular prisms drawn, so that the output range can be other shapes instead of just a square.
            The filter function should have 2 parameters: obj, pos.
            obj is the Terrain3D self. From obj, you have access to all of the variables in the Terrain3D self.
            pos is the current position of the pixel that it is checking.

            Example::

                def circle_filter(obj, pos):
                    return (pos[0] ** 2 + pos[1] ** 2) <= (obj.world_size / 2) ** 2
                # You have to use world_size instead of size because size is just the dimensions of the height map.
                # world_size is the dimensions of the Terrain3D.

        Return
        ------
        NodePath
            The single object containing all boxes drawn in the terrain.
        """
        terrain_root = obj.render.attachNewNode("Terrain3D")
        if filter_func == None:
            filter_func = lambda obj, pos: True
        original_render = obj.render
        obj.render = terrain_root
        for y, row in enumerate(self.height_map):
            for x, h in enumerate(row):
                world_x = x * self.scale * 0.05 + self.pos[0]
                world_y = y * self.scale * 0.05 + self.pos[1]
                if filter_func(self, (world_x, world_y)):
                    color = self.biome.height_to_color(h)
                    height = self.biome.height_to_3d(h)
                    draw_panda3d_box(obj, 0.1 * self.scale, height, 0.1 * self.scale, (world_x, world_y, self.pos[2]), color)
        obj.render = original_render
        terrain_root.flattenStrong()
        return terrain_root

    def re_generate(self) -> None:
        """Re-Generates the terrain (creates a new height map)."""
        self.height_map = core_diamond_square(self.size, self.roughness)

    def save_as_stl(self, filename: str, filter_func: Callable[[object, tuple[int, int]], bool] | None = None):
        """
        Exports the terrain into a STL file.

        Parameters
        ----------
        filename : str
            The target file path (e.g., 'terrain.stl').
        filter_func : function, optional
            Filters the rectangular prisms drawn, so that the output range can be other shapes instead of just a square.
            The filter function should have 2 parameters: obj, pos. obj is the Terrain3D self. From obj, you have access to all of the variables in the Terrain3D self.
            pos is the current position of the pixel that it is checking.

            Example::

                def circle_filter(obj, pos):
                    return (pos[0] ** 2 + pos[1] ** 2) <= (obj.world_size / 2) ** 2
                    # You have to use world_size instead of size because size is just the dimensions of the height map.
                    # world_size is the dimensions of the Terrain3D.

        Returns
        -------
        Terrain3D
            The terrain that was saved (self).
        """
        _TerrainSaving.save_as_stl(self, filename, filter_func)

    def save_as_obj(self, filename: str, filter_func: Callable[[object, tuple[int, int]], bool] | None = None):
        """
        Exports the terrain data into a colored OBJ file with an MTL file for material/biome colors.

        Parameters
        ----------
        filename : str
            The target file path (e.g., 'terrain.obj').
        filter_func : Callable | None
            Filters the rectangular prisms drawn, so that the output range can be other shapes instead of just a square.
            The filter function should have 2 parameters: obj, pos. obj is the Terrain3D self. From obj, you have access to all of the variables in the Terrain3D self.
            pos is the current position of the pixel that it is checking.
    
            Example::

                def circle_filter(obj, pos):
                    return (pos[0] ** 2 + pos[1] ** 2) <= (obj.world_size / 2) ** 2
                    # You have to use world_size instead of size because size is just the dimensions of the height map.
                    # world_size is the dimensions of the Terrain3D.

        Returns
        -------
        Terrain3D
            The terrain that was saved (self).
        """

        _TerrainSaving.save_as_obj(self, filename, filter_func)
