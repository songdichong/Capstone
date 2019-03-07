'''
Original Author: Dichong Song, Yuhan Ye, Yue Ma, Shengyao Lu
Creation date: Jan 10, 2019
Contents of file: 
	1. Flask framework (main thread) 
		1.1 render static html source
		1.2 accept message from frontend web page
		1.3 monitor the login/register state
		1.4 handles the login/logout state and send corresponding data to front end
		1.5 find information in database and register in database
		1.6 always on
	2. Xml fetcher (sub-thread)
		2.1 parse content from given url
		2.2 output in json format
		2.3 repeat every hour
	3. FaceDetection
'''
from flask import Flask,render_template,jsonify,request,session,redirect,url_for
from xml.dom import minidom
from urllib.request import urlopen
from pyfingerprint.pyfingerprint import PyFingerprint
import sched, time, _thread,json,io,shlex,subprocess,datetime,sqlite3,requests
import face_recognition
import picamera
import numpy as np

######################### Constant Division ############################
FRONT_END_MSG_RESPOND = 3
FRONT_END_MSG_TAKE_PHOTO = 2
INVALID_USER = -1
MODE_INITIAL = 0
MODE_LOGIN = 1
MODE_REGISTER = 2
MODE_LOGOUT = 3
########################################################################

###################### Initialization Division #########################
app=Flask(__name__)
s = sched.scheduler(time.time, time.sleep)
username = ""
email = ""
userID = INVALID_USER
DETECTEDUSER = False
mode = MODE_INITIAL
databaseName = 'test.db'
########################################################################

################### Useful Function Division ###########################
def xmlfetcher(urllink):
	xml_file = urlopen(urllink)
	mydoc = minidom.parse(xml_file)
	items = mydoc.getElementsByTagName('title')
	result = []
	for item in items:
		result.append(item.firstChild.data)
	return result

def write_to_json(): 
	my_list = xmlfetcher("https://www.cbc.ca/cmlink/rss-topstories")
	f1 = open("./static/upload/newsfeed/news.json","w")
	with io.open('./static/upload/newsfeed/news.json', 'w', encoding='utf-8') as f:
		f.write(json.dumps(my_list, ensure_ascii=False))
	s.enter(3600, 1, write_to_json)
	s.run()
	
def execute_cmd(cmd):
	args = shlex.split(cmd)
	p = subprocess.run(args,stdout = subprocess.PIPE)
	result = p.stdout
	return result

def select_from_database(userID,databaseName):
	conn = sqlite3.connect(databaseName)
	c = conn.cursor()
	t = (int(userID),)
	c.execute('SELECT * FROM User WHERE findex=?',t)
	a=c.fetchone()
	conn.commit()
	conn.close()
	return a

def add_into_database(userID,username,email,preference,databaseName):
	conn = sqlite3.connect(databaseName)
	c = conn.cursor()
	c.execute('''
	INSERT INTO User(findex,username,email,preference)VALUES(?,?,?,?)
	''',(userID,username,email,preference))
	conn.commit()
	conn.close()

def createTable(databaseName):
	conn = sqlite3.connect(databaseName)
	c = conn.cursor()
	c.execute('''
	CREATE TABLE IF NOT EXISTS USER(findex int,username String,email String,preference int)
	''')
	conn.commit()
	conn.close()

def execute_search_fingerprint():
	global DETECTEDUSER
	history_state = False
	while True:
		if DETECTEDUSER == True:
			if history_state != DETECTEDUSER:
				execute_cmd("sudo fuser -k /dev/ttyUSB0")
				execute_cmd("sudo python3 ./pyFingerprint/example_search.py")
				history_state = DETECTEDUSER
		else:
			history_state = False
	
def enroll_fingerprint():
	try:
		f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

		if ( f.verifyPassword() == False ):
			raise ValueError('The given fingerprint sensor password is wrong!')

	except Exception as e:
		print('The fingerprint sensor could not be initialized!')
		print('Exception message: ' + str(e))
		exit(1)

	## Gets some sensor information
	print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

	## Tries to enroll new finger
	try:
		print('Waiting for finger...')

		## Wait that finger is read
		while ( f.readImage() == False ):
			pass

		## Converts read image to characteristics and stores it in charbuffer 1
		f.convertImage(0x01)

		## Checks if finger is already enrolled
		result = f.searchTemplate()
		positionNumber = result[0]

		if ( positionNumber >= 0 ):
			return positionNumber
			#call search
		
		## Creates a template
		f.createTemplate()

		## Saves template at new position number
		positionNumber = f.storeTemplate()
		print('Finger enrolled successfully!')
		print('New template position #' + str(positionNumber))
		
		return positionNumber
	except Exception as e:
		print('Operation failed!')
		print('Exception message: ' + str(e))
		
