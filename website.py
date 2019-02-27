'''
Original Author: Dichong Song, Yuhan Ye, Yue Ma
Creation date: Jan 10, 2019
Contents of file: 
	1. Flask framework (main thread) 
		1.1 render static html source
		1.2 communicate with frontend web page
		1.3 always on
	2. Xml fetcher (sub-thread)
		2.1 parse content from given url
		2.2 output in json format
		2.3 repeat every hour
'''
from flask import Flask,render_template,jsonify,request,session,redirect,url_for
from xml.dom import minidom
from urllib.request import urlopen
from pyfingerprint.pyfingerprint import PyFingerprint
import sched, time, _thread,json,io,shlex,subprocess,datetime,sqlite3
import cv2
import face_recognition

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
DETECTEDUSER = "False"
mode = MODE_INITIAL
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

def select_from_database(userID):
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	t = (int(userID),)
	c.execute('SELECT * FROM User WHERE findex=?',t)
	a=c.fetchone()
	conn.commit()
	conn.close()
	return a
	
def add_into_database(userID,username,email,preference):
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	c.execute('''
	INSERT INTO User(findex,username,email,preference)VALUES(?,?,?,?)
	''',(userID,username,email,preference))
	conn.commit()
	conn.close()
########################################################################


####################### OpenCV Division ################################
def FaceDetection(video_capture):

	process_this_frame = True

	# Grab a single frame of video
	ret, frame = video_capture.read()
	# Resize frame of video to 1/4 size for faster face recognition processing
	small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
	# Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
	rgb_small_frame = small_frame[:, :, ::-1]

	# Only process every other frame of video to save time
	if process_this_frame:
		detected_face = False
		# # Find all the faces and face encodings in the current frame of video
		# face_locations = face_recognition.face_locations(rgb_small_frame)
		# face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

		face_landmarks_list = face_recognition.face_landmarks(rgb_small_frame)
		for face_landmarks in face_landmarks_list:
			detected_face = True
			break
		if detected_face:
			print("Face Detected.")

			return "True"
	#video_capture.release()
	return "False"
	# Release handle to the webcam

def task2():
	global DETECTEDUSER
	video_capture = cv2.VideoCapture(0)
	while True:

		DETECTEDUSER = FaceDetection(video_capture)
########################################################################

########################## Flask Division ##############################
@app.route('/',methods=['GET','POST'])
def index():
	global userID,username,email,mode
	if request.method == "POST":
		data = request.form['request'].encode('utf-8')
		print(data)
		print(userID)
		print(mode)
		if (int(data) == FRONT_END_MSG_RESPOND) and (userID != INVALID_USER) and (mode == MODE_LOGIN):
			#successfully login
			result = select_from_database(userID)
			username = result[1]
			email = result[2]
			preference = result[3]
			mode = MODE_INITIAL
			print(username)
			return jsonify({"mode":"login_success","username":username})
			
		elif (int(data) == FRONT_END_MSG_RESPOND) and (userID != INVALID_USER) and (mode == MODE_REGISTER):
			#register
			preference = "11111"
			add_into_database(userID,username,email,preference)
			mode = MODE_INITIAL
			r = execute_cmd("sudo python3 example_search.py")
			print(r)
			#TODO: logout after timeout
			return jsonify({"mode":"register_success","username":username})
		
		elif (int(data) == FRONT_END_MSG_RESPOND) and (userID != INVALID_USER) and (mode == MODE_LOGOUT):
			#logout 
			mode = MODE_INITIAL
			username = ""
			email = ""
			userID = INVALID_USER
			return redirect('/')
		
		elif (int(data) == FRONT_END_MSG_TAKE_PHOTO):
			try:
				execute_cmd("mkdir -p " + username)
				filename = username + "_" + datetime.datetime.now().strftime("%B_%d_%Y_%H:%M:%S")+".jpg"
				msg = execute_cmd("raspistill -n -o "+"./"+username +"/"+filename)
				return jsonify({"status":msg})
			except Exception:
				print("some error happens 1")
				return render_template("specialUserPage.html")
	return render_template('mainPage.html')

@app.route('/signup',methods=['POST'])
def signup():
	global username,email
	if request.method == "POST":
		email = request.form['gml']
		username = request.form['uname']
		print(email)
		print(username)
		r1 = execute_cmd("sudo fuser -k /dev/ttyUSB0")
		print(r1)
		r2 = execute_cmd("sudo python3 example_enroll.py")
		print(r2)
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
	#_thread.start_new_thread(write_to_json,())
	# _thread.start_new_thread(remote_controller,())
	#~ _thread.start_new_thread(task2,())
	app.debug=True
	app.run(host='0.0.0.0',port=4310)
########################################################################
