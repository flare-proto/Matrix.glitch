import pygame
import luma
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




# Colors
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)

# Constants
GRAVITY = 0.5
JUMP_STRENGTH = 10
PLAYER_SPEED = 5



lights_engine = LightingEngine(
    screen_res=screen_res, native_res=native_res, lightmap_res=native_res)
lights_engine.set_ambient(20, 20, 20, 20)

engine = lights_engine.graphics

final_layer = engine.make_layer(screen_res)

lights_engine.light_output_target =final_layer

shader_vhs = engine.load_shader_from_path('assets/shaders/vertex.glsl', 'assets/shaders/fragment_vhs.glsl')

lights = luma.group()

l0 = luma.light(lights_engine,position=(500, 80), power=1., radius=50)
l0.join(lights)
l0.set_color(254, 118, 162, 255)

l1 = luma.light(lights_engine,position=(500, 100), power=1., radius=50)
l1.join(lights)
l1.set_color(255, 255, 255, 200)

l2 = luma.light(lights_engine,position=(500, 120), power=1., radius=50)
l2.join(lights)
l2.set_color(186, 76, 201, 255)

l3 = luma.light(lights_engine,position=(500, 140), power=1., radius=50)
l3.join(lights)
l3.set_color(166,166, 166, 255)

l4 = luma.light(lights_engine,position=(500, 160), power=1., radius=50)
l4.join(lights)
l4.set_color(112, 122, 219, 255)

light = PointLight(position=(0, 0), power=1., radius=250)
light.set_color(255, 255, 255, 200)
lights_engine.lights.append(light)





# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(BLUE)
        self.rect = self.image.get_frect(topleft=pos)
        self.vel_y = 0
        self.vel_x = 0
        self.on_ground = False
        self.jumps_left = 1  # Can jump once initially
        self.jumps = 1
        self.jumpCooldown = 0

    def jump(self):
        """Handles the jumping and double jumping logic."""
        if self.on_ground:
            self.vel_y -= JUMP_STRENGTH
            self.jumps_left = self.jumps  # Reset to 1 jump when grounded
            
            self.jumpCooldown += 75
        elif self.jumps_left > 0 and self.jumpCooldown <= 0:  # Double jump logic
            self.vel_y -= JUMP_STRENGTH*1.25
            self.jumps_left -= 1  # Use one jump
            l = luma.decayLight(lights_engine,self.rect.center,2,100,1000)
            l.set_color(150, 150, 255, 200)
            l.join(lights)
            self.jumpCooldown += 75
            
    def cooldown(self,dt):
        if self.jumpCooldown>0:
            self.jumpCooldown -= dt

    def update(self, keys):
        # Horizontal Movement
        self.vel_x = 0
        if keys[pygame.K_LEFT]:
            self.vel_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.vel_x = PLAYER_SPEED

        # Apply horizontal movement
        self.rect.x += self.vel_x

        # Horizontal collision with platforms
        for platform in platform_group:
            if self.rect.colliderect(platform.rect):
                # Prevent moving through the platform on the left or right
                if self.vel_x > 0:  # Moving right
                    self.rect.right = platform.rect.left
                if self.vel_x < 0:  # Moving left
                    self.rect.left = platform.rect.right

        # Gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Vertical collision with platforms (falling down)
        self.on_ground = False  # Reset on_ground flag
        for platform in platform_group:
            if self.rect.colliderect(platform.rect):
                # Collision from above (falling)
                if self.vel_y >= 0:  # Moving down
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                    self.vel_y = 0
                    self.jumps_left = self.jumps  # Reset jumps on ground
                    
                # Collision from below (jumping up)
                elif self.vel_y < 0:  # Moving up
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

        # Jumping (called separately)
        #if keys[pygame.K_SPACE]:
        #    self.jump()  # Call jump function

        # Update light position to match player's position
        light.position = self.rect.center
        
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
platform_group.add(Platform((100, 500), (100, 20)))
platform_group.add(Platform((200, 450), (100, 20)))
platform_group.add(Platform((400, 350), (150, 20)))
platform_group.add(Platform((600, 250), (120, 20)))

platform_group.add(Platform((400, 180), (120, 20)))

# Game loop
running = True
t = 0
dt = 0
while running:
    screen.fill(WHITE)
    engine.clear(0, 0, 0)
    final_layer.clear(0, 0, 0)

    keys = pygame.key.get_pressed()
    player_group.update(keys)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
                pass

    

    platform_group.draw(screen)
    player_group.draw(screen)
    
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
    lights.update(dt)
    player.cooldown(dt)

pygame.quit()
sys.exit()
