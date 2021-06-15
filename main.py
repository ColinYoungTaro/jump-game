from key import init_keys
from singleton import Singleton
from scene_title import SceneTitle
from base.mscene import Scene
from base.task import GameTaskQue, Task
import pygame
from pygame import Surface
from pygame.time import Clock
from pygame.locals import *
from scene_game import SceneGame

import config  
class Game:
    # 初始化
    def __init__(self):
        # 初始化模块
        pygame.init()
        pygame.font.init()
        # 配置基本信息
        self.width = config.width
        self.height = config.height
        self.size = self.width,self.height
        self.fps = 60
        self.clock = Clock()
        # 程序的屏幕Surface对象
        # self.screen = pygame.display.set_mode(self.size,pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode(self.size)
        # 当前的场景
        self.scene = SceneTitle()
        # 任务队列，用来处理游戏所需自定义的一些任务
        self.task_que = GameTaskQue(self)

        Singleton.get_instance().bind_global_task_que(task_que=self.task_que)
        # self.task_que.push(SceneTransitionTask())
        # 创建精灵组
        self.group = pygame.sprite.Group()

        self.transition_layer = Surface((config.width,config.height))
        self.transition_layer.fill((0,0,0))
        self.transition_layer.set_alpha(0)

    

    # 更新模块，完成游戏每一帧的更新
    
    def get_transition_layer(self):
        return self.transition_layer

    def update(self):
        # 更新任务和场景
        if self.scene.is_enable():
            self.scene.update()
        self.task_que.update()

    def change_scene(self,next):
        self.scene.dispose()
        self.scene = next

    # 绘图模块
    def draw(self):
        # 清屏
        self.screen.fill((60,120,170))
        surface = self.scene.show(self.screen)
        if surface:
            self.screen.blit(surface,Rect(-self.scene.offset.x,self.scene.offset.y,config.width,config.height))
        self.screen.blit(self.transition_layer,(0,0))
        # 更新屏幕
        # 控制fps
        self.clock.tick(self.fps)
        pygame.display.update()
    
    # 物理模块
    def physics(self):
        if self.scene.is_enable():
            self.scene.physics()
        pass 

    # 默认的事件处理模块
    def event(self):
        events = pygame.event.get()
        # 将所有事件传递给场景对象进行处理
        if self.scene.is_enable():
            self.scene.event(events)
        # 在框架最外层处理整个框架应该处理的任务
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit()
            elif event.type == pygame.QUIT:
                self.exit()

    def tasks(self):
        pass 

    def exit(self):
        self.scene.dispose()
        exit()

    def run(self):
        while True:
            # 游戏循环
            # 依次调用 物理，逻辑，画面，时间和任务的更新
            self.physics()
            self.update()
            self.draw()
            self.event()
            self.tasks()
           
def main():
    game = Game()
    init_keys()
    game.run()


if __name__ == '__main__':
    main()

