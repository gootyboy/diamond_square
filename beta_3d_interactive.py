from src.diamond_square import *
from panda3d.core import TextNode, CardMaker

class Panda3DTerrain3D(Panda3DBase):
    def __init__(self):
        super().__init__()
        self.instructions_visible = True
        self.roughness = 1.0
        self.current_rough = 1.0
        self.current_boxes = None
        self.terrain = Terrain3D(size=2 ** 7 + 1, biome=DEFAULT_BIOME, roughness=self.roughness, scale=5, pos=(0, 0, 0))
        self.current_boxes = self.terrain.draw_panda3d(obj=self)
        self.taskMgr.add(self.draw_loop, "DrawTerrainTask")

        self.key_state = {"arrow_right-down": False, "arrow_left-down": False, "r-down": False}

        self.accept("arrow_right", self.arrow_right_down, extraArgs=[0.05])
        self.accept("arrow_left", self.arrow_left_down, extraArgs=[0.05])
        self.accept("arrow_right-up", self.arrow_right_up)
        self.accept("arrow_left-up", self.arrow_left_up)
        self.accept("r", self.r_key_down)
        self.accept("r-up", self.r_key_up)
        self.accept("mouse1", self.close_instructions)
        self.accept("mouse2", self.close_instructions)
        self.accept("i-up", self.i_key_up)

        all_textbg_cm = CardMaker('ui_rect')
        all_textbg_cm.set_frame(-0.6, 0, -0.25, 0)

        self.all_textbg_rect = self.a2dTopRight.attach_new_node(all_textbg_cm.generate())
        self.all_textbg_rect.set_color(0.0, 0.0, 0.0, 1.0)
        self.all_textbg_rect.hide()

        rough_bg_cm = CardMaker('ui_rect')
        rough_bg_cm.set_frame(-0.6, 0, -0.15, 0)

        self.rough_bg_rect = self.a2dTopRight.attach_new_node(rough_bg_cm.generate())
        self.rough_bg_rect.set_color(0.0, 0.0, 0.0, 1.0)
        self.rough_bg_rect.hide()

        self.roughness_text = TextNode('RoughnessText')
        self.roughness_text.setText(f"Roughness = {self.current_rough}")
        self.roughness_text.setTextColor(1, 1, 1, 1)
        self.roughness_text.setAlign(TextNode.A_right)

        self.rough_text_node = self.a2dTopRight.attachNewNode(self.roughness_text)
        self.rough_text_node.setScale(0.07)
        self.rough_text_node.setPos(-0.05, 0, -0.1) 
        self.rough_text_node.hide()

        self.loading_text = TextNode("LoadingText")
        self.loading_text.setText(f"Generating...")
        self.loading_text.setTextColor(1, 1, 1, 1)
        self.loading_text.setAlign(TextNode.A_right)

        self.loading_text_node = self.a2dTopRight.attachNewNode(self.loading_text)
        self.loading_text_node.setScale(0.07)
        self.loading_text_node.setPos(-0.05, 0, -0.2)

        self.loading_text_node.hide()

        text1 = TextNode("InstructionText")
        text1.setText("KEYS")
        text1.setTextColor(1, 1, 1, 1)
        text1.setAlign(TextNode.ACenter)
        self.instruction1_node = self.aspect2d.attachNewNode(text1)
        self.instruction1_node.setScale(0.2)
        self.instruction1_node.setPos(0, 0, 0.75)

        text2 = TextNode("InstructionText")
        text2.setText("Left Arrow: Decrease Roughness\n\nRight Arrow: Increase Roughness\n\n'r': Re-Generate Terrain\n\n'i': Instructions (this page)\n\n\nClick anywhere on the screen to continue...")
        text2.setTextColor(1, 1, 1, 1)
        text2.setAlign(TextNode.ACenter)
        self.instruction2_node = self.aspect2d.attachNewNode(text2)
        self.instruction2_node.setScale(0.1)
        self.instruction2_node.setPos(0, 0, 0.5)

        self.enable_terrain_blur()

    def i_key_up(self):
        self.instructions_visible = True

    def enable_terrain_blur(self):
        self.current_boxes.setColorScale(0.25, 0.25, 0.25, 1)

    def disable_terrain_blur(self):
        self.current_boxes.clearColorScale()

    def close_instructions(self):
        if self.instructions_visible == False:
            return

        self.instructions_visible = False
        self.disable_terrain_blur()
        self.instruction1_node.hide()
        self.instruction2_node.hide()
        self.rough_text_node.show()
        self.rough_bg_rect.show()

    def arrow_right_down(self, amount):
        if self.instructions_visible == False:
            self.key_state["arrow_right-down"] = True
            self.current_rough += amount
            if self.current_rough < 0.0:
                self.current_rough = 0.0
            if self.current_rough > 1.0:
                self.current_rough = 1.0

    def arrow_left_down(self, amount):
        if self.instructions_visible == False:
            self.key_state["arrow_left-down"] = True
            self.current_rough -= amount
            if self.current_rough < 0.0:
                self.current_rough = 0.0
            if self.current_rough > 1.0:
                self.current_rough = 1.0

    def arrow_right_up(self):
        if self.instructions_visible == False:
            self.key_state["arrow_right-down"] = False
            self.loading_text_node.hide()
            self.all_textbg_rect.hide()
            self.roughness = self.current_rough
            if self.roughness < 0.0:
                self.roughness = 0.0
            if self.roughness > 1.0:
                self.roughness = 1.0

            self.terrain.roughness = self.roughness

            if self.current_boxes:
                self.current_boxes.removeNode()

            self.current_boxes = self.terrain.draw_panda3d(obj=self)

    def arrow_left_up(self):
        if self.instructions_visible == False:
            self.key_state["arrow_left-down"] = False
            self.loading_text_node.hide()
            self.all_textbg_rect.hide()
            self.roughness = self.current_rough
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
            self.loading_text_node.show()
            self.all_textbg_rect.show()
            self.current_rough += 0.05
            if self.current_rough < 0.0:
                self.current_rough = 0.0
            if self.current_rough > 1.0:
                self.current_rough = 1.0
        if self.key_state["arrow_left-down"]:
            self.loading_text_node.show()
            self.all_textbg_rect.show()
            self.current_rough -= 0.05
            if self.current_rough < 0.0:
                self.current_rough = 0.0
            if self.current_rough > 1.0:
                self.current_rough = 1.0
        if self.key_state["r-down"]:
            self.loading_text_node.show()
            self.all_textbg_rect.show()
        if self.instructions_visible:
            self.enable_terrain_blur()
            self.instruction1_node.show()
            self.instruction2_node.show()
            self.rough_text_node.hide()
            self.rough_bg_rect.hide()

        return task.cont

    def r_key_down(self):
        if self.instructions_visible == False:
            self.key_state["r-down"] = True

    def r_key_up(self):
        if self.instructions_visible == False:
            self.key_state["r-down"] = False
            self.loading_text_node.hide()
            self.all_textbg_rect.hide()
            if self.current_boxes:
                self.current_boxes.removeNode()

            self.terrain.re_generate()
            self.current_boxes = self.terrain.draw_panda3d(obj=self)

app = Panda3DTerrain3D()
app.run()
