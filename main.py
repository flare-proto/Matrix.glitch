import pygame
import flare.scene
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


scene = pygame.Surface((800, 600))

class MenuScene(flare.scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.buttons = [
            flare.scene.Button(flare.scene.SCREEN_WIDTH // 2 - 100, 250, 200, 50, "Start Game", lambda: self.manager.set_scene("game")),
            flare.scene.Button(flare.scene.SCREEN_WIDTH // 2 - 100, 320, 200, 50, "Settings", lambda: self.manager.set_scene("settings")),
            flare.scene.Button(flare.scene.SCREEN_WIDTH // 2 - 100, 390, 200, 50, "Quit", lambda: pygame.quit() or exit()),
            flare.scene.Button(flare.scene.SCREEN_WIDTH // 2 - 100, 450, 200, 50, "DEBUG", lambda: self.manager.set_scene("debug")),
        ]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            for button in self.buttons:
                button.check_click(event)

    def render(self, screen):
        screen.fill(flare.scene.DARK_GRAY)
        font = pygame.font.Font(None, 48)
        title_text = font.render("Main Menu", True, flare.scene.WHITE)
        screen.blit(title_text, (flare.scene.SCREEN_WIDTH // 2 - 80, 150))

        for button in self.buttons:
            button.draw(screen)
            
class SettingsScene(flare.scene.Scene):
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.manager.set_scene("menu")

    def render(self, screen):
        screen.fill((100, 100, 100))
        font = pygame.font.Font(None, 36)
        text = font.render("Settings - Press ESC to return", True, flare.scene.WHITE)
        screen.blit(text, (flare.scene.SCREEN_WIDTH // 2 - 120, flare.scene.SCREEN_HEIGHT // 2))

class DEBUGScene(flare.scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.camera_x, self.camera_y = 0, 0
        self.water_animation_index = 0
        self.animation_timer = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.manager.set_scene("menu")

    def update(self):
        keys = pygame.key.get_pressed()

    def render(self, scr:pygame.Surface):
        scr.fill((0, 0, 0))
        x = 0
        y = 0
        for k,a in assets["tex"].items():
            r:pygame.Rect = a.get_rect()
            x += r.w
            if x >= 700:
                x = 0
                y += 16
            scr.blit(a,(x,y))


class GameScene(flare.scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.camera_x, self.camera_y = 0, 0
        self.water_animation_index = 0
        self.animation_timer = 0
        
        self.cardSel = None

    def handle_events(self, events):
        for event in events:
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    exit()
                case pygame.KEYDOWN :
                    match event.key:
                        case pygame.K_ESCAPE:
                            self.manager.set_scene("menu")
                

    def update(self):
        keys = pygame.key.get_pressed()

    def render(self, scr:pygame.Surface):
        scr.fill((15, 15, 15))
        
        scene.fill((20, 10, 40))
        pygame.draw.rect(scene, (255, 255, 255), (200, 200, 400, 200))
        pygame.draw.line(scene, (255, 0, 0), (0, 0), (800, 600), 5)
        scene.blit(logo,(250,250))

# Main loop
def main():
    t = 0.0
    manager = flare.scene.SceneManager()
    manager.add_scene("menu", MenuScene(manager))
    manager.add_scene("game", GameScene(manager))
    manager.add_scene("settings", SettingsScene(manager))
    manager.add_scene("debug", DEBUGScene(manager))
    manager.set_scene("menu")

    running = True
    while running:
        events = pygame.event.get()
        manager.handle_events(events)
        manager.update()
        manager.render(scene)

        pygame.display.flip()
        shader.render(scene, time=t)
        dt = clock.tick(60) / 1000
        t += dt  # advance time

if __name__ == "__main__":
    main()
