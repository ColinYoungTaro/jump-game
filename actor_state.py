from actor import Actor
from actor_input_handler import JumpCommand, MoveCommand, ThrustCommand
from base.state import State,StateMachine
from pygame import Vector2

# 可以左右移动的状态，继承了普通的状态类
class MovableState(State):
    def handle_command(self, cmd, actor):
        if isinstance(cmd, MoveCommand):
            x = cmd.x 
            y = cmd.y
            actor.pos += Vector2(x, y)
        

# 跳起来的状态，继承了可移动的状态
class JumpState(MovableState):
    def __init__(self, name=None) -> None:
        super().__init__(name)
        self.doubleJump = 1

    def on_enter(self, actor:Actor):
        self.startJump(actor)

    def startJump(self, actor):
        force = 4 
        actor.set_vy(force)

    def refresh(self,actor:Actor):
        if actor.is_grounded:
            return GroundedState()
            
    def handle_command(self, cmd, actor: Actor):
        super().handle_command(cmd, actor)
        if isinstance(cmd, JumpCommand):
            if self.doubleJump:
                self.doubleJump = 0
                self.startJump(actor)
        elif isinstance(cmd, ThrustCommand):
            return ThrustState()
            

class ThrustState(State):

    def __init__(self, name=None) -> None:
        super().__init__(name)

    def refresh(self, actor:Actor):
        actor.set_vx(5)
        actor.set_vy(0)

    def handle_command(self, cmd, actor: Actor):
        return super().handle_command(cmd)

# 在地面上的状态，继承了可移动的状态
class GroundedState(MovableState):
    # def handle_command(self, cmd, actor):
    #     super().handle_command(cmd, actor)

    def refresh(self,actor:Actor):
        if not actor.is_grounded:
            return JumpState()

    def handle_command(self, cmd, actor):
        # 保证在接收jumpCommand的过程中也可以移动，需要调用父类的handle函数
        super().handle_command(cmd, actor)
        if isinstance(cmd,JumpCommand):
            cmd.execute(actor)
            return JumpState()

# 状态机
class ActorStateMachine(StateMachine):
    def __init__(self,ctrl_actor) -> None:
        super().__init__()
        self.actor = ctrl_actor
        self.current_state = JumpState()

    def handle_command(self,cmd):
        if self.current_state:
            next_state = self.current_state.handle_command(cmd,self.actor)
            if next_state:
                self.change_state(next_state)
        else:
            print("error:current state is NULL")

    def refresh(self):
        next_state : State = self.current_state.refresh(self.actor)
        if next_state:
            self.change_state(next_state)

    def change_state(self, state : State):
        if state:
            self.current_state.on_exit(self.actor)
            self.current_state = state
            self.current_state.on_enter(self.actor)

