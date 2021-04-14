class State:
    def __init__(self,name=None) -> None:
        if name is not None:
            self.name = name 

    def refresh(self):
        pass 

    def on_enter(self):
        pass 

    def on_exit(self):
        pass 

    def handle_command(self,cmd):
        pass



class StateMachine:
    def __init__(self) -> None:
        self.state_dict = {}
        self.current_state = None
        pass

    def get_current_state(self):
        return self.current_state

    def refresh(self):
        self.current_state.refresh() 

    def handle_command(self,cmd):
        pass 
