from pygame_light2d import LightingEngine, PointLight,Hull
import pygame.math



class group:
    def __init__(self):
        self._members =set()
    def kill(self):
        for i in self._members:
            i._rem(self)
            self._members.remove(i)
            i._kill()
    def clear(self):
        for i in self._members:
            i._rem(self)
            self._members.remove(i)
    def _rem(self,memb):
        self._members.remove(memb)
    def _join(self,memb):
        self._members.add(memb)
    def update(self,dt):
        for i in list(self._members):
            i.update(dt)

class light:
    def __init__(self,engine:LightingEngine,position: tuple[int],power: float=1., radius: float=1):
        self._eng = engine
        self._groups:set[group] =set()
        self.light = PointLight(position=position, power=power, radius=radius)
        self._eng.lights.append(self.light)
    def set_color(self,r:int=0,g:int=0,b:int=0,a:int=0):
        self.light.set_color(r, g, b, a)
        return self
    def kill(self):
        for g in list(self._groups):
            g._rem(self)
            self._groups.remove(g)
        #self._eng.lights.remove(self)
    def _rem(self,g:group):
        self._groups.remove(g)
    def join(self,g:group):
        g._join(self)
        self._groups.add(g)
        return self
    def update(self,dt):
        pass

class decayLight(light):
    def __init__(self, engine, position, power = 1, radius = 1,time_to_gone: float=3):
        super().__init__(engine, position, power, radius)
        self.maxTime = time_to_gone
        self.max = power
        self.time_remain = time_to_gone
    def update(self, dt):
        self.time_remain -= dt
        self.light.power = pygame.math.remap(0,self.maxTime,0,self.max,self.time_remain)
        if self.time_remain <= 0:
            self.kill()
            
class hull:
    def __init__(self,engine:LightingEngine,verts):
        self._eng = engine
        self._groups:set[group] =set()
        self.hull = Hull(verts)
        self._eng.hulls.append(self.hull)

    def kill(self):
        for g in list(self._groups):
            g._rem(self)
            self._groups.remove(g)
        self._eng.hulls.remove(self)
    def _kill(self):
        self._eng.hulls.remove(self)
    def _rem(self,g:group):
        self._groups.remove(g)
    def join(self,g:group):
        g._join(self)
        self._groups.add(g)
        return self
    def update(self,dt):
        pass