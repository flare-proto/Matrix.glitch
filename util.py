class Point2:
    def __init__(self,x,y):
        self.x =x
        self.y =y
    @property
    def xy(self):
        return (self.x,self.y)
    
    @property
    def yx(self):
        return (self.y,self.x)
    
    @xy.setter
    def xyset(self,val):
        self.x = val[0]
        self.y = val[1]
        
    def __add__(self, b):
        assert isinstance(b,Point2)
        return Point2(self.x+b.x,self.y+b.y)