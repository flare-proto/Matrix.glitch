import pygame
import sys
from pygame_light2d import LightingEngine, PointLight
import levels
import pygame_light2d as pl2d
from game import Game

# Initialize
pygame.init()

screen_res = (800, 600)
native_res = (800, 600)

screen = pygame.display.set_mode(screen_res, pygame.DOUBLEBUF | pygame.OPENGL)
clock = pygame.time.Clock()
game = Game(screen)


# Game loop
running = True
t = 0
dt = 0

while running:
    screen.fill((255, 255, 255))
    game.engine.clear(0, 0, 0)
    game.final_layer.clear(0, 0, 0)

    keys = pygame.key.get_pressed()
    game.level_manager.draw(screen)
    game.level_manager.level.player.update(keys, game.level_manager.level.platform_group)

    # Call the on_frame function for custom per-frame logic
    
    game.level_manager.on_frame(dt)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.level_manager.level.player.jump()

    
    tex = game.lights_engine.surface_to_texture(screen)
    game.lights_engine.render_texture(
        tex, pl2d.BACKGROUND,
        pygame.Rect(0, 0, tex.width, tex.height),
        pygame.Rect(0, 0, tex.width, tex.height))
    tex.release()
    game.lights_engine.render()
    game.shader_vhs['time'] = t
    game.engine.render(game.final_layer.texture, game.engine.screen, position=(0, 0),scale=1., shader=game.shader_vhs)
    
    pygame.display.flip()
    dt = clock.tick(60)
    t += dt
    game.level_manager.level.player.cooldown(dt)

pygame.quit()
sys.exit()
