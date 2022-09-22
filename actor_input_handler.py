
from actor import Actor
from singleton import Singleton
from pygame import Vector2
from pygame import key
from pygame.constants import K_LEFT, K_RIGHT, K_c, K_z
from pygame.key import get_pressed
from base.command import InputHandler,Command


"""sumary_line
    定义命令对象
    通过将命令传递给角色所属的状态机来完成角色的状态转移
"""

# jumpCommand：跳跃的命令
class JumpCommand(Command):
    def __init__(self,force = 10):
        self.force = min(force,5)
        super().__init__()

    def execute(self,actor:Actor):
        pass 
        # actor.set_vy(self.force)

class ThrustCommand(Command):
    def __init__(self):
        self.force = 4
    
    def execute(self,actor:Actor):
        # actor.set_vx(self.force)
        pass 

# 移动命令，构造函数包括移动的Δx和Δy
class MoveCommand(Command):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        super().__init__()

    def execute(self, ctrl_obj):
        actor : Actor = ctrl_obj
        actor.pos += Vector2(self.x,self.y)

class ActorInputHandler(InputHandler):
    
    def __init__(self) -> None:
        super().__init__()

    def handle_input(self, key):
        if key == K_c:
            return JumpCommand()
        elif key == K_z:
            return ThrustCommand()
        return None

    def update(self):
        key_list = get_pressed()

        if key_list[K_RIGHT] :
           return MoveCommand(5,0)
           
        elif key_list[K_LEFT]:
            return MoveCommand(-5,0)


