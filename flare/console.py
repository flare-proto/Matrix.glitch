import pygame,logging,coloredlogs,collections,re

CHAR_WIDTH = 10
CHAR_HEIGHT = 15

ANSI_COLORS = {
    '30': (0, 0, 0),        # Black
    '31': (255, 0, 0),      # Red
    '32': (0, 255, 0),      # Green
    '33': (255, 255, 0),    # Yellow
    '34': (0, 0, 255),      # Blue
    '35': (255, 0, 255),    # Magenta
    '36': (0, 255, 255),    # Cyan
    '37': (255, 255, 255),  # White,
    "81": (255,175,0),
    '0': (255, 255, 255)    # Reset (default white)
}

class logHandle(logging.Handler):
    def __init__(self, level = 0):
        super().__init__(level)
        self.log = collections.deque([],100)
    def emit(self, record):
        self.log.append(record.getMessage())
        
class console:
    def __init__(self):
        self.log = collections.deque([],100)
        self.font = pygame.font.Font(None, 20)
    def draw(self,scr):
        for Y,l in enumerate(self.log):
            y = Y*20
            matches = re.findall(r'(\033\[(\d+)m)?([^(\033)]*)', l)

            current_color = (255, 255, 255)  # Default white
            offset_x = 10

            for ansi_code, color_code, content in matches:
                if color_code in ANSI_COLORS:
                    current_color = ANSI_COLORS[color_code]

                if content:
                    text_surface = self.font.render(content, True, current_color)
                    scr.blit(text_surface, (offset_x, y))
                    offset_x += text_surface.get_width()
    def write(self,w):
        self.log.append(w)
    def update(self,w):
        self.log.pop()
        self.log.append(w)