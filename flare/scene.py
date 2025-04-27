import pygame

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

WHITE = (255, 255, 255)
DARK_GRAY = (30, 30, 30)
LIGHT_GRAY = (200, 200, 200)
BLUE = (0, 100, 200)




# Scene Manager
class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current_scene = None

    def add_scene(self, name, scene):
        """Add a scene to the manager."""
        self.scenes[name] = scene

    def set_scene(self, name):
        """Switch to a different scene."""
        if name in self.scenes:
            self.current_scene = self.scenes[name]

    def handle_events(self, events):
        if self.current_scene:
            self.current_scene.handle_events(events)

    def update(self):
        if self.current_scene:
            self.current_scene.update()

    def render(self, screen):
        if self.current_scene:
            self.current_scene.render(screen)
            
class Scene:
    def __init__(self, manager):
        self.manager: SceneManager = manager  # Reference to SceneManager
    
    def handle_events(self, events):
        pass
    
    def update(self):
        pass
    
    def render(self, screen):
        pass            

# Button Class
class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = LIGHT_GRAY if self.rect.collidepoint(mouse_pos) else WHITE
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, DARK_GRAY, self.rect, 3, border_radius=10)

        text_surface = self.font.render(self.text, True, DARK_GRAY)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.action()