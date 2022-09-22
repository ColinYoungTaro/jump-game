# 命令程序接口
from typing import Callable
from pygame.constants import KEYDOWN, K_SPACE


class Command:
    def __init__(self):
        pass

    def execute(self,ctrl_obj):
        pass 

class InputHandler:
    def __init__(self) -> None:
        pass 
    
    def handle_input(self,key):
        pass

    def dispose(self):
        pass 

class EventHandler(Callable):
    def __call__(self, gameobj, event):
        pass 

class UpdateHandler(Callable):
    def __call__(self, gameobj):
        pass 