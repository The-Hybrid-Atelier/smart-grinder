import socket
import numpy as np
import time

def mapFromTo(x,a,b,c,d):
   y=(x-a)/(b-a)*(d-c)+c
   return np.int16(y)

buffer_size = 512

# Client. Sends a sin wave with 256 samples
fs = 10000

x = np.arange(0, 2*np.pi, (2*np.pi)/buffer_size)
x = np.vectorize(np.sin)(x*440)
x = np.vectorize(mapFromTo)(x, -1, 1, -32768, 32767)


x_index = 0
x_len = len(x)



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('', 8080))
print("starting client!")

while True:
    streamData256 = "".join(str(audioData)+"," for audioData in x) + "\n"
    s.send(bytes(streamData256, "utf-8"))
    # s.send(bytes(str(x[x_index]) + "\n", "utf-8"))
    x_index = (x_index + 1) % x_len