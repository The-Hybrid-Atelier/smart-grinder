import serial
import time
import datetime
from datetime import datetime
import json
import queue
import atexit
import sys, getopt

## Change this to match your local settings
SERIAL_PORT = '/dev/cu.usbmodem00001'
SERIAL_BAUDRATE = 9600


class SerialProcess():
    def __init__(self, input_queue, output_queue, f):
        self.f = f
        self.input_queue = input_queue
        self.output_queue = output_queue
        try:
            self.sp = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=1)
            print ("SUCCESS: Arduino was found!")
        except Exception as e:
            # raise e
            self.sp = None
            print ("ERROR: Arduino is not attached! Check to make sure the USB for the door alarm is connected to the BiD computer.")
    def opened(self):
        return self.sp
    def close(self):
        if self.sp:
            self.sp.close()

    def writeSerial(self, data):
        if self.sp:
            self.sp.write(data)
        # time.sleep(1)

    def readSerial(self):
        if self.sp:
            # return self.sp.readline().replace("\n", "")
            msg= self.sp.readline().decode('utf-8')
            # Extracting flag from the message
            arr= msg.split (":")
            if len (arr) < 1 :
                return None

            acceptedFlags= ["s", "f"]
            flag= arr [0]
            msg = arr [1]

            if flag in acceptedFlags:
                # accept the msg
                if flag == "s":
                    return msg
                elif flag == "f":
                    return float(msg)
                else:
                    return None
            else:
                return None

            # return decipher_message(self.sp.readline())

    def run(self):
        if self.sp:
            self.sp.flushInput()
            while True:
                # look for incoming tornado request
                if not self.input_queue.empty():
                    data = self.input_queue.get()

                    # send it to the serial device
                    self.writeSerial(data)
                    print ("writing to serial: ", data)

                # look for incoming serial data
                if (self.sp.inWaiting() > 0):
                    data = self.readSerial()
                    if data:
                        print ("reading from serial: ", data )
                        # send it back to tornado
                        self.output_queue.put(data)
                        self.f.write(str(data) + "\n")

def writeToFile(userID):
    try:

        f = open(str(userID) + ".txt","w+")

        now = datetime.now()
        timestamp = datetime.timestamp(now)

        f.write(str(timestamp) + '\n')
        q1 = queue.Queue()
        q2 = queue.Queue()
        sp = SerialProcess(q1, q2, f)
        sp.run()
    except KeyboardInterrupt:
        f.close()
        print ("FILE HAS CLOSED")
        # raise

# Read what was specified with -u
def main(argv):
   user = ''

   opts, args = getopt.getopt(argv,"u:",["user="])
   for opt, arg in opts:
      if opt in ("-u", "--user"):
         user = arg
   print ("User file is" , user)
   writeToFile(user)

if __name__ == "__main__":
   main(sys.argv[1:])
