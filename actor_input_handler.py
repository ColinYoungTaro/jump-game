
from pygame import Vector2
from pygame import key
from pygame.constants import K_LEFT, K_RIGHT, K_SPACE
from pygame.key import get_pressed
from base.command import InputHandler,Command
from volume import messure
import random
#import pyaudio
import numpy as np
from config import volumn_threshold,volumn_max

"""sumary_line
    定义命令对象
    通过将命令传递给角色所属的状态机来完成角色的状态转移
"""

# jumpCommand：跳跃的命令
class JumpCommand(Command):
    def __init__(self,force=10):
        self.force = force
        super().__init__()

    def execute(self,actor):
        actor.set_vy(self.force)

# 移动命令，构造函数包括移动的Δx和Δy
class MoveCommand(Command):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        super().__init__()

    def execute(self, ctrl_obj):
        actor = ctrl_obj
        actor.pos += Vector2(self.x,self.y)
'''

class AudioConfig:
    CHUNK = 256
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 25050
    RECORD_SECONDS = 0.1
    WAVE_OUTPUT_FILENAME = "cache.wav"

''' 
"""sumary_line
    input_handler:处理输入
"""
class ActorInputHandler(InputHandler):
    
    def __init__(self) -> None:
        super().__init__()
        self.audio_frames = []
        '''
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=AudioConfig.FORMAT,
            channels=AudioConfig.CHANNELS,
            rate=AudioConfig.RATE,
            input=True,
            frames_per_buffer=AudioConfig.CHUNK
        )
        '''

    def handle_input(self, key):
        if key == K_SPACE:
            return JumpCommand()
        return None

    def update(self):
        # 持续监测
        '''
        try:
             
            data = self.stream.read(AudioConfig.CHUNK,exception_on_overflow = False)
            self.audio_data = np.fromstring(data, dtype=np.short)
            # print(self.audio_data[len(self.audio_data)-1])
            average_volumn = np.average(np.abs(self.audio_data))
            average_volumn = min(average_volumn,volumn_max)
            print(average_volumn)


            if average_volumn > volumn_threshold["high"]:
                return JumpCommand((average_volumn-volumn_threshold["high"])/400) 
            elif average_volumn > volumn_threshold["low"]:
                return MoveCommand(1.5,0) 

        except Exception as e:
            print(e)
            return None
        '''
        key_list = get_pressed()

        if key_list[K_RIGHT] :
            return MoveCommand(5,0)
        elif key_list[K_LEFT]:
            return MoveCommand(-5,0)
        
class AudioInputHandler(InputHandler):
    def update(self):
        vol = messure(1)
        # print(vol)
        # print(vol)
        if vol<0.05:
            return
        elif vol<0.15:
            return MoveCommand(2,0)
        else:
            return [JumpCommand(),MoveCommand(2,0)]
