import serial
class SerialProcess():
	def __init__(self, port, baud, callback):
		self.callback = callback
		try:
			print(port, baud)
			self.sp = serial.Serial(port, baud, timeout=1)
			print ("SUCCESS: Arduino was found!")
		except Exception as e:
			self.sp = None
			print ("ERROR: Arduino is not attached! Check to see the port appears.")
			raise
	def close(self):
		if self.sp:
			self.sp.close()

	def readSerial(self):
		if self.sp:
			msg= self.sp.readline().decode('utf-8')

			# Extracting flag from the message
			arr= msg.split (":")
			if len (arr) < 2 :
				return None

			acceptedFlags= ["s", "f"]
			flag= arr [0]
			msg = arr [1]

			if flag in acceptedFlags:
				# accept the msg
				if flag == "s":
					return None
				elif flag == "f":
					return float(msg)
				else:
					return None
			else:
				return None

	'''
	Clear the port to serial. 
	Read in last message, parse, then store as a newline in file f.
	'''
	def run(self):
		if self.sp:
			self.sp.flushInput()
			while True:
				if (self.sp.inWaiting() > 0):
					data = self.readSerial()
					if data:
						self.callback(data)
						self.sp.flushInput()
