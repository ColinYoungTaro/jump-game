from actor import COLOR_DOUBLE_JMP, COLOR_FIRE, COLOR_IDLE, COLOR_RED, COLOR_THRUST, Actor
from actor_input_handler import JumpCommand, MoveCommand, PunchCommand, ThrustCommand
from base.state import State,StateMachine
from pygame import Vector2

# 可以左右移动的状态，继承了普通的状态类
class MovableState(State):
    def __init__(self, name=None) -> None:
        self.dir = 1

    def refresh(self, actor:Actor):
        pass 
        
    def handle_command(self, cmd, actor : Actor):
        if isinstance(cmd, MoveCommand):
            actor.set_vx(cmd.x)
            if cmd.x != 0 :
                self.dir = 1 if cmd.x > 0 else -1
        

# 跳起来的状态，继承了可移动的状态
class JumpState(MovableState):
    def __init__(self, name=None) -> None:
        super().__init__(name)
        self.force = 13

    def on_enter(self, actor:Actor):
        if actor.allow_jmp_time != 0:
            actor.set_color(COLOR_IDLE)
        else:
            actor.set_color(COLOR_DOUBLE_JMP)

        if actor.is_grounded:
            self.startJump(actor, self.force)
        else:
            pass 

    def startJump(self, actor, force):
        actor.set_vy(force)

    def refresh(self,actor:Actor):
        if actor.is_grounded:
            return GroundedState()
        
    def handle_command(self, cmd, actor: Actor):
        
        if isinstance(cmd, JumpCommand):
            if actor.allow_jmp_time > 0:
                actor.allow_jmp_time = 0
                self.startJump(actor, self.force * 0.6)
                actor.set_color(COLOR_DOUBLE_JMP)

        elif isinstance(cmd, ThrustCommand):
            if actor.allow_thrust_time > 0 :
                actor.allow_thrust_time = 0
                return ThrustState(self.dir)
        
        elif isinstance(cmd, PunchCommand):
            return PunchPrepareState()
        
        return super().handle_command(cmd, actor)
            

class ThrustState(State):

    def __init__(self, dir, name=None) -> None:
        super().__init__(name)
        self.dir = 1 if dir > 0 else -1
        self.vx = 20
        self.fr = 0.9

    def on_enter(self, actor:Actor):
        actor.set_velocity(self.vx * self.dir , 0)
        actor.set_color(COLOR_THRUST)

    def refresh(self, actor:Actor):
        vx = self.vx
        if vx > 10:
            vx -= self.fr
            vx = max(vx, 0)
            actor.set_velocity(vx * self.dir, 0)
        else:
            return JumpState()
        self.vx = vx 

    def handle_command(self, cmd, actor: Actor):
        pass 

class PunchState(State):
    def __init__(self, name=None) -> None:
        super().__init__(name)

    def on_enter(self, obj:Actor=None):
        obj.set_velocity(0, -25)


    def refresh(self, obj:Actor):
        if obj.is_grounded:
            return PunchEndState()

class PunchPrepareState(State):
    def __init__(self, name=None) -> None:
        self.frame_cnt = 15

    def refresh(self, obj:Actor):
        obj.set_velocity(0, 2)
        obj.set_color(COLOR_RED)
        if self.frame_cnt > 0:
            self.frame_cnt -= 1
        else:
            return PunchState()

class PunchEndState(State):
    def __init__(self, name=None) -> None:
        self.frame_cnt = 20

    def refresh(self, obj:Actor):
        obj.set_velocity(0, 0)
        if self.frame_cnt > 0:
            self.frame_cnt -= 1
        else:
            return GroundedState()

# 在地面上的状态，继承了可移动的状态
class GroundedState(MovableState):
    def on_enter(self, obj=None):
        assert(isinstance(obj, Actor))
        obj.set_color(COLOR_IDLE)

    def refresh(self,actor:Actor):
        if not actor.is_grounded:
            return JumpState()
        super().refresh(actor)

    def handle_command(self, cmd, actor):
        super().handle_command(cmd, actor)
        if isinstance(cmd,JumpCommand):
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

