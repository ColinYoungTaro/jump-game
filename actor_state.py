from actor import Actor
from actor_input_handler import JumpCommand, MoveCommand
from base.state import State,StateMachine

# 可以左右移动的状态，继承了普通的状态类
class MovableState(State):
    def handle_command(self, cmd, actor):
        if isinstance(cmd,MoveCommand):
            cmd.execute(actor)
        

# 跳起来的状态，继承了可移动的状态
class JumpState(MovableState):
    def refresh(self,actor:Actor):
        if actor.is_grounded:
            return GroundedState()


# 在地面上的状态，继承了可移动的状态
class GroundedState(MovableState):
    def handle_command(self, cmd, actor):
        super().handle_command(cmd, actor)

    def refresh(self,actor):
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
            self.current_state.handle_command(cmd,self.actor)
        else:
            print("error:current state is NULL")

    def refresh(self):
        # (self.current_state)
        next_state : State = self.current_state.refresh(self.actor)
        if next_state:
            self.current_state.on_exit()
            self.current_state = next_state
            self.current_state.on_enter()

