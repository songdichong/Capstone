from face_recognition import face_locations,face_encodings
import picamera
import os,time,requests
import numpy as np
from gpiozero import MotionSensor

####################### FaceDetection Division #########################
def FaceDetection():
	print("FaceDetection")
	camera = picamera.PiCamera()
	camera.resolution = (320, 240)
	frame = np.empty((240, 320, 3), dtype=np.uint8)	
	# capture a frame
	camera.capture(frame, format="rgb")
	# detecting faces
	for i in range(2):
		face_location = face_locations(frame)
		face_encoding = face_encodings(frame, face_location)
		# if one or more than one face are detected
		if len(face_encoding)>0:
			print('Detected')
			camera.close()
			return True
	camera.close()
	return False

def PIRtask():
	global DETECTEDUSER
	DETECTEDUSER = False
	url = "http://0.0.0.0:4310/getUserFace"
	pir = MotionSensor(4)
	isDetected = 1
	lastmove_time = time.time()
	now_time = lastmove_time
	while True:
		if pir.motion_detected:
			if pir.motion_detected:
				lastmove_time = time.time()
				if DETECTEDUSER == False: 
					print("turn on screen")
					#~ os.system("xset dpms force on")
					DETECTEDUSER = True
					isDetected = 1
					data = {'isDetected': isDetected}
					r = requests.post(url, data)
		else:
			now_time = time.time()
			if now_time - lastmove_time > 10:
				if not FaceDetection():
					# turn off monitor
					DETECTEDUSER = False
					#~ os.system("xset dpms force off")
					isDetected = 0
					data = {'isDetected': isDetected}
					r = requests.post(url, data)
					print("turn off screen")
				else: 
					lastmove_time = time.time()
				
########################################################################
if __name__=="__main__":
	PIRtask()
