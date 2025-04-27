import pygame
import sys,pyshade
import pygame_light2d as pl2d
import pygame_light2d.double_buff
from pygame_light2d import LightingEngine, PointLight, Hull

# Initialize
pygame.init()

screen_res = (800, 600)
native_res = (800, 600)



screen = pygame.display.set_mode(screen_res,pygame.DOUBLEBUF|pygame.OPENGL)
clock = pygame.time.Clock()

with open("assets/shaders/vhs.frag","r") as f:
    VHS = f.read()

shader = pyshade.ShaderPostProcessor((800,600), fragment_shader_source=VHS)

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)

# Constants
GRAVITY = 0.5
JUMP_STRENGTH = -10
PLAYER_SPEED = 5



lights_engine = LightingEngine(
    screen_res=screen_res, native_res=native_res, lightmap_res=native_res)
lights_engine.set_ambient(30, 30, 30, 30)

light = PointLight(position=(0, 0), power=1., radius=250)
light.set_color(255, 100, 0, 200)
lights_engine.lights.append(light)

light2 = PointLight(position=(100, 300), power=1., radius=500)
light2.set_color(255, 255, 255, 200)
lights_engine.lights.append(light2)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=pos)
        self.vel_y = 0
        self.on_ground = False

    def update(self, keys):
        # Movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        if keys[pygame.K_SPACE]:
            if self.on_ground:
                self.vel_y = JUMP_STRENGTH

        # Gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Ground Collision
        self.on_ground = False
        for platform in platform_group:
            if self.rect.colliderect(platform.rect) and self.vel_y >= 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True
        light.position =self.rect.center
        
# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=pos)
        vertices = [self.rect.topleft, self.rect.topright, self.rect.bottomright, self.rect.bottomleft]
        self.hull = Hull(vertices)
        lights_engine.hulls.append(self.hull)

# Groups
player = Player((100, 400))
player_group = pygame.sprite.Group(player)

platform_group = pygame.sprite.Group()
# Ground
platform_group.add(Platform((0, 550), (800, 50)))
# Floating platforms
platform_group.add(Platform((200, 450), (100, 20)))
platform_group.add(Platform((400, 350), (150, 20)))
platform_group.add(Platform((600, 250), (120, 20)))

# Game loop
running = True
t = 0
while running:
    screen.fill(WHITE)

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player_group.update(keys)

    platform_group.draw(screen)
    player_group.draw(screen)

    surf = shader.render(screen,t)
    
    tex = lights_engine.surface_to_texture(surf)
    
    lights_engine.render_texture(
        tex, pl2d.BACKGROUND,
        pygame.Rect(0, 0, tex.width, tex.height),
        pygame.Rect(0, 0, tex.width, tex.height))
    tex.release()
    lights_engine.render()
    
    pygame.display.flip()
    t += clock.tick(60)

pygame.quit()
sys.exit()