########################################################################

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
		face_locations = face_recognition.face_locations(frame)
		face_encodings = face_recognition.face_encodings(frame, face_locations)
		# if one or more than one face are detected
		if len(face_encodings)>0:
			print('Detected')
			camera.close()
			return True
	camera.close()
	return False

def PIRtask():  
	global DETECTEDUSER,mode 
	from gpiozero import MotionSensor
	pir = MotionSensor(4)
	disp_on = True
	while True:
		if pir.motion_detected:
			print("You moved")
			DETECTEDUSER = True
			execute_cmd("vcgencmd display_power 1")
			disp_on = True
			for i in range(30):
				time.sleep(1)
		else:
			if disp_on:
				if not FaceDetection():
					# turn off monitor
					execute_cmd("vcgencmd display_power 0")
					DETECTEDUSER = False
					disp_on = False
					mode = MODE_LOGOUT
					execute_cmd("sudo fuser -k /dev/ttyUSB0")
########################################################################

########################## Flask Division ##############################
@app.route('/',methods=['GET','POST'])
def index():
	global userID,username,email,mode,DETECTEDUSER
	if request.method == "POST":
		data = request.form['request'].encode('utf-8')
		print("data",data)
		print("userID",userID)
		print("mode",mode)
		print("DETECTEDUSER",DETECTEDUSER)
		if (int(data) == FRONT_END_MSG_RESPOND) and (userID != INVALID_USER) and (mode == MODE_LOGIN):
			#successfully login
			result = select_from_database(userID,databaseName)
			username = result[1]
			email = result[2]
			preference = result[3]
			mode = MODE_INITIAL
			print(username)
			return jsonify({"mode":"login_success","username":username})
		
		elif (int(data) == FRONT_END_MSG_RESPOND) and (userID == INVALID_USER) and (mode == MODE_LOGIN):
			#unknown user
			mode = MODE_INITIAL
			return jsonify({"mode":"login_fail"})
		
		elif (int(data) == FRONT_END_MSG_RESPOND) and (userID != INVALID_USER) and (mode == MODE_REGISTER):
			#register
			print("here")
			try:
				preference = "11111"
				add_into_database(userID,username,email,preference,databaseName)
				mode = MODE_INITIAL
				_thread.start_new_thread(execute_search_fingerprint,())
				#TODO: logout after timeout
				return jsonify({"mode":"register_success","username":username})
			except Exception:
				mode = MODE_INITIAL
				return jsonify({"mode":"register_fail"})
		
		elif (int(data) == FRONT_END_MSG_RESPOND) and (userID != INVALID_USER) and (mode == MODE_LOGOUT):
			#logout 
			mode = MODE_INITIAL
			username = ""
			email = ""
			userID = INVALID_USER
			return jsonify({"mode":"logout_success"})
		
		elif (int(data) == FRONT_END_MSG_TAKE_PHOTO):
			try:
				execute_cmd("mkdir -p " + username)
				filename = username + "_" + datetime.datetime.now().strftime("%B_%d_%Y_%H:%M:%S")+".jpg"
				msg = execute_cmd("raspistill -n -o "+"./"+username +"/"+filename)
				return jsonify({"mode":"photo_success"})
			except Exception:
				print("some error happens 1")
				return render_template("specialUserPage.html")
				
	return render_template('mainPage.html')

@app.route('/signup',methods=['POST'])
def signup():
	global username,email,mode,userID
	if request.method == "POST":
		email = request.form['gml']
		username = request.form['uname']
		print(email)
		print(username)
		r1 = execute_cmd("sudo fuser -k /dev/ttyUSB0")
		print(r1)
		mode = MODE_REGISTER
		userID = enroll_fingerprint()
		
	return redirect('/')
		
@app.route('/specialUserPage',methods = ['GET'])
def specialUserPage():
	return render_template("specialUserPage.html")

@app.route('/login',methods = ['POST'])
def login():
	global userID,mode
	if request.method == "POST":
		data = request.form['userID']
		print(data)
		userID = int(data)
		mode = MODE_LOGIN
		return "success"

@app.route('/register',methods = ['POST'])
def register():
	global userID,mode
	if request.method == "POST":
		print("here")
		userID = request.form['positionNumber']
		print(userID)
		mode = MODE_REGISTER
		return "success"
########################################################################

######################### Main Function ################################
if __name__=="__main__":
	_thread.start_new_thread(PIRtask,())
	_thread.start_new_thread(execute_search_fingerprint,())
	createTable(databaseName)
	app.debug=True
	app.run(host='0.0.0.0',port=4310)
########################################################################
