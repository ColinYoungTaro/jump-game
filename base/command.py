# 命令程序接口
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
        if key.key == K_SPACE:
            print("space down") 
            return Command()