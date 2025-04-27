import pygame
from pygame.locals import *
from pyshade import ShaderPostProcessor

pygame.init()
screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)

# VHS Glitch Shader
with open("assets/shaders/vhs.frag","r") as f:
    vhs_shader_code = f.read()

shader = ShaderPostProcessor((800, 600), fragment_shader_source=vhs_shader_code)

logo =  pygame.image.load("assets/flare.png")

clock = pygame.time.Clock()
running = True
t = 0.0

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Draw scene
    scene = pygame.Surface((800, 600))
    scene.fill((20, 10, 40))
    pygame.draw.rect(scene, (255, 255, 255), (200, 200, 400, 200))
    pygame.draw.line(scene, (255, 0, 0), (0, 0), (800, 600), 5)
    scene.blit(logo,(250,250))

    # Render with shader
    shader.render(scene, time=t)

    pygame.display.flip()
    dt = clock.tick(60) / 1000
    t += dt  # advance time
