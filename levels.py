import pygame
from pygame_light2d import LightingEngine,PointLight,Hull

import luma

# Colors
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
GRAVITY = 0.5
JUMP_STRENGTH = 10


class Player(pygame.sprite.Sprite):
    def __init__(self, pos,lightEngine:LightingEngine,lights:luma.group):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(BLUE)
        self.rect = self.image.get_frect(topleft=pos)
        self.vel_y = 0
        self.vel_x = 0
        self.on_ground = False
        
        self.lightEngine = lightEngine
        self.lights = lights
        
        self.lamp = luma.light(lightEngine,(0,0),1,300)
        self.lamp.set_color(255,255,255,255)
        
        
        self.jumps_left = 1
        self.jumps = 1
        self.jumpCooldown = 0

    def jump(self):
        if self.on_ground:
            self.vel_y -= JUMP_STRENGTH
            self.jumps_left = self.jumps
        elif self.jumps_left > 0 and self.jumpCooldown <= 0:
            self.vel_y -= JUMP_STRENGTH * 1.25
            self.jumps_left -= 1
            self.jumpCooldown += 75
            t = luma.decayLight(self.lightEngine,self.rect.center,2,100,1000)
            t.set_color(150,200,255,255)
            t.join(self.lights)

    def cooldown(self, dt):
        if self.jumpCooldown > 0:
            self.jumpCooldown -= dt

    def update(self, keys, platform_group,):
        self.vel_x = 0
        if keys[pygame.K_LEFT]:
            self.vel_x = -5
        if keys[pygame.K_RIGHT]:
            self.vel_x = 5

        self.rect.x += self.vel_x
        for platform in platform_group:
            if self.rect.colliderect(platform.rect):
                if self.vel_x > 0:
                    self.rect.right = platform.rect.left
                if self.vel_x < 0:
                    self.rect.left = platform.rect.right

        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        self.on_ground = False
        for platform in platform_group:
            if self.rect.colliderect(platform.rect):
                if self.vel_y >= 0:
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                    self.vel_y = 0
                    self.jumps_left = self.jumps
        self.lamp.light.position = self.rect.center

class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, size,light_engine:LightingEngine,hulls:luma.group):
        super().__init__()
        self._hulls = hulls
        self.image = pygame.Surface(size)
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=pos)
        vertices = [self.rect.topleft, self.rect.topright, self.rect.bottomright, self.rect.bottomleft]
        self.hull = luma.hull(light_engine,vertices)
        self.hull.join(hulls)

class Level:
    def __init__(self, level_number, sublevel_number,light_engine:LightingEngine):
        self.light_engine = light_engine
        self.lights = luma.group()
        self.hulls = luma.group()
        
        
        self.level_number = level_number
        self.sublevel_number = sublevel_number
        self.platform_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.player = Player((100, 400),light_engine,self.lights)
        self.player_group.add(self.player)
        self.platform_group.add(Platform((0, 550), (800, 50),light_engine,self.hulls))  # Ground platform
        self.setup_level()

    def setup_level(self):
        """Set up platforms and objects specific to this level and sublevel."""
        if self.level_number == 1:
            if self.sublevel_number == 1:
                self.platform_group.add(Platform((100, 500), (100, 20),self.light_engine,self.hulls))
                self.platform_group.add(Platform((200, 450), (100, 20),self.light_engine,self.hulls))
            elif self.sublevel_number == 2:
                self.platform_group.add(Platform((300, 350), (150, 20),self.light_engine,self.hulls))
                self.platform_group.add(Platform((400, 200), (120, 20),self.light_engine,self.hulls))

        elif self.level_number == 2:
            if self.sublevel_number == 1:
                self.platform_group.add(Platform((100, 400), (100, 20),self.light_engine,self.hulls))
                self.platform_group.add(Platform((250, 300), (150, 20),self.light_engine,self.hulls))
            elif self.sublevel_number == 2:
                self.platform_group.add(Platform((400, 250), (120, 20),self.light_engine,self.hulls))
                self.platform_group.add(Platform((500, 150), (120, 20),self.light_engine,self.hulls))

    def on_frame(self, player,dt):
        """Define actions or events that happen every frame for this level."""
        if self.level_number == 2 and self.sublevel_number == 2:
            player.vel_y += GRAVITY * 0.5  # Change gravity for a specific level
        self.lights.update(dt)
    def draw(self,scr):
        self.platform_group.draw(scr)
        self.player_group.draw(scr)

class LevelManager:
    def __init__(self,light_engine:LightingEngine):
        self.current_level = 1
        self.current_sublevel = 1
        self.level = Level(self.current_level, self.current_sublevel,light_engine)

    def advance_level(self):
        """Advance to the next level or sublevel."""
        self.current_sublevel += 1
        if self.current_sublevel > 2:  # For example, 2 sublevels per level
            self.current_sublevel = 1
            self.current_level += 1

        self.level = Level(self.current_level, self.current_sublevel)
        print(f"Level {self.current_level}-{self.current_sublevel} started!")

    def on_frame(self,dt):
        """Call on_frame on the current level."""
        self.level.on_frame(self.level.player,dt)
    def draw(self,scr):
        self.level.draw(scr)