# 场景 继承自gameObject
from pygame import Surface
import pygame
from base.task import TaskQue
import sys
sys.path.append("..")
import config

class Scene():
    def __init__(self,x=config.width,y=config.height) -> None:
        super().__init__()
        self.offset = pygame.Vector2(0,0)
        self.task_que = TaskQue()
        self.surface = Surface((x,y))
    
    def post_task(self,task):
        self.task_que.push(task)

    def event(self,events):
        pass 

    def physics(self):
        pass

    def update(self):
        self.task_que.update()

    def dispose(self):
        pass 


