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
	for i in range(5):
		# detecting faces
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
	DETECTEDUSER = False
	url = "http://0.0.0.0:4310/getUserFace"
	pir = MotionSensor(4)
	isDetected = 1
	while True:
		if pir.motion_detected:
			print("You moved")
			DETECTEDUSER = True
			isDetected = 1
			data = {'isDetected': isDetected}
			r = requests.post(url, data)
			time.sleep(60)
		
		else:
			if not FaceDetection():
				# turn off monitor
				DETECTEDUSER = False
				isDetected = 0
				data = {'isDetected': isDetected}
				r = requests.post(url, data)
				print("turn off screen")
				time.sleep(0.5)
				
########################################################################
if __name__=="__main__":
	PIRtask()
