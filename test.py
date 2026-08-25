from src.diamond_square import *
from direct.showbase.ShowBase import ShowBase

terrain = Terrain3D(2 ** 7 + 1, TROPICAL_BIOME, 0.6, 4)

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, MouseButton
import math
from src.diamond_square import *

class Panda3DBase(ShowBase):
    def __init__(self):
        super().__init__()

        self.disableMouse()

        self.target = Vec3(0, 0, 0)
        self.yaw = 0
        self.pitch = 0
        self.distance = 10
        self.mouse_sensitivity = 100
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
        if self.mouseWatcherNode.isButtonDown(MouseButton.one()):
            if self.mouseWatcherNode.hasMouse():
                mouse = self.mouseWatcherNode.getMouse()

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

class MyGame(Panda3DBase):
    def __init__(self):
        super().__init__()

        terrain.draw_panda3d(self)

app = MyGame()

app.run()
