import numpy as np
import soundfile as sf
import sounddevice as sd

file_data = ""
fs = 10000
bufferSize = 512


sd.default.samplerate = fs


with open("user440.dat", 'r') as f:
    file_data = f.read()


samples = [np.int16(s) for s in file_data.split(",")[:-1]]


sd.play(samples, blocking=True)
