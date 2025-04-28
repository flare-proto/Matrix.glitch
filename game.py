import luma,levels
from pygame_light2d import LightingEngine

screen_res = (1500, 900)
native_res = (1500, 900)

class Game:
    def __init__(self):
        self.lights_engine = LightingEngine(
            screen_res=screen_res, native_res=native_res, lightmap_res=native_res
        )
        self.lights_engine.set_ambient(30, 30, 30, 30)
        
        self.engine = self.lights_engine.graphics
        self.final_layer = self.engine.make_layer(screen_res)

        self.lights_engine.light_output_target =self.final_layer

        self.shader_vhs = self.engine.load_shader_from_path('assets/shaders/vertex.glsl', 'assets/shaders/fragment_vhs.glsl')
        self.lights = luma.group()
        self.hulls = luma.group()
        
        self.level_manager =levels.LevelManager(self)