from src.diamond_square import *
from panda3d.core import TextNode, CardMaker

class Panda3DTerrain3D(Panda3DBase):
    def __init__(self):
        super().__init__()

        self.current_biome_index = 0
        self.arrow_right_counter = 0
        self.arrow_left_counter = 0
        self.instructions_visible = True
        self.roughness = 1.0
        self.current_rough = 1.0
        self.current_boxes = None
        self.terrain = Terrain3D(size=2 ** 7 + 1, biome=ADDED_BIOMES.biomes()[self.current_biome_index], roughness=self.roughness, scale=5, pos=(0, 0, 0))
        self.current_boxes = self.terrain.draw_panda3d(obj=self)
        self.taskMgr.add(self._draw_loop, "DrawTerrainTask")
        self.key_state = {"arrow_right-down": False, "arrow_left-down": False, "r-down": False}

        all_textbg_cm = CardMaker('ui_rect')
        all_textbg_cm.set_frame(-1, 0, -0.35, 0)
        self.all_textbg_rect = self.a2dTopRight.attach_new_node(all_textbg_cm.generate())
        self.all_textbg_rect.set_color(0.0, 0.0, 0.0, 1.0)
        self.all_textbg_rect.hide()

        no_loading_cm = CardMaker('ui_rect')
        no_loading_cm.set_frame(-1, 0, -0.25, 0)
        self.no_loading_bg_rect = self.a2dTopRight.attach_new_node(no_loading_cm.generate())
        self.no_loading_bg_rect.set_color(0.0, 0.0, 0.0, 1.0)
        self.no_loading_bg_rect.hide()

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
        self.loading_text_node.setPos(-0.05, 0, -0.3)
        self.loading_text_node.hide()

        self.biome_text = TextNode('BiomeText')
        self.biome_text.setText(f"Biome ({self.current_biome_index}/{len(ADDED_BIOMES.biomes()) - 1}): {ADDED_BIOMES.names()[self.current_biome_index]}")
        self.biome_text.setTextColor(1, 1, 1, 1)
        self.biome_text.setAlign(TextNode.A_right)
        self.biome_text_node = self.a2dTopRight.attachNewNode(self.biome_text)
        self.biome_text_node.setScale(0.07)
        self.biome_text_node.setPos(-0.05, 0, -0.2)

        text1 = TextNode("InstructionText")
        text1.setText("KEYS")
        text1.setTextColor(1, 1, 1, 1)
        text1.setAlign(TextNode.ACenter)
        self.instruction1_node = self.aspect2d.attachNewNode(text1)
        self.instruction1_node.setScale(0.2)
        self.instruction1_node.setPos(0, 0, 0.75)

        instructions = ["Left Arrow: Decrease Roughness", "Right Arrow: Increase Roughness", "Up arrow: Increase Biome index", "Down arrow: Decrease Biome index", "'r': Re-Generate Terrain", "'i': Instructions (this page)", "\nClick anywhere on the screen to continue..."]
        text2 = TextNode("InstructionText")
        text2.setText("\n\n".join(instructions))
        text2.setTextColor(1, 1, 1, 1)
        text2.setAlign(TextNode.ACenter)
        self.instruction2_node = self.aspect2d.attachNewNode(text2)
        self.instruction2_node.setScale(0.1)
        self.instruction2_node.setPos(0, 0, 0.5)

        self._enable_terrain_dark()

        self.accept("arrow_right", self._arrow_right_down, extraArgs=[0.05])
        self.accept("arrow_left", self._arrow_left_down, extraArgs=[0.05])
        self.accept("arrow_right-up", self._arrow_right_up)
        self.accept("arrow_left-up", self._arrow_left_up)
        self.accept("r", self._r_key_down)
        self.accept("r-up", self._r_key_up)
        self.accept("mouse1", self._close_instructions)
        self.accept("mouse2", self._close_instructions)
        self.accept("i-up", self._i_key_up)
        self.accept("arrow_up-up", self._arrow_up_up)
        self.accept("arrow_down-up", self._arrow_down_up)

    def _get_dimensions(node_path):
        pt1, pt2 = node_path.getTightBounds()

        width = pt2.getX() - pt1.getX()
        height = pt2.getY() - pt1.getY()
        depth = pt2.getZ() - pt1.getZ()
        return width, height, depth

    def _arrow_up_up(self):
        self.current_biome_index += 1
        if self.current_biome_index < 0:
            self.current_biome_index = 0
        if self.current_biome_index > len(ADDED_BIOMES.biomes()) - 1:
            self.current_biome_index = len(ADDED_BIOMES.biomes()) - 1

        if self.current_boxes:
            self.current_boxes.removeNode()

        biome = ADDED_BIOMES.biomes()[self.current_biome_index]
        self.terrain.biome = biome
        self.terrain.re_generate()
        self.current_boxes = self.terrain.draw_panda3d(obj=self)

    def _arrow_down_up(self):
        self.current_biome_index -= 1
        if self.current_biome_index < 0:
            self.current_biome_index = 0
        if self.current_biome_index > len(ADDED_BIOMES.biomes()) - 1:
            self.current_biome_index = len(ADDED_BIOMES.biomes()) - 1

        if self.current_boxes:
            self.current_boxes.removeNode()

        biome = ADDED_BIOMES.biomes()[self.current_biome_index]
        self.terrain.biome = biome
        self.terrain.re_generate()
        self.current_boxes = self.terrain.draw_panda3d(obj=self)

    def _i_key_up(self):
        self.instructions_visible = True

    def _enable_terrain_dark(self):
        self.current_boxes.setColorScale(0.25, 0.25, 0.25, 1)

    def _disable_terrain_dark(self):
        self.current_boxes.clearColorScale()

    def _close_instructions(self):
        if self.instructions_visible == False:
            return

        self.instructions_visible = False
        self._disable_terrain_dark()
        self.instruction1_node.hide()
        self.instruction2_node.hide()
        self.rough_text_node.show()
        self.no_loading_bg_rect.show()

    def _arrow_right_down(self, amount):
        if self.instructions_visible == False:
            self.key_state["arrow_right-down"] = True
            self.current_rough += amount
            if self.current_rough < 0.0:
                self.current_rough = 0.0
            if self.current_rough > 1.0:
                self.current_rough = 1.0

    def _arrow_left_down(self, amount):
        if self.instructions_visible == False:
            self.key_state["arrow_left-down"] = True
            self.current_rough -= amount
            if self.current_rough < 0.0:
                self.current_rough = 0.0
            if self.current_rough > 1.0:
                self.current_rough = 1.0

    def _arrow_right_up(self):
        self.arrow_right_counter = 0
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

    def _arrow_left_up(self):
        self.arrow_left_counter = 0
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

    def _draw_loop(self, task):
        self.biome_text.setText(f"Biome ({self.current_biome_index}/{len(ADDED_BIOMES.biomes()) - 1}): {ADDED_BIOMES.names()[self.current_biome_index]}")
        if self.instructions_visible == False:
            self.roughness_text.setText(f"Roughness: {self.current_rough:.2f}")

            if self.key_state["arrow_right-down"]:
                self.arrow_right_counter += 1
                self.loading_text_node.show()
                self.all_textbg_rect.show()
                if self.arrow_right_counter > 30:
                    self.current_rough += 0.01
                    if self.current_rough < 0.0:
                        self.current_rough = 0.0
                    if self.current_rough > 1.0:
                        self.current_rough = 1.0
            if self.key_state["arrow_left-down"]:
                self.arrow_left_counter += 1
                self.loading_text_node.show()
                self.all_textbg_rect.show()
                if self.arrow_left_counter > 30:
                    self.current_rough -= 0.01
                    if self.current_rough < 0.0:
                        self.current_rough = 0.0
                    if self.current_rough > 1.0:
                        self.current_rough = 1.0
            if self.key_state["r-down"]:
                self.loading_text_node.show()
                self.all_textbg_rect.show()
        if self.instructions_visible:
            self._enable_terrain_dark()
            self.instruction1_node.show()
            self.instruction2_node.show()
            self.rough_text_node.hide()
            self.no_loading_bg_rect.hide()

        return task.cont

    def _r_key_down(self):
        if self.instructions_visible == False:
            self.key_state["r-down"] = True

    def _r_key_up(self):
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
