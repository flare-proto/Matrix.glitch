import pygame,collections
class TextPrint:
    def __init__(self,font=None,fontSize=25,line_height=15):
        self.base_line_height = line_height
        self.reset()
        self.font = pygame.font.Font(font, fontSize)

    def tprint(self, screen, text):
        text_bitmap = self.font.render(text, True, (255, 255, 255))
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = self.base_line_height

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10
        
class LogDisplay:
    def __init__(self):
        self.tp = TextPrint(fontSize=20,line_height=15)
        self.log = collections.deque([],50)
    def draw(self,scr):
        self.tp.reset()
        for i in self.log:
            self.tp.tprint(scr,i)
    def write(self,w):
        self.log.append(w)
        
