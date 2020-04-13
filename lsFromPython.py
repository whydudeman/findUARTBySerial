import glob
import serial
import sys
import json
import requests
import hashlib
import uuid
import os
import datetime
import time, threading
import schedule
url = 'http://188.40.108.37:8084/sensor/v1/'
kwh=0.0
counter=0
impulse=1600
filialId=23
usb_port=''

def find_port(port_name=None,baudrate=9600,timeout=0.2):
	if sys.platform.startswith('win'):
  		ports = ['COM%s' % (i+1) for i in range(256)]
	elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
  		ports = glob.glob('/dev/ttyUSB*')
	elif sys.platform.startswith('darwin'):
  		ports = glob.glob('/dev/tty.usbserial*')
	else:
  		raise EnvironmentError('Error finding ports on your operating system')
	print("Scanning port for UART signals")
	arduino_port = ''
	for port in ports:
		try:
  			arduino = serial.Serial(port=port,baudrate = baudrate, timeout=timeout)
  			print(arduino)
  			datayes = arduino.inWaiting()
	  		print(datayes)
	  		arduino_serial = openbci_id(arduino)
	  		print(arduino_serial)
	  		arduino.close()
	  		if arduino_serial:
	  			arduino_port = port;
	  			print(arduino_port)
		except (OSError, serial.SerialException) as e:
			print(e)
			pass
		except Exception as e:
			print(e)
			pass
	return arduino_port
def openbci_id(serial):
    """

    When automatically detecting port, parse the serial return for the "OpenBCI" ID.

    """
    line = ''
    #Wait for device to send data
    time.sleep(2)
    c=''
    if serial.inWaiting():
    	c = serial.read().decode('utf-8')
    if len(c)>0:
    	print(len(c))
    	return True
    return False
def save_data(sensor_value):
	# write filestamp file
	file = open("last.txt", "w")
	print(str(sensor_value)+" HEllos")
	file.write(str(sensor_value))
	file.close()
	kwh=sensor_value
	return sensor_value
def load_data(kwh):
	print(kwh)
	if os.path.exists('last.txt') == False:
	    file = open("last.txt", "w")
	    file.write(kwh)
	    file.close()
	    return kwh
		#read last filestamp file stored
	else:
		file = open("last.txt", "r")
		kwh = float(file.read())
		file.close()
		return kwh
def send_post():
	t = threading.Timer(600.0, send_post)
	t.start()
	save_data(kwh)
	date=datetime.datetime.now()
	date=date.strftime("%Y-%m-%dT%H:%M:%S")
	unique_id=hashlib.sha224(str(uuid.getnode()).encode()).hexdigest()	
	data = {"value" : kwh, "date" : date, "filialId":filialId,"identity":unique_id}
	r1=requests.post(url=url,json=data)
	print(r1.text)
def job():
    print("I'm running on thread")
def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()
# kwh=save_data(12.4)
kwh=load_data(kwh)
send_post()
# t = threading.Timer(600, send_post)
# t.start()
while True:
	try:
		print("tring to find port")
		usb_port=find_port()
		print(usb_port+" usb_port")
		if usb_port=='':
			print("No proper USB device found")
			time.sleep(5)
			continue
	except Exception as e:
		print(e)
		continue
	except KeyboardInterrupt:
		break
	else:
		try:
			arduino=serial.Serial(usb_port, baudrate=9600, timeout=.2)
			while True:
				data=''
				if arduino.inWaiting():
					data = arduino.readline()[:-1] #the last bit gets rid of the new-line chars
					print(data.decode())
					if data.decode()=='1kwh':
						kwh=kwh+1/impulse
						currentTime=datetime.datetime.now()
						currentTime=currentTime.strftime("%Y-%m-%dT%H:%M:%S")
						print(kwh)
			# if data:
			# 	print(arduino.read())
			# 	# parsed_json = (json.loads(data))
			# 	# x = requests.post(url+"messages", json = parsed_json)
			# 	# print(x.text)

		except (OSError, serial.SerialException) as e:
			print(e)
			pass
		except Exception as e:
			print(e)
			pass
