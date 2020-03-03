import socket
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from drawnow import *



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 8080))
s.listen(5)
x = np.arange(0, 2*np.pi, (2*np.pi)/256)
x_index = 0
x_len = len(x)

f = open("user440.dat", 'w')


# Plot setup
mic = [x for x in range(0,50)]
plt.ion()
amount = 0

def makeFig(): 
    # plt.ylim(80,90)                                 #Set y min and max values
    plt.title('User: Grinder Data')      #Plot the title
    plt.grid(True)                                  #Turn the grid on
    plt.ylabel('Mic Level')                            #Set ylabels
    plt.plot(mic, 'r')       
    plt.show()
    # plt.ylim(-5, 5)       

def onMessage(data): 
    # Plot value
    global amount 

    mic.append(data)
    drawnow(makeFig)
    plt.pause(.00000001)

    if amount == 100:
        print("closing")
        exit()
    amount += 1
    # if (len(mic) > 50):
    #     mic.pop(0)



def procesStreamData(data):
    # string = "".join(s for s in data)
    # print([int(s) for s in example_string.split(',')])
    # print(data)
    print("-------processStreamData:-------")
    f.write(str(data) + "\n")
    # for value in string.split(","):
        # onMessage(np.int16(value))
        # print(value)
    print("-------END processStreamData-------")


        


cl = 0
# # -------------------
while True:
    client, addr = s.accept()

    # client.send(bytes(str(x[x_index]), "utf-8"))
    rec = ""
    while True:
        print("A client connected")
        # data = client.recv(256)

        rec += client.recv(2048*2).decode("utf-8")
        print(rec)
        rec_end = rec.find('\n')
        if rec_end != -1:
            data = rec[:rec_end]

            # Do whatever you want with data here
            print("==========")
            procesStreamData(data)
            print(data)
            print("---------------")
            print("---------------")
            print("---------------")
            print("---------------")
            print("---------------")

            if cl == 4:
                f.close()
                exit()
            cl += 1
            rec = rec[rec_end+1:]
