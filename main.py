import serial
arduino=serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=.2)
while True:
	data=''
	if arduino.inWaiting():
		data = arduino.readline()[:-1] #the last bit gets rid of the new-line chars
		print(data.decode())