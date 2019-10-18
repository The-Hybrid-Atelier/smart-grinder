import time, datetime, atexit, sys, getopt, json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
from serial_process import SerialProcess
from drawnow import *
'''
Executing this script will opens a serial port to an Arduino, 
reads in values, and store them to a file.

The serial messages coming from the arduino have been formatted as follows:
<flag>:<value>\n

flag: a character that denotes the value's data type (e.g., 's'=string, 'i'=int, 'f'=float)
value: the string representation of the value

The file holds a timestamp on the first line, followed by each message received from the Arduino
during the duration of the session. Messages are separated by newlines (\n).
'''

# Setup plot
plt.ion()
mic=[]
cnt=0

def main(argv):
	user, port, baud = parseCommandLineArgs(argv)	
	print ("\tStoring data in: /%s.txt"%user)
	print ("\tOpening %s @ %s" % (port, baud))
	openAndReadPort(user, port, baud)
	

'''
Retrieves parameters from the command line to override default values.
Params include: 
* -u : a user_id that will be used to generate a unique file to store mic recordings
* -p : the port that the Arduino microphone is attached to
* -b : the communication speed of the Arduino
'''
DEFAULT_SERIAL_PORT = '/dev/cu.usbmodem00001'
DEFAULT_SERIAL_BAUDRATE = 9600

def parseCommandLineArgs(argv):
	user = ''
	port = DEFAULT_SERIAL_PORT
	baud = DEFAULT_SERIAL_BAUDRATE

	opts, args = getopt.getopt(argv,"u:p:b:",["user=", "port=", "baud="])

	for opt, arg in opts:
		if opt in ("-u", "--user"):
			user = arg
		if opt in ("-p", "--port"):
			port = arg
		if opt in ("-b", "--baud"):
			baud = arg

	return user, port, baud


'''
Given a user and serial port, we will open the serial port and write all
incoming values to a file /data/<user>.txt. The epoch timestamp is appended as
the first line of the file. 
'''
def openAndReadPort(user, port, baud):
	def makeFig(): 
			plt.ylim(80,90)                                 #Set y min and max values
			plt.title('User %s: Grinder Data' % user)      #Plot the title
			plt.grid(True)                                  #Turn the grid on
			plt.ylabel('Mic Level')                            #Set ylabels
			plt.plot(mic, 'r')       
			plt.show()
			plt.ylim(0,1)                           #Set limits of second y axis- adjust to readings you are getting
			
	# Handle message data logic
	def onMessage(data): 
		# Write value to file
		f.write(str(data) + "\n")

		# Plot value
		mic.append(data)
		drawnow(makeFig)
		plt.pause(.000001)
		if (len(mic) > 50):
			mic.pop(0)


	try:
		filename = "data/%s.txt" % user

		f = open(filename,"w+")
		
		# Write timestamp as firstline of file
		dt = datetime.now()
		timestamp = datetime.timestamp(dt)
		f.write("%s\n"% timestamp)
		print("\tTimestamp: %s (%s)" % (dt, timestamp))

		sp = SerialProcess(port, baud, onMessage)
		sp.run()
	
	except KeyboardInterrupt:
		f.close()
		print ("\nFile closed. Recording is located at:\t /data%s.txt" % user)


if __name__ == "__main__":
	main(sys.argv[1:])