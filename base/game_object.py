from pygame import Vector2
from pygame import sprite
from pygame.sprite import Sprite

class gameObject(Sprite):
    def __init__(self) -> None:
        super().__init__()
        # pos坐标是相对左下角的坐标
        self.pos = Vector2(0,0)
        pass
    
    def set_pos(self,x,y):
        self.pos.x = x
        self.pos.y = y

    def get_pos(self):
        return self.pos

    def physics(self):
        pass 

    def event(self):
        pass 

    def dispose(self):
        pass 