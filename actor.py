from base.animation import Animation
from pygame import Rect, Vector2
from pygame.draw import circle, rect
import pygame
from pygame.sprite import Sprite
from base.game_object import gameObject
import config
from base.state import State,StateMachine

COLOR_RED = (255,0,0)

class Actor(gameObject):
    # 初始化相关状态
    def __init__(self) -> None:
        super().__init__()
        # 判定是否落地的标志
        self.is_grounded = False
        # 判定任务的速度
        self.velocity = Vector2(0,0)
        # # sprite相关
        self.image = pygame.Surface([30,30])
        self.image.set_colorkey((0,0,0))
        # 主体图像 
        # TODO:可以用图像替代
        circle(self.image,COLOR_RED,(15,15),15)
        self.rect = self.image.get_rect()
        


    def show(self):
        self.rect.x = self.pos.x
        self.rect.y = config.height-self.pos.y-self.rect.height

    def physics(self,gravity):
        self.pos += self.velocity

        if(not self.is_grounded):
            self.velocity += gravity

    # 获取屏幕上Actor的精灵对象
    def get_sprite(self):
        return self.sprite

    def set_velocity(self,vx,vy):
        self.velocity = Vector2(vx,vy)

    def set_vx(self,vx):
        self.velocity.x = vx
    
    def set_vy(self,vy):
        self.velocity.y = vy

    # 落地时候的回调函数
    def on_ground(self):
        # print("grounded")
        self.is_grounded = True
        self.velocity = Vector2(0,0)
        