from actor_state import ActorStateMachine
from actor_input_handler import ActorInputHandler
from pygame.constants import KEYDOWN
from base.command import Command
from pygame.event import post
from actor import Actor
from pygame import Rect, Surface, Vector2, draw, sprite, surface
from base.game_object import gameObject
import pygame
from base.mscene import Scene
import config

COLOR_BLACK = (0,0,0)
COLOR_WHITE = (255,255,255)

# 正方形区域，x,y相对于
# TODO {map左下角笛卡尔坐标系}
# 的位置
# w，h为区域的宽高
class Block(gameObject):
    # 创建正方形区域
    def __init__(self,w,h,x,y) -> None:
        super().__init__()
        self.w = w
        self.h = h
        self.floor_h = 10
        self.pos = Vector2(x,y)
        # 创建一个黑色矩形
        self.image = Surface([w,h])
        self.rect = Rect(x,config.height-y-h,w,h)
        self.image.fill(COLOR_BLACK)

    def __repr__(self) -> str:
        return "w:{0},h:{1},x:{2},y:{3}".format(self.w,self.h,self.pos.x,self.pos.y)

    # 更改显示位置，根据Scene传入的offset
    def show(self,offset):
        self.rect.x = -offset.x+self.pos.x
        self.rect.y = config.height-self.pos.y-self.h

    # 获取平台的地面坐标
    def get_level(self) -> int:
        return self.pos.y + self.h

    def adjust_grounded_object(self,obj:sprite.Sprite):
        # 调整actor的位置到地板上
        if obj.pos.y >= self.get_level() - obj.rect.h:
            obj.pos.y = self.get_level() - 1
            if hasattr(obj,'on_ground') and not obj.is_grounded:
                obj.on_ground()

class GameMap(gameObject):
    def __init__(self) -> None:
        # 载入地图信息
        # TODO:将地图信息写入配置文件
        super().__init__()
        self.ground = []
        self.w = 1000
        self.h = 600

        # 加入地板
        self.ground.append(Block(200,50,0,0))
        self.ground.append(Block(220,40,230,0))

        # sprite的image，rect属性补全，用于绘图和坐标确定
        self.image = Surface([self.w,self.h])
        self.image.fill(COLOR_WHITE)
        self.rect = self.image.get_rect()

    # 返回地面物体的列表用于碰撞检测
    def get_all_floor(self):
        return self.ground

# 游戏场景
class SceneGame(Scene):
    def __init__(self) -> None:
        super().__init__()
        self.gravity = pygame.Vector2(0,-config.gravity)
        self.map = GameMap()
        # 地图的坐标偏移量
        self.offset = pygame.Vector2(0,0)
        self.actor = Actor()
        self.actor.set_pos(0,300)
        self.sprite_group = sprite.Group()
        self.input_handler = ActorInputHandler()
        self.actor_state_machine = ActorStateMachine(self.actor)

        self.sprite_group.add(self.actor)
        for block in self.map.get_all_floor():
            self.sprite_group.add(block)

    def bind(self,vector):
        if vector.x > int(config.width / 2):
            self.offset.x = vector.x - int(config.width / 2)

    def update(self):
        # self.offset.x += 1.2
        self.bind(self.actor.pos)
        self.sprite_group.update()
        for floor in self.map.get_all_floor():
            floor.show(self.offset)
        self.actor.show(self.offset)
        self.actor_state_machine.refresh()


    def show(self,screen):
        self.sprite_group.draw(screen)

    def physics(self):
        # 判断落地
        all_floor = self.map.get_all_floor()
        floor:Block = sprite.spritecollideany(self.actor,all_floor)
        # 当检测到碰撞对象后，将actor防止在地板上
        if floor is not None:
            floor.adjust_grounded_object(self.actor)
        else:
            self.actor.is_grounded = False
                    
        self.actor.physics(Vector2(0,-config.gravity))

    def event(self, events):
        # 需要持续监测的cmd
        cmd = self.input_handler.update()
        if cmd:
            self.actor_state_machine.handle_command(cmd)

        # 需要监测触发信号的cmd
        for event in events:
            if event.type == KEYDOWN:
                cmd = self.input_handler.handle_input(event.key)
                if cmd is not None:
                    self.actor_state_machine.handle_command(cmd)
    