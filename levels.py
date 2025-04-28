import pygame,os
from lupa import LuaRuntime
from pygame_light2d import Hull, LightingEngine, PointLight

import luma
from game import Game
from util import Point2

sandbox = LuaRuntime(unpack_returned_tuples=True, register_eval=False)

# Remove access to global functions that could be dangerous
# Inject restricted environment into Lua
sandbox.globals()["_G"] = None  # Remove global environment access
sandbox.globals()["os"] = None  # Prevent OS access
sandbox.globals()["io"] = None  # Prevent file operations
sandbox.globals()["debug"] = None  # Block debugging functions

# Colors
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
GRAVITY = 0.5
JUMP_STRENGTH = 10
PLAYER_SPEED=5

class Player(pygame.sprite.Sprite):
    def __init__(self, pos,game:Game):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(BLUE)
        self.rect = self.image.get_frect(topleft=pos)
        self.vel_y = 0
        self.vel_x = 0
        self.on_ground = False
        
        self.game = game
        
        self.lamp = luma.light(game.lights_engine,(0,0),1,300)
        self.lamp.set_color(255,255,255,255)
        
        
        self.jumps_left = 1
        self.jumps = 1
        self.jumpCooldown = 0

    def jump(self):
        if self.on_ground:
            self.vel_y -= JUMP_STRENGTH
            self.jumps_left = self.jumps
            t = luma.decayLight(self.game.lights_engine,self.rect.center,1,100,1500)
            t.set_color(200,50,255,255)
            t.join(self.game.lights)
        elif self.jumps_left > 0 and self.jumpCooldown <= 0:
            self.vel_y -= JUMP_STRENGTH * 1.2
            self.jumps_left -= 1
            self.jumpCooldown += 100
            t = luma.decayLight(self.game.lights_engine,self.rect.center,2,100,1000)
            t.set_color(100,200,255,255)
            t.join(self.game.lights)

    def cooldown(self, dt):
        if self.jumpCooldown > 0:
            self.jumpCooldown -= dt

    def update(self, keys, platform_group,):
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
        self.lamp.light.position = self.rect.center

class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, size,game:Game):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=pos)
        vertices = [self.rect.topleft, self.rect.topright, self.rect.bottomright, self.rect.bottomleft]
        self.hull = luma.hull(game.lights_engine,vertices)
        self.hull.join(game.hulls)

class WarpGate(luma.member):
    def __init__(self,pos:Point2,game: Game):
        super().__init__()
        self.pos =  pos
        self.game = game
        self.lights = luma.group()
        self.rect = pygame.Rect(0,0,50,130)
        self.rect.center = self.pos.xy
        
        self._makeLight(Point2(0,-40),pygame.Color(230, 107, 147))
        self._makeLight(Point2(0,-20),pygame.Color(255,255,255))
        self._makeLight(Point2(0,0),pygame.Color(205, 83, 221))
        self._makeLight(Point2(0,20),pygame.Color(166, 166, 166))
        self._makeLight(Point2(0,40),pygame.Color(112, 122, 219))
        
    def _makeLight(self,offset:Point2,col:pygame.Color):
        l = luma.light(self.game.lights_engine,(
            (self.pos+offset).xy
        ),1.5,50)
        l.set_color(col.r,col.g,col.b,col.a)
        l.join(self.lights)
    def update(self, dt):
        if self.game.level_manager.level.player.rect.colliderect(self.rect):
            self.game.level_manager.advance_level()
    def kill(self):
        super().kill()
        self.lights.kill()
class Level:
    def __init__(self, level_number, sublevel_number,game:Game):
        self.game = game
        
        
        
        self.level_number = level_number
        self.sublevel_number = sublevel_number
        self.platform_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.player = Player((100, 400),self.game)
        
        self.setup_level()
        

    def setup_level(self):
        """Set up platforms and objects specific to this level and sublevel."""
        
        self.player_group.add(self.player)
        self.platform_group.add(Platform((0, 850), (1500, 50),self.game))  # Ground platform
        
        pth = os.path.join("levels",f"l{self.level_number}_{self.sublevel_number}.lua")
        if os.path.exists(pth):
            with open(pth,"r") as f:
                lt = LevelToolkit(self)
                sandbox.execute(f.read())(lt)
        else:
            self.wg = WarpGate(Point2(500,100),self.game)
            if self.level_number == 1:
                if self.sublevel_number == 1:
                    self.platform_group.add(Platform((100, 500), (100, 20),self.game))
                    self.platform_group.add(Platform((200, 450), (100, 20),self.game))
                elif self.sublevel_number == 2:
                    self.platform_group.add(Platform((300, 350), (150, 20),self.game))
                    self.platform_group.add(Platform((400, 200), (120, 20),self.game))

            elif self.level_number == 2:
                if self.sublevel_number == 1:
                    self.platform_group.add(Platform((100, 400), (100, 20),self.game))
                    self.platform_group.add(Platform((250, 300), (150, 20),self.game))
                elif self.sublevel_number == 2:
                    self.platform_group.add(Platform((400, 250), (120, 20),self.game))
                    self.platform_group.add(Platform((500, 400), (120, 20),self.game))

    def on_frame(self, player,dt):
        """Define actions or events that happen every frame for this level."""
        if self.level_number == 2 and self.sublevel_number == 2:
            player.vel_y += GRAVITY * 0.5  # Change gravity for a specific level
        if self.player.rect.y >= 900:
            self.reset()
        self.game.lights.update(dt)
        self.wg.update(dt)
    def draw(self,scr):
        self.platform_group.draw(scr)
        self.player_group.draw(scr)
    def end(self):
        self.game.hulls.kill()
        self.player.lamp.kill()
        self.wg.kill()
    def reset(self):
        self.game.hulls.kill()
        self.wg.kill()
        self.platform_group.empty()
        self.setup_level()
        self.player.vel_x = 0
        self.player.vel_y = 0
        
class LevelManager:
    def __init__(self,game:Game):
        self.current_level = 1
        self.current_sublevel = 1
        self.game = game
        self.level = Level(self.current_level, self.current_sublevel,game)

    def advance_level(self):
        """Advance to the next level or sublevel."""
        self.level.end()
        self.current_sublevel += 1
        if self.current_sublevel > 2:  # For example, 2 sublevels per level
            self.current_sublevel = 1
            self.current_level += 1
        
        self.level = Level(self.current_level, self.current_sublevel,self.game)
        print(f"Level {self.current_level}-{self.current_sublevel} started!")

    def on_frame(self,dt):
        """Call on_frame on the current level."""
        self.level.on_frame(self.level.player,dt)
    def draw(self,scr):
        self.level.draw(scr)
        
class LevelToolkit:
    def __init__(self,level: Level):
        self.level = level
    def Point2(self,x,y):
        return Point2(x,y)
    def Platform(self, pos, size):
        self.level.platform_group.add(Platform(pos.xy,size.xy,self.level.game))
    def exit(self,pos):
        self.level.wg = WarpGate(pos,self.level.game)
    def player(self,pos):
        self.level.player.rect.center = pos.xy