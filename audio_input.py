"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import wave
import time
import sys
import numpy as np
from numpy.core.fromnumeric import shape
from numpy.lib.function_base import average

# instantiate PyAudio (1)
p = pyaudio.PyAudio()


RATE = 48000
SEC  = 0.2
CHUNK= 256

# open stream using callback (3)
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# start the stream (4)
stream.start_stream()

while True:
    data = stream.read(CHUNK)
    audio_data = np.fromstring(data,dtype=np.short)
    abs_data = np.abs(audio_data)
    average_data = np.average(abs_data)
    print(average_data)