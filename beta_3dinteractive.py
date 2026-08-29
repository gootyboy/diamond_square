from src.diamond_square import *
from panda3d.core import TextNode

class Panda3DTerrain3D(Panda3DBase):
    def __init__(self):
        super().__init__()
        self.roughness = 1.0
        self.current_rough = 1.0
        self.current_boxes = None
        self.terrain = Terrain3D(size=2 ** 7 + 1, biome=TROPICAL_BIOME, roughness=self.roughness, scale=5, pos=(0, 0, 0))
        self.current_boxes = self.terrain.draw_panda3d(obj=self)
        self.taskMgr.add(self.draw_loop, "DrawTerrainTask")

        self.key_state = {"arrow_right-down": False, "arrow_left-down": False}

        self.accept("arrow_right", self.right_down, extraArgs=[0.1])
        self.accept("arrow_left", self.left_down, extraArgs=[0.1])
        self.accept("arrow_right-up", self.increase_rough, extraArgs=[0.1])
        self.accept("arrow_left-up", self.decrease_rough, extraArgs=[0.1])
        self.accept("r", self.re_generate)

        self.roughness_text = TextNode('roughness text')
        self.roughness_text.setText(f"Roughness = {self.current_rough}")
        self.roughness_text.setTextColor(1, 1, 1, 1)
        self.roughness_text.setAlign(TextNode.A_right)

        text_node_path = self.a2dTopRight.attachNewNode(self.roughness_text)

        text_node_path.setScale(0.07)
        text_node_path.setPos(-0.05, 0, -0.1) 

    def right_down(self, amount):
        self.key_state["arrow_right-down"] = True
        self.current_rough += amount
        if self.current_rough < 0.0:
            self.current_rough = 0.0
        if self.current_rough > 1.0:
            self.current_rough = 1.0

    def left_down(self, amount):
        self.key_state["arrow_left-down"] = True
        self.current_rough = self.current_rough
        if self.current_rough < 0.0:
            self.current_rough = 0.0
        if self.current_rough > 1.0:
            self.current_rough = 1.0

    def increase_rough(self, amount):
        self.key_state["arrow_right-down"] = False
        self.roughness = self.current_rough
        if self.roughness < 0.0:
            self.roughness = 0.0
        if self.roughness > 1.0:
            self.roughness = 1.0

        self.terrain.roughness = self.roughness

        if self.current_boxes:
            self.current_boxes.removeNode()

        self.current_boxes = self.terrain.draw_panda3d(obj=self)

    def decrease_rough(self, amount):
        self.key_state["arrow_left-down"] = False
        self.roughness -= amount
        if self.roughness < 0.0:
            self.roughness = 0.0
        if self.roughness > 1.0:
            self.roughness = 1.0

        self.terrain.roughness = self.roughness

        if self.current_boxes:
            self.current_boxes.removeNode()

        self.current_boxes = self.terrain.draw_panda3d(obj=self)

    def draw_loop(self, task):
        self.roughness_text.setText(f"Roughness: {self.current_rough:.2f}")

        if self.key_state["arrow_right-down"]:
            self.current_rough += 0.1 / 30
            if self.current_rough < 0.0:
                self.current_rough = 0.0
            if self.current_rough > 1.0:
                self.current_rough = 1.0
        if self.key_state["arrow_left-down"]:
            self.current_rough -= 0.1 / 30
            if self.current_rough < 0.0:
                self.current_rough = 0.0
            if self.current_rough > 1.0:
                self.current_rough = 1.0

        return task.cont

    def re_generate(self):
        if self.current_boxes:
            self.current_boxes.removeNode()

        self.terrain.re_generate()
        self.current_boxes = self.terrain.draw_panda3d(obj=self)

# Creating the panda3d app.
app = Panda3DTerrain3D()
# Running the app.
app.run()
