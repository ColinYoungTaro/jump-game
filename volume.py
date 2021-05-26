import pyaudio
import struct
import math
CHUNK = 200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000

def messure(times):
    voice_volume = rec(times)
    return (sum(voice_volume)/times)

# 测量
def rec(times):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []
    for _ in range(0, times):
        data = stream.read(CHUNK,exception_on_overflow=False)
        data_f = rms(data)
        frames.append(float(data_f))
    stream.stop_stream()
    stream.close()
    # p.terminate()
    return frames

# 计算音量
def rms( data ):
    count = len(data)/2
    format = "%dh"%(count)
    shorts = struct.unpack(format, data)
    sum_squares = 0.0
    for sample in shorts:
        n = sample * (1.0 / 32768)
        sum_squares += n*n
    return math.sqrt(sum_squares / count)

