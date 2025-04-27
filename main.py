import pygame
import sys
from pygame_light2d import LightingEngine, PointLight
import levels
import pygame_light2d as pl2d

# Initialize
pygame.init()

screen_res = (800, 600)
native_res = (800, 600)

screen = pygame.display.set_mode(screen_res, pygame.DOUBLEBUF | pygame.OPENGL)
clock = pygame.time.Clock()

# Lighting Engine
lights_engine = LightingEngine(
    screen_res=screen_res, native_res=native_res, lightmap_res=native_res
)
lights_engine.set_ambient(20, 20, 20, 20)

engine = lights_engine.graphics
final_layer = engine.make_layer(screen_res)

lights_engine.light_output_target =final_layer

shader_vhs = engine.load_shader_from_path('assets/shaders/vertex.glsl', 'assets/shaders/fragment_vhs.glsl')


# Game loop
running = True
t = 0
dt = 0
level_manager = levels.LevelManager(lights_engine)

while running:
    screen.fill((255, 255, 255))
    engine.clear(0, 0, 0)
    final_layer.clear(0, 0, 0)

    keys = pygame.key.get_pressed()
    level_manager.level.player.update(keys, level_manager.level.platform_group)

    # Call the on_frame function for custom per-frame logic
    
    level_manager.on_frame(dt)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                level_manager.level.player.jump()

    level_manager.draw(screen)
    tex = lights_engine.surface_to_texture(screen)
    lights_engine.render_texture(
        tex, pl2d.BACKGROUND,
        pygame.Rect(0, 0, tex.width, tex.height),
        pygame.Rect(0, 0, tex.width, tex.height))
    tex.release()
    lights_engine.render()
    shader_vhs['time'] = t
    engine.render(final_layer.texture, engine.screen, position=(0, 0),scale=1., shader=shader_vhs)
    
    pygame.display.flip()
    dt = clock.tick(60)
    t += dt
    level_manager.level.player.cooldown(dt)

pygame.quit()
sys.exit()
