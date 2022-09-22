from actor_input_handler import JumpCommand, MoveCommand
from base.command import InputHandler
import numpy as np
import pyaudio
from config import *
import threading
#import pyaudio
import numpy as np
from config import volumn_threshold,volumn_max
import math

from singleton import Singleton
from pygame.key import get_pressed
from base.command import InputHandler
from volume import messure


class AudioConfig:
    CHUNK = 256
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 25050
    RECORD_SECONDS = 0.1
    WAVE_OUTPUT_FILENAME = "cache.wav"


"""sumary_line
    input_handler:处理输入
"""

class ActorInputHandler(InputHandler):
    
    def __init__(self) -> None:
        super().__init__()
        self.audio_frames = []
        
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=AudioConfig.FORMAT,
            channels=AudioConfig.CHANNELS,
            rate=AudioConfig.RATE,
            input=True,
            frames_per_buffer=AudioConfig.CHUNK
        )
        

    def handle_input(self, key):
        pass 

    def update(self):
        # 持续监测
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

class AudioInputThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.vol = 0
        self.is_running = True

    def run(self) -> None:
        while self.is_running:
            self.vol = messure(1)
            Singleton.get_instance().set_volumn(self.vol)

    def terminate(self):
        self.is_running = False
    
class AudioInputHandler(InputHandler):
    def __init__(self) -> None:
        super().__init__()
        self.vol = 0
        self.audio_thread = AudioInputThread()
        self.audio_thread.start()


    def update(self):

        self.vol = Singleton.get_instance().get_volume()
        
        if self.vol<0.011:
            return
        elif self.vol<0.15:
            return MoveCommand(2,0)
        else:
            return [JumpCommand(50*math.sqrt(self.vol - 0.15)),MoveCommand(2,0)]

    def dispose(self):
        self.audio_thread.terminate()

     

        